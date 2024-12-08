from typing import Literal

from pydantic import validate_call
from sax.netlist import RecursiveNetlist as RecursiveNetlist

from .core._simulate import _circuit, _circuit_df, _circuit_plot
from .settings import SETTINGS as s


@validate_call
def circuit(
    netlist: RecursiveNetlist,
    pdk: str = s.pdk.name,
    host: str = s.sim.host,
    api_key: str = s.api.key,
):
    """Create a sax circuit with dosax backend."""
    return _circuit(netlist, pdk, host, api_key)


@validate_call
def circuit_df(
    netlist: RecursiveNetlist,
    pdk: str = s.pdk.name,
    host: str = s.sim.host,
    api_key: str = s.api.key,
):
    """Create a sax circuit with dosax backend."""
    return _circuit_df(netlist, pdk, host, api_key)


@validate_call
def circuit_plot(
    netlist: RecursiveNetlist,
    pdk: str = s.pdk.name,
    host: str = s.sim.host,
    api_key: str = s.api.key,
    op: str = "dB",
    port_in: str = "",
    which: Literal["html", "json"] = "html",
):
    """Create a sax circuit with dosax backend."""
    return _circuit_plot(
        netlist=netlist,
        pdk=pdk,
        host=host,
        api_key=api_key,
        op=op,
        port_in=port_in,
        which=which,
    )
