import inspect
import json
import os
import pathlib
import sys
import time
from typing import Literal
from xml.etree import ElementTree

import gdsfactory as gf
import kfactory
import uvicorn
import yaml
from fastapi import Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from natsort import natsorted

from gdsfactoryplus.core.generate_svg import generate_svg

from ..core.cli.app import app as cli
from ..core.cli.patch_netlist import changed as _changed
from ..core.cli.patch_netlist import modify_body as _modify_body
from ..core.cli.patch_netlist import patch_netlist_post as _patch_netlist_post
from ..core.cli.tree import _tree, get_args
from ..core.cli.tree_item import _tree_item
from ..core.netlist import ensure_netlist_order, patch_netlist
from ..core.shared import (
    activate_pdk_by_name,
    get_active_pdk,
    get_custom_cell_names,
    get_pdk_cell_names,
)
from ..core.show import send_error
from ..settings import SETTINGS as s
from ..settings import find_docode_project_dir, maybe_find_docode_project_dir

try:
    from doweb.api.viewer import FileView, file_view_static  # type: ignore
    from doweb.browser import get_app  # type: ignore
except ImportError:
    from kweb.api.viewer import FileView, file_view_static
    from kweb.browser import get_app

PDK: str = s.pdk.name
PROJECT_DIR: str = maybe_find_docode_project_dir() or os.getcwd()


kfactory.conf.config.cell_layout_cache = False
app = get_app(fileslocation=PROJECT_DIR, editable=False)


def needs_to_be_removed(path):
    if path == "/":
        return True
    elif path.startswith("/file"):
        return True
    elif path.startswith("/gds"):
        return True


app.router.routes = [r for r in app.routes if not needs_to_be_removed(r.path)]  # type: ignore

