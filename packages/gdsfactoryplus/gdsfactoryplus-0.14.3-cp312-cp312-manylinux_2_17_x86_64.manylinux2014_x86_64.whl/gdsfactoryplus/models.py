from typing import Any, Literal

from pydantic import BaseModel, Field
from sax.netlist import RecursiveNetlist as RecursiveNetlist


class ShowMessage(BaseModel):
    what: Literal["show"] = "show"  # do not override
    mime: (
        Literal[
            "html",
            "json",
            "yaml",
            "plain",
            "base64",
            "png",
            "gds",
            "netlist",
            "dict",
            "error",
        ]
        | None
    ) = None
    content: str


class ErrorMessage(BaseModel):
    what: Literal["error"] = "error"  # do not override
    category: str
    message: str
    path: str


Message = ShowMessage | ErrorMessage


class SimulationConfig(BaseModel):
    """Data model for simulation configuration."""

    pdk: str
    wl0: float
    wl1: float
    nwl: int = 300
    op: str = "none"
    port_in: str = ""
    settings: dict[str, Any] = Field(default_factory=dict)


class SimulationData(BaseModel):
    """Data model for simulation."""

    netlist: RecursiveNetlist
    config: SimulationConfig
