__author__ = "GDSFactory"
__version__ = "0.13.1"

# patch gf.cell
from functools import wraps

import gdsfactory as gf

gf._cell = gf.cell  # type: ignore


@wraps(gf._cell)  # type: ignore
def _cell(*args, **kwargs):
    c = gf._cell(*args, **kwargs)  # type: ignore
    c.is_gf_cell = True
    return c


gf.cell = _cell


from .core.bbox import bbox as bbox
from .core.check import check_conn as check_conn
from .core.check import check_drc as check_drc
from .core.check import get as get
from .core.check import get_download_url as get_download_url
from .core.check import run as run
from .core.check import start as start
from .core.check import status as status
from .core.check import upload_input as upload_input
from .core.communication import send_message as send_message
from .core.generate_svg import generate_svg as generate_svg
from .core.generate_svg import get_svg as get_svg
from .core.netlist import ensure_netlist_order as ensure_netlist_order
from .core.netlist import get_ports as get_ports
from .core.netlist import patch_netlist as patch_netlist
from .core.netlist import (
    patch_netlist_with_connection_info as patch_netlist_with_connection_info,
)
from .core.netlist import (
    patch_netlist_with_hierarchy_info as patch_netlist_with_hierarchy_info,
)
from .core.netlist import patch_netlist_with_icon_info as patch_netlist_with_icon_info
from .core.netlist import (
    patch_netlist_with_placement_info as patch_netlist_with_placement_info,
)
from .core.netlist import patch_netlist_with_port_info as patch_netlist_with_port_info
from .core.netlist import reset_netlist_schematic_info as reset_netlist_schematic_info
from .core.netlist import try_get_ports as try_get_ports
from .core.netlist import wrap_component_in_netlist as wrap_component_in_netlist
from .core.parse_oc_spice import parse_oc_spice as parse_oc_spice
from .core.schema import get_base_schema as get_base_schema
from .core.schema import get_netlist_schema as get_netlist_schema
from .core.shared import cli_environment as cli_environment
from .core.shared import get_python_cells as get_python_cells
from .core.shared import get_yaml_cell_name as get_yaml_cell_name
from .core.shared import get_yaml_cells as get_yaml_cells
from .core.shared import get_yaml_paths as get_yaml_paths
from .core.shared import ignore_prints as ignore_prints
from .core.shared import import_pdk as import_pdk
from .core.shared import import_python_modules as import_python_modules
from .core.shared import print_to_file as print_to_file
from .core.shared import register_cells as register_cells
from .core.show import show as show
from .core.watcher import PicsWatcher as PicsWatcher
from .models import Message as Message
from .models import ShowMessage as ShowMessage
from .models import SimulationConfig as SimulationConfig
from .models import SimulationData as SimulationData
from .settings import SETTINGS as SETTINGS
from .simulate import circuit as circuit
from .simulate import circuit_df as circuit_df
from .simulate import circuit_plot as circuit_plot