this_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(this_dir, "static")
app.mount("/static2", StaticFiles(directory=static_dir), name="static2")
templates = Jinja2Templates(directory=os.path.join(this_dir, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@cli.command()
def serve(
    pdk: str = PDK,
    port: int = 8787,
    host: str = "0.0.0.0",
    reload: bool = False,
    workers: int = 0,
):
    print(f"{pdk=}\nproject_dir={PROJECT_DIR}\n{port=}\n{host=}", file=sys.stderr)
    uvicorn.run(
        "gdsfactoryplus.cli.serve:app",
        forwarded_allow_ips="*",
        host=host,
        port=int(port),
        proxy_headers=True,
        reload=reload,
        use_colors=True,
        workers=workers if workers > 0 else None,
    )


@app.get("/")
def redirect():
    return RedirectResponse("/code/")


@app.get("/code")
def code():
    return "gfp server is running."


@app.post("/patch-netlist")
def patch_netlist_post(path: str, body: str = Body(...), schemapath: str = ""):
    activate_pdk_by_name(PDK)
    try:
        content = _patch_netlist_post(path, body, schemapath, PDK)
    except Exception as e:
        send_error(e.__class__.__name__, str(e), path)
        raise e from e
    return PlainTextResponse(content)


@app.get("/patch-netlist")
def patch_netlist_get(path: str, schemapath: str = ""):
    activate_pdk_by_name(PDK)
    content = _patch_netlist_post(path, "", schemapath, PDK)
    return PlainTextResponse(content)


@app.get("/pdk")
def pdk():
    return PlainTextResponse(PDK)


@app.get("/dir")
def project_dir():
    return PlainTextResponse(PROJECT_DIR)


@app.get("/pdk/list")
def list_custom():
    pdk = activate_pdk_by_name(PDK)
    resp = {
        "custom": get_custom_cell_names(pdk),
        "pdk": get_pdk_cell_names(pdk),
        "all": natsorted(pdk.cells),
    }
    return resp


@app.get("/settings/{component}")
def settings(component: str):
    pdk = activate_pdk_by_name(PDK)
    try:
        types = _get_allowed_instance_settings(pdk.cells[component])
        defaults = get_args(pdk.cells[component])
    except KeyError:
        types, defaults = {}, {}
    ret = {
        "name": component,
        "settings": {},
        "refs": {},
    }
    for key, tp in types.items():
        ret["settings"][key] = {
            "type": tp,
        }
        if key in defaults:
            ret["settings"][key]["default"] = defaults[key]
            if defaults[key] in pdk.cells:
                if not "@component" in ret["refs"]:
                    ret["refs"]["@component"] = list(pdk.cells)
                ret["settings"][key]["type"] = "@component"
            if defaults[key] in pdk.cross_sections:
                if not "@cross_section" in ret["refs"]:
                    ret["refs"]["@cross_section"] = [
                        xs for xs in pdk.cross_sections if xs != "cross_section"
                    ]
                ret["settings"][key]["type"] = "@cross_section"
    return ret


@app.get("/tree")
def tree(
    path: str = s.name,
    by: Literal["cell", "file", "flat"] = "cell",
    key: str = "",
    format: str = "yaml",
):
    activate_pdk_by_name(PDK)
    tree = _tree(path, by, key, format)
    if str(format).strip().lower() == "json":
        return JSONResponse(json.loads(tree))
    else:
        return PlainTextResponse(tree)


@app.post("/save")
def save_post(body: str = Body(...), *, path: str):
    if not path.endswith(".pic.yml"):
        return PlainTextResponse(f"{path!r} is not a .pic.yml file.", status_code=422)
    try:
        netlist_and_schematic = yaml.safe_load(body)
    except Exception:
        netlist_and_schematic = {}
    if not isinstance(netlist_and_schematic, dict):
        netlist_and_schematic = {}
    netlist = netlist_and_schematic.get("netlist", {})
    schematic = netlist_and_schematic.get("schematic", {})
    schematic_path = f"{path[:-8]}.scm.yml"
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    repo_dir = find_docode_project_dir()
    schema_dir = os.path.join(repo_dir, "build", "schemas")
    pics_dir = os.path.join(repo_dir, s.name)
    schema_path = os.path.relpath(
        os.path.join(schema_dir, os.path.relpath(f"{path[:-8]}.json", pics_dir)),
        pics_dir,
    )
    with open(schematic_path, "w") as file:
        yaml.safe_dump(schematic, file, sort_keys=False)
    yaml_str = yaml.safe_dump(netlist, sort_keys=False)
    yaml_str = f"# yaml-language-server: $schema={schema_path}\n{yaml_str}"
    with open(path, "w") as file:
        file.write(yaml_str)
    return PlainTextResponse(f"netlist saved to {path}.")


@app.get("/save")
def save_get(body: str, path: str):
    return save_post(body=body, path=path)


@app.get("/load")
def load(path: str):
    if not path.endswith(".pic.yml"):
        return PlainTextResponse(f"{path!r} is not a .pic.yml file.", status_code=422)
    schematic_path = f"{path[:-8]}.scm.yml"
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    if os.path.exists(path):
        netlist = yaml.safe_load(open(path))
    else:
        netlist = {}
    if not isinstance(netlist, dict):
        netlist = {}
    if os.path.exists(schematic_path):
        schematic = yaml.safe_load(open(schematic_path))
    else:
        schematic = {}
    if not isinstance(schematic, dict):
        schematic = {}
    ret = {
        "netlist": netlist,
        "schematic": schematic,
    }
    return ret


@app.get("/tree-item")
def tree_item(
    name: str,
    path: str = s.name,
    key: str = "",
    format: str = "yaml",
):
    activate_pdk_by_name(PDK)
    try:
        tree = _tree_item(name, path, key, format)
    except KeyError:
        tree = "{}"
    if str(format).strip().lower() == "json":
        return JSONResponse(json.loads(tree))
    else:
        return PlainTextResponse(tree)


@app.get("/svg/{component}.svg")
def svg(component: str, width: int = 80, height: int = 80):
    pdk = activate_pdk_by_name(PDK)
    try:
        comp = pdk.get_component(component)
    except Exception:
        comp = gf.Component()
    assert isinstance(comp, gf.Component)
    svg = generate_svg(comp, width, height)
    return Response(svg, media_type="image/svg+xml")


@app.get("/view2")
async def view2(
    request: Request,
    file: str,
    cell: str = "",
    rdb: str = "",
    theme: Literal["light", "dark"] = "dark",
    regen_lyp: bool = False,
):
    if rdb:
        rdbs = rdb.split(",")
        rdb = os.path.join("build", "lyrdb", os.path.basename(rdbs[0]))
        xmls = [open(xml).read() for xml in rdbs]
        xml = merge_rdb_strings(*xmls)
        open(rdb, "w").write(xml)

    assert PROJECT_DIR is not None
    layer_props = os.path.join(PROJECT_DIR, "build", "lyp", f"{PDK}.lyp")
    if regen_lyp or not os.path.exists(layer_props):
        _pdk = get_active_pdk()
        layer_views = _pdk.layer_views
        assert layer_views is not None
        layer_views.to_lyp(filepath=layer_props)

    try:
        fv = FileView(
            file=pathlib.Path(file),
            cell=cell or None,
            layer_props=layer_props,
            rdb=rdb or None,
        )
        resp = await file_view_static(request, fv)  # type: ignore
    except HTTPException as e:
        print(e, file=sys.stderr)
        color = "#f5f5f5" if theme == "light" else "#121317"
        return HTMLResponse(f'<body style="background-color: {color}"></body>')
    body = resp.body.decode()  # type: ignore
    body = _modify_body(resp.body.decode(), theme, file)  # type: ignore
    return HTMLResponse(body)


@app.get("/changed")
async def changed(path: str):
    assert PROJECT_DIR is not None
    return _changed(PROJECT_DIR, path)


def merge_rdb_strings(*xml_strings: str) -> str:
    # Parse the first XML string
    root = ElementTree.fromstring(xml_strings[0])
    tree = ElementTree.ElementTree(root)

    # Define sets to track unique cells and categories
    unique_cells = set()
    unique_categories = set()

    # Helper function to extract cells, categories, and items
    def extract_elements(root):
        cells = root.find(".//cells")
        categories = root.find(".//categories")
        items = root.find(".//items")
        return cells, categories, items

    # Extract elements from the first string
    base_cells, base_categories, base_items = extract_elements(root)

    # Track unique cells and categories
    for cell in base_cells:  # type: ignore
        unique_cells.add(ElementTree.tostring(cell))
    for category in base_categories:  # type: ignore
        unique_categories.add(ElementTree.tostring(category))

    # Process subsequent strings
    for xml_string in xml_strings[1:]:
        root = ElementTree.fromstring(xml_string)
        cells, categories, items = extract_elements(root)

        # Add unique cells
        for cell in cells:  # type: ignore
            cell_str = ElementTree.tostring(cell)
            if cell_str not in unique_cells:
                unique_cells.add(cell_str)
                base_cells.append(cell)  # type: ignore

        # Add unique categories
        for category in categories:  # type: ignore
            category_str = ElementTree.tostring(category)
            if category_str not in unique_categories:
                unique_categories.add(category_str)
                base_categories.append(category)  # type: ignore

        # Add all items
        for item in items:  # type: ignore
            base_items.append(item)  # type: ignore

    # Convert the final tree to a string
    merged_xml_string = ElementTree.tostring(tree.getroot(), encoding="utf-8")
    return merged_xml_string.decode("utf-8")


@app.get("/yaml/edit")
def edit(request: Request, path: str = "", theme: str = "dark"):
    activate_pdk_by_name(PDK)
    netlist = _load_netlist(path)

    if isinstance(netlist, Response):
        return netlist

    return templates.TemplateResponse(
        request,
        "index.html",
        {"path": path, "netlist": netlist, "theme": theme},
    )


@app.get("/yaml/delete")
def delete(path: str = "", what=""):
    activate_pdk_by_name(PDK)
    if what == "" or path == "":
        return Response(status_code=404)

    netlist = subnetlist = _load_netlist(path)
    if isinstance(netlist, Response):
        return netlist

    what = what.replace("--", ",").split("-")

    if len(what) < 2:
        # TODO: return error ?
        return HTMLResponse("")

    key = None
    for key in what[:-1]:
        assert not isinstance(subnetlist, Response)
        subnetlist = subnetlist[key]

    assert not isinstance(subnetlist, Response)
    if what[-1] in subnetlist:
        del subnetlist[what[-1]]
        _save_netlist(netlist, path)
    else:
        pass  # TODO: return error ?

    return PlainTextResponse("")


@app.get("/yaml/add")
def add(request: Request, path: str = "", what=""):
    activate_pdk_by_name(PDK)
    if what == "" or path == "":
        return Response(status_code=404)
    what = tuple(what.replace("--", ",").split("-"))
    pdk = get_active_pdk()

    netlist = _load_netlist(path)
    if isinstance(netlist, Response):
        return netlist

    assert isinstance(netlist, dict)
    if what[0] == "routes" and len(what) == 1:
        netlist["routes"] = {"_": {"links": {}}, **netlist.get("routes", {})}
        return templates.TemplateResponse(
            request,
            "routes.html",
            {"netlist": netlist, "path": path, "goto": "routes-_-editvalue"},
        )
    elif what[0] == "routes" and len(what) == 2:
        name = what[1]
        routes = netlist["routes"]

        routes[name] = routes.get(name, {})
        if not "links" in routes[name]:
            routes[name]["links"] = {}
        # TODO: add to html!
        elif not "routing_strategy" in routes[name]:
            routes[name]["routing_strategy"] = list(pdk.routing_strategies)[0]  # type: ignore
        elif not "settings" in routes[name]:
            routes[name]["settings"] = {}

        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request, "route.html", {"route": routes[name], "name": name, "path": path}
        )
    elif what[0] == "routes" and len(what) == 3 and what[-1] == "settings":
        name = what[1]
        routes = netlist["routes"]
        route = routes[name]
        route["settings"] = {"_": "_", **route.get("settings", {})}
        return templates.TemplateResponse(
            request,
            "settings.html",
            {
                "name": name,
                "path": path,
                "settings": route["settings"],
                "goto": f"routes-{name}-settings-_-editvalue",
                "which": "routes",
            },
        )
    elif what[0] == "routes" and len(what) == 3 and what[-1] == "links":
        name = what[1]
        routes = netlist["routes"]
        route = routes[name]
        route["links"] = {"_": "_", **route.get("links", {})}
        return templates.TemplateResponse(
            request,
            "links.html",
            {
                "route": routes[name],
                "name": name,
                "path": path,
                "goto": f"routes-{name}-links-_-editvalue",
            },
        )
    elif what[0] == "connections" and len(what) == 1:
        netlist["connections"] = {"_": "_", **netlist.get("connections", {})}
        return templates.TemplateResponse(
            request,
            "connections.html",
            {"netlist": netlist, "path": path, "goto": "connections-_-editvalue"},
        )
    elif what[0] == "ports" and len(what) == 1:
        netlist["ports"] = {"_": "_", **netlist.get("ports", {})}
        return templates.TemplateResponse(
            request,
            "ports.html",
            {"netlist": netlist, "path": path, "goto": "ports-_-editvalue"},
        )
    elif what[0] == "instances" and len(what) == 1:
        netlist["instances"] = {
            "_": {
                "component": "straight",
                "settings": {},
            },
            **netlist.get("instances", {}),
        }
        return templates.TemplateResponse(
            request,
            "instances.html",
            {"netlist": netlist, "path": path, "goto": f"instances-_-editvalue"},
        )
    elif what[0] == "instances" and len(what) == 2:
        name = what[1]
        instances = netlist["instances"]
        instance = instances[name]
        instances[name] = {
            "component": instance.get("component", "straight"),
            "settings": instance.get("settings", {}),
        }
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "instance.html",
            {"instance": instances[name], "name": name, "path": path},
        )
    elif what[0] == "instances" and len(what) == 3 and what[-1] == "settings":
        name = what[1]
        instances = netlist["instances"]
        instance = instances[name]
        instance["settings"] = {"_": "_", **instance.get("settings", {})}
        return templates.TemplateResponse(
            request,
            "settings.html",
            {
                "name": name,
                "path": path,
                "settings": instance["settings"],
                "goto": f"instances-{name}-settings-_-editvalue",
                "which": "instances",
            },
        )
    elif what[0] == "placements" and len(what) == 1:
        netlist["placements"] = {"_": {}, **netlist.get("placements", {})}
        return templates.TemplateResponse(
            request,
            "placements.html",
            {"netlist": netlist, "path": path, "goto": "placements-_-editvalue"},
        )
    elif what[0] == "placements" and len(what) == 2:
        name = what[1]
        placements = netlist["placements"]
        placement = placements[name]
        placements[name] = {"_": "_", **placement}
        return templates.TemplateResponse(
            request,
            "placement.html",
            {
                "placement": placements[name],
                "name": name,
                "path": path,
                "goto": f"placements-{name}-_-editvalue",
            },
        )

    return PlainTextResponse("")


