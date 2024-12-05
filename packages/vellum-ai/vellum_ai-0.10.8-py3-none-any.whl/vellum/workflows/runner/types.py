"""Only intenral types and enums for WorkflowRunner should be defined in this module."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from vellum.workflows.types.generics import StateType

if TYPE_CHECKING:
    from vellum.workflows.events import NodeEvent
    from vellum.workflows.nodes.bases import BaseNode


@dataclass(frozen=True)
class WorkItemEvent(Generic[StateType]):
    node: "BaseNode[StateType]"
    event: "NodeEvent"
