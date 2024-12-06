from __future__ import annotations

from collections import defaultdict
from typing import Dict, Any, Optional, Tuple, List, DefaultDict

from attr import define
from attrs import field

from fixcore.model.graph_access import Section, EdgeTypes
from fixcore.model.model import Model, ResolvedPropertyPath, ComplexKind
from fixcore.model.resolve_in_graph import GraphResolver
from fixcore.query.model import Query
from fixcore.types import Json, EdgeType
from fixcore.util import first

ancestor_merges = {
    f"ancestors.{p.to_path[1]}" for r in GraphResolver.to_resolve for p in r.resolve if p.to_path[0] == "ancestors"
}


@define
class QueryModel:
    query: Query
    model: Model
    env: Dict[str, Any] = {}

    def is_set(self, name: str) -> bool:
        if value := self.env.get(name):
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ["1", "true", "yes", "y"]
        return False

    def __prop(self, path: str) -> Tuple[str, Optional[str]]:
        merge_name = first(lambda name: path.startswith(name + "."), self.query.merge_names) or first(
            lambda name: path.startswith(name + "."), ancestor_merges
        )
        # remove merge_name and section part (if existent) from the local_path
        lookup = Section.without_section(path[len(merge_name) + 1 :] if merge_name else path)  # noqa: E203
        return lookup, merge_name

    def prop_kind(self, path: str) -> Tuple[ResolvedPropertyPath, Optional[str]]:  # prop, merge_name
        lookup, merge_name = self.__prop(path)
        resolved = self.model.property_by_path(lookup)
        return resolved, merge_name

    def owners(self, path: str) -> List[ComplexKind]:
        lookup, _ = self.__prop(path)
        return self.model.owners_by_path(lookup)


@define(repr=True, eq=True)
class GraphUpdate:
    nodes_created: int = 0
    nodes_updated: int = 0
    nodes_deleted: int = 0
    edges_created: int = 0
    edges_updated: int = 0
    edges_deleted: int = 0

    def all_changes(self) -> int:
        return (
            self.nodes_created
            + self.nodes_updated
            + self.nodes_deleted
            + self.edges_created
            + self.edges_updated
            + self.edges_deleted
        )

    def __add__(self, other: GraphUpdate) -> GraphUpdate:
        return GraphUpdate(
            self.nodes_created + other.nodes_created,
            self.nodes_updated + other.nodes_updated,
            self.nodes_deleted + other.nodes_deleted,
            self.edges_created + other.edges_created,
            self.edges_updated + other.edges_updated,
            self.edges_deleted + other.edges_deleted,
        )


@define
class GraphChange:
    node_inserts: List[Json] = field(factory=list)
    node_updates: List[Json] = field(factory=list)
    node_deletes: List[Json] = field(factory=list)
    edge_inserts: DefaultDict[EdgeType, List[Json]] = field(factory=lambda: defaultdict(list))
    edge_updates: DefaultDict[EdgeType, List[Json]] = field(factory=lambda: defaultdict(list))
    edge_deletes: DefaultDict[EdgeType, List[Json]] = field(factory=lambda: defaultdict(list))

    def to_update(self) -> GraphUpdate:
        return GraphUpdate(
            len(self.node_inserts),
            len(self.node_updates),
            len(self.node_deletes),
            sum(len(edges) for edges in self.edge_inserts.values()),
            sum(len(edges) for edges in self.edge_updates.values()),
            sum(len(edges) for edges in self.edge_deletes.values()),
        )

    def change_count(self) -> int:
        return self.to_update().all_changes()

    def __add__(self, other: GraphChange) -> GraphChange:
        update = GraphChange()
        # insert
        update.node_inserts.extend(self.node_inserts)
        update.node_inserts.extend(other.node_inserts)
        # update
        update.node_updates.extend(self.node_updates)
        update.node_updates.extend(other.node_updates)
        # delete
        update.node_deletes.extend(self.node_deletes)
        update.node_deletes.extend(other.node_deletes)
        for edge_type in EdgeTypes.all:
            # insert
            update.edge_inserts[edge_type].extend(self.edge_inserts[edge_type])
            update.edge_inserts[edge_type].extend(other.edge_inserts[edge_type])
            # update
            update.edge_updates[edge_type].extend(self.edge_updates[edge_type])
            update.edge_updates[edge_type].extend(other.edge_updates[edge_type])
            # delete
            update.edge_deletes[edge_type].extend(self.edge_deletes[edge_type])
            update.edge_deletes[edge_type].extend(other.edge_deletes[edge_type])
        return update

    def clear(self) -> None:
        self.node_inserts.clear()
        self.node_updates.clear()
        self.node_deletes.clear()
        self.edge_inserts.clear()
        self.edge_updates.clear()
        self.edge_deletes.clear()