@app.get("/yaml/editvalue")
def editvalue(request: Request, path: str = "", what: str = "", added: bool = False):
    activate_pdk_by_name(PDK)
    if what == "" or path == "":
        return Response(status_code=404)
    if not path.endswith(".pic.yml"):
        return PlainTextResponse(f"{path!r} is not a .pic.yml file.", status_code=422)
    this_cell_name = os.path.basename(path)[:-8]
    what = tuple(what.replace("--", ",").split("-"))  # type: ignore
    pdk = get_active_pdk()

    netlist = _load_netlist(path)
    if isinstance(netlist, Response):
        return netlist

    if what[0] == "instances" and len(what) == 2:
        _, name = what
        return templates.TemplateResponse(
            request,
            "edit_name.html",
            {
                "path": path,
                "name": name,
                "what": "instances",
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )
    elif what[0] == "instances" and what[2] == "settings":
        try:
            _, name, _, key = what
            value = netlist["instances"][name]["settings"].get(key, "_")
            component = netlist["instances"][name]["component"]
            allowed_values = _get_allowed_instance_settings(pdk.cells[component])
            given_values = [
                k for k in list(netlist["instances"][name]["settings"]) if k != "_"
            ]
            allowed_values = {
                k: v
                for k, v in allowed_values.items()
                if k == key or k not in given_values
            }
            if len(allowed_values) < 1:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {"error": "no more settings for this component."},
                )

            if value == "_":
                key, value = list(allowed_values.items())[0]
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )
        return templates.TemplateResponse(
            request,
            "edit_setting.html",
            {
                "path": path,
                "key": key,
                "name": name,
                "what": "setting",
                "value": str(value),
                "allowed": allowed_values,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "instances":
        _, name, _ = what
        try:
            value = netlist["instances"][name].get("component", "_")
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )
        allowed = [name for name in pdk.cells if name != this_cell_name]
        return templates.TemplateResponse(
            request,
            "edit_setting.html",
            {
                "path": path,
                "key": "component",
                "name": name,
                "what": "component",
                "value": str(value),
                "allowed": {"component": natsorted(allowed)},
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "connections":
        key = what[1]
        try:
            value = netlist["connections"].get(key, "_")

            given_ports = [k for k in [key, value] if k != "_"]
            free_ports = _get_free_ports(netlist) + given_ports
            if len(free_ports) < 2:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {
                        "error": f"Not enough free ports to make a connection with. free_ports: {', '.join(free_ports)}"
                    },
                )

            if key == "_":
                key = free_ports[0]
                value = free_ports[1]
            given_ports = [key, value]
            allowed = given_ports + [k for k in free_ports if k not in given_ports]
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )

        return templates.TemplateResponse(
            request,
            "edit_connection.html",
            {
                "path": path,
                "key": key,
                "name": "connection",
                "what": "connection",
                "value": str(value),
                "allowed": allowed,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "routes" and len(what) == 2:
        _, name = what
        return templates.TemplateResponse(
            request,
            "edit_name.html",
            {
                "path": path,
                "name": name,
                "what": "routes",
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )
    elif what[0] == "routes" and len(what) == 3 and what[-1] == "routing_strategy":
        _, name, _ = what
        value = netlist["routes"][name].get("routing_strategy", "_")
        return templates.TemplateResponse(
            request,
            "edit_setting.html",
            {
                "path": path,
                "key": "routing_strategy",
                "name": name,
                "what": "routing_strategy",
                "value": str(value),
                "allowed": {"routing_strategy": _get_routing_strategies()},
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )
    elif what[0] == "routes" and what[2] == "links":
        _, name, _, key = what
        try:
            value = netlist["routes"][name]["links"].get(key, "_")
            given_ports = [k for k in [key, value] if k != "_"]
            free_ports = _get_free_ports(netlist) + given_ports
            if len(free_ports) < 2:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {
                        "error": f"Not enough free ports to make a link with. free_ports: {', '.join(free_ports)}"
                    },
                )
            if key == "_":
                key = free_ports[0]
                value = free_ports[1]
            given_ports = [key, value]
            allowed = given_ports + [k for k in free_ports if k not in given_ports]
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )

        return templates.TemplateResponse(
            request,
            "edit_connection.html",
            {
                "path": path,
                "key": key,
                "name": name,
                "what": "link",
                "value": str(value),
                "allowed": allowed,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "routes" and what[2] == "settings":
        try:
            _, name, _, key = what
            routes = netlist["routes"] = netlist.get("routes", {})
            route = routes[name] = routes.get(name, {})
            settings = route["settings"] = route.get("settings", {})
            value = settings.get(key, "_")
            pdk = get_active_pdk()
            routing_strategies = pdk.routing_strategies or {}
            if not routing_strategies:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {"error": "No routing strategies in PDK."},
                )
            default_routing_strategy = list(routing_strategies)[0]
            routing_strategy = route["routing_strategy"] = route.get(
                "routing_strategy", default_routing_strategy
            )
            allowed_values = _get_allowed_instance_settings(
                routing_strategies[routing_strategy]
            )
            given_values = [k for k in settings if k != "_"]
            allowed_values = {
                k: v
                for k, v in allowed_values.items()
                if (k == key or k not in given_values) and k != "_"
            }
            if len(allowed_values) < 1:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {"error": "no more settings for this routing strategy."},
                )
            if value == "_":
                key, value = list(allowed_values.items())[0]
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )
        return templates.TemplateResponse(
            request,
            "edit_setting.html",
            {
                "path": path,
                "key": key,
                "name": name,
                "what": "routing_setting",
                "value": "",
                "allowed": allowed_values,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "ports":
        key = what[1]
        try:
            value = netlist["ports"].get(key, "_")

            given_ports = [k for k in [value] if k != "_"]
            free_ports = _get_free_ports(netlist) + given_ports
            if len(free_ports) < 1:
                return templates.TemplateResponse(
                    request, "error.html", {"error": "No more free ports."}
                )
            if value == "_":
                value = free_ports[0]
            given_ports = [value]
            allowed = given_ports + [k for k in free_ports if k not in given_ports]
        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )

        return templates.TemplateResponse(
            request,
            "edit_port.html",
            {
                "path": path,
                "key": key,
                "name": "port",
                "what": "port",
                "value": str(value),
                "allowed": allowed,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )

    elif what[0] == "placements" and len(what) == 2:
        _, name = what
        allowed = list(netlist["instances"])
        return templates.TemplateResponse(
            request,
            "edit_name.html",
            {
                "path": path,
                "name": name,
                "what": "placements",
                "list": list,
                "isinstance": isinstance,
                "added": added,
                "allowed": allowed,
            },
        )

    elif what[0] == "placements":
        _, name, key = what
        try:
            value = netlist["placements"][name].get(key, "_")

            allowed_values = _get_allowed_placement_settings(netlist)
            given_values = list(netlist["placements"][name])
            allowed_values = {
                k: v
                for k, v in allowed_values.items()
                if k == key or k not in given_values
            }

            if len(allowed_values) < 1:
                return templates.TemplateResponse(
                    request,
                    "error.html",
                    {"error": "no more placement settings for this component."},
                )

        except Exception as e:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"{e.__class__.__name__}: {e}"}
            )

        return templates.TemplateResponse(
            request,
            "edit_setting.html",
            {
                "path": path,
                "key": key,
                "name": name,
                "what": "placement",
                "value": str(value),
                "allowed": allowed_values,
                "list": list,
                "isinstance": isinstance,
                "added": added,
            },
        )


@app.get("/yaml/accept")
def accept(
    request: Request,
    path: str = "",
    name: str = "",
    what: str = "",
    key: str = "",
    value: str = "",
    prev_key: str = "",
):
    activate_pdk_by_name(PDK)
    if path == "" or name == "" or what == "" or key == "" or value == "":
        return Response(status_code=404)
    value = yaml.safe_load(f"value: {value}")["value"]

    netlist = _load_netlist(path)
    if isinstance(netlist, Response):
        return netlist

    if what == "instances":
        instance = netlist["instances"].pop(
            name, {"component": "straight", "settings": {}}
        )
        if key in netlist["instances"]:
            error = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"An instance named '{key}' already exists."},
            ).body
            if name != "_":
                instance = templates.TemplateResponse(
                    request,
                    "instance.html",
                    {"instance": instance, "name": name, "path": path},
                ).body
            else:
                instance = b""
            return HTMLResponse(error + instance)  # type: ignore

        netlist["instances"][key] = instance
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "instance.html",
            {"instance": instance, "name": key, "path": path},
        )

    elif what == "setting":
        settings = netlist["instances"][name]["settings"]
        prev_value = settings.get(prev_key, "_")
        if prev_key in settings:
            del settings[prev_key]
        if prev_key != "_":
            prev = templates.TemplateResponse(
                request,
                "setting.html",
                {
                    "path": path,
                    "name": name,
                    "k": prev_key,
                    "v": prev_value,
                    "which": "instances",
                },
            ).body
        else:
            prev = b""
        if key in settings:
            this = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"A setting named '{key}' already exists."},
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        settings[key] = value
        component_name = netlist["instances"][name].get("component", "")
        if not component_name:
            this = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"Can't edit settings. Choose a component first."},
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        pdk = get_active_pdk()
        if component_name not in pdk.cells:
            this = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"No component named '{component_name}' in pdk."},
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        try:
            pdk.cells[component_name](**settings)
        except Exception as e:
            templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"{e.__class__.__name__}: {e}"},
            ).body
            return HTMLResponse(this + prev)  # type: ignore

        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "setting.html",
            {"path": path, "name": name, "k": key, "v": value, "which": "instances"},
        )
    elif what == "routing_setting":
        settings = netlist["routes"][name]["settings"]
        prev_value = settings.get(prev_key, "_")
        if prev_key in settings:
            del settings[prev_key]
        if prev_key != "_":
            prev = templates.TemplateResponse(
                request,
                "setting.html",
                {
                    "path": path,
                    "name": name,
                    "k": prev_key,
                    "v": prev_value,
                    "which": "routes",
                },
            ).body
        else:
            prev = b""
        this = templates.TemplateResponse(
            request,
            "setting.html",
            {"path": path, "name": name, "k": key, "v": value, "which": "routes"},
        ).body
        if key in settings:
            this = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"A setting named '{key}' already exists."},
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        settings[key] = value
        routing_strategy_name = netlist["routes"][name].get("routing_strategy", "")
        if not routing_strategy_name:
            this = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"Can't edit settings. Choose a routing_strategy first."},
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        pdk = get_active_pdk()
        if routing_strategy_name not in (pdk.routing_strategies or {}):
            this = templates.TemplateResponse(
                request,
                "error.html",
                {
                    "error": f"No routing strategy named '{routing_strategy_name}' in pdk."
                },
            ).body
            return HTMLResponse(this + prev)  # type: ignore
        try:
            (pdk.routing_strategies or {})[routing_strategy_name](**settings)
        except Exception as e:
            warning = templates.TemplateResponse(
                request,
                "warning.html",
                {"error": f"{e.__class__.__name__}: {e}"},
            ).body
            return HTMLResponse(warning + this)  # type: ignore
        _save_netlist(netlist, path)
        return HTMLResponse(this)
    elif what == "component":
        settings = netlist["instances"][name]
        settings["component"] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request, "component.html", {"path": path, "name": name, "component": value}
        )
    elif what == "routing_strategy":
        route = netlist["routes"][name]
        route["routing_strategy"] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "routing_strategy.html",
            {"path": path, "name": name, "route": route},
        )

    elif what == "connection":
        connections = netlist["connections"]
        if prev_key in connections:
            del connections[prev_key]
        connected_ports = _get_connected_ports(netlist)
        if key in connected_ports:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"Port {key} already connected."}
            )
        if value in connected_ports:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"Port {value} already connected."}
            )
        connections[key] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request, "connection.html", {"path": path, "p_in": key, "p_out": value}
        )

    elif what == "routes":
        route = netlist["routes"].pop(name, {"links": {}})
        if key in netlist["routes"]:
            error = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"A route/bundle named '{key}' already exists."},
            ).body
            if name != "_":
                route = templates.TemplateResponse(
                    request,
                    "route.html",
                    {"route": route, "name": name, "path": path},
                ).body
            else:
                route = b""
            return HTMLResponse(error + route)  # type: ignore
        netlist["routes"][key] = route
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "route.html",
            {"route": route, "name": key, "path": path},
        )

    elif what == "link":
        links = netlist["routes"][name]["links"]
        if prev_key in links:
            del links[prev_key]
        connected_ports = _get_connected_ports(netlist)
        if key in connected_ports:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"Port {key} already connected."}
            )
        if value in connected_ports:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"Port {value} already connected."}
            )
        links[key] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "link.html",
            {"path": path, "name": name, "p_in": key, "p_out": value},
        )

    elif what == "port":
        ports = netlist["ports"]
        if prev_key in ports:
            del ports[prev_key]
        connected_ports = _get_connected_ports(netlist)
        if key in ports:
            return templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"An output port with name '{key}' already exists"},
            )
        if value in connected_ports:
            return templates.TemplateResponse(
                request, "error.html", {"error": f"Port {value} already connected."}
            )
        ports[key] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request, "port.html", {"path": path, "p": key, "ip": value}
        )

    if what == "placements":
        placement = netlist["placements"].pop(name, {})

        error = ""
        if key in netlist["placements"]:
            error = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"An instance named '{key}' already exists."},
            ).body
        elif key not in netlist["instances"]:
            error = templates.TemplateResponse(
                request,
                "error.html",
                {"error": f"Can't create placement. Instance '{key}' does not exist."},
            ).body

        if error:
            if name != "_":
                placement = templates.TemplateResponse(
                    request,
                    "placement.html",
                    {"placement": placement, "name": name, "path": path},
                ).body
            else:
                placement = b""
            return HTMLResponse(error + placement)  # type: ignore

        netlist["placements"][key] = placement
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "placement.html",
            {"placement": placement, "name": key, "path": path},
        )

    elif what == "placement":
        placements = netlist["placements"][name]
        if prev_key in placements:
            del placements[prev_key]
        placements[key] = value
        _save_netlist(netlist, path)
        return templates.TemplateResponse(
            request,
            "placementsetting.html",
            {"path": path, "name": name, "k": key, "v": value, "which": "placements"},
        )

    return Response(status_code=404)


def _save_netlist(netlist, path):
    comment = netlist.pop("_comment", None)
    netlist = ensure_netlist_order(netlist)
    yaml_str = yaml.safe_dump(netlist, sort_keys=False)
    if comment:
        yaml_str = f"{comment}\n{yaml_str}"
    open(path, "w").write(yaml_str)


def _load_netlist(path) -> dict | Response:
    path = os.path.abspath(path)

    if not path.endswith(".pic.yml"):
        return PlainTextResponse(
            f"Path {path} is not a .pic.yml file.", status_code=422
        )
    name = os.path.basename(path)[:-8]

    yaml_str = open(path).read()
    yaml_lines = yaml_str.split("\n")
    if yaml_lines[0].startswith("#"):
        comment = yaml_lines[0].strip()
    else:
        comment = None

    try:
        netlist = yaml.safe_load(yaml_str)
    except FileNotFoundError:
        return PlainTextResponse(f"Path {path} not found.", status_code=404)

    try:
        netlist = patch_netlist(name, netlist)
    except Exception:
        pass

    netlist["instances"] = {
        k: netlist["instances"][k] for k in natsorted(netlist["instances"])
    }

    if comment:
        netlist["_comment"] = comment
    return netlist


def _get_allowed_instance_settings(pcell):
    pdk = get_active_pdk()
    types = {}
    for k, p in inspect.signature(pcell).parameters.items():
        if p.annotation is inspect._empty:
            if p.default is inspect._empty:
                types[k] = "str"
            else:
                types[k] = getattr(p.default, "__class__", str).__name__
        else:
            types[k] = getattr(p.annotation, "__name__", str(p.annotation))
        types[k] = types[k].replace("| None", "").strip()
        if "CrossSection" in types[k]:
            types[k] = [xs for xs in pdk.cross_sections if xs != "cross_section"]
        elif "Component" in types[k]:
            types[k] = list(pdk.cells)
    if "kwargs" in types:
        del types["kwargs"]
    return types


def _get_allowed_placement_settings(netlist):
    ports = _get_ports(netlist)
    allowed = {
        "x": "str",
        "y": "str",
        "xmin": "str",
        "ymin": "str",
        "xmax": "str",
        "ymax": "str",
        "dx": "str",
        "dy": "str",
        "port": ports,
        "rotation": "str",
        "mirror": "bool",
    }
    return allowed


def _get_ports(netlist):
    all_ports = set()
    for name, inst in netlist["instances"].items():
        if isinstance(inst, str):
            component = inst
            settings = {}
        else:
            component = inst.get("component", "")
            settings = inst.get("settings", {})
        pdk = get_active_pdk()
        func = pdk.cells.get(component)
        if not func:
            continue
        try:
            comp = func(**settings)
        except Exception:
            try:
                comp = func()
            except Exception:
                comp = None
        if comp is None:
            continue
        ports = [p.name for p in comp.ports]
        for port in ports:
            all_ports.add(f"{name},{port}")
    return natsorted(all_ports)


def _get_connected_ports(netlist):
    given_ports = set()
    for k, v in netlist["connections"].items():
        given_ports.add(k)
        given_ports.add(v)
    for v in netlist["ports"].values():
        given_ports.add(v)
    for bundle in netlist["routes"].values():
        links = bundle.get("links", {})
        for k, v in links.items():
            given_ports.add(k)
            given_ports.add(v)
    return natsorted(given_ports)


def _get_free_ports(netlist):
    ports = _get_ports(netlist)
    connected_ports = _get_connected_ports(netlist)
    ports = [p for p in ports if p not in connected_ports]
    return ports


def _get_routing_strategies():
    pdk = get_active_pdk()
    return natsorted(pdk.routing_strategies or [])
