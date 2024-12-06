import logging
from typing import List, Dict, Tuple, Union, Optional

from rich.progress import track

from bigeye_sdk.model.enums import MatchType
from bigeye_sdk.functions.search_and_match_functions import wildcard_search, fuzzy_match
from bigeye_sdk.functions.table_functions import fully_qualified_table_to_elements
from bigeye_sdk.generated.com.bigeye.models.generated import (
    Table,
    Integration,
    TableauWorkbook,
    Source,
    Schema,
    Delta,
    TableColumn,
    DataNodeType,
    DataNode,
    LineageRelationship,
    LineageNavigationNodeV2Response
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.model.lineage_facade import SimpleLineageConfigurationFile, SimpleLineageEdgeRequest, \
    LineageColumnOverride, SimpleEtlTask
from bigeye_sdk.model.protobuf_enum_facade import SimpleDataNodeType

log = get_logger(__file__)


class LineageController:
    def __init__(self, client: DatawatchClient):
        self.client = client
        self.sources_by_name_ix: Dict[str, Source] = self.client.get_sources_by_name()
        self.edge_requests: List[SimpleLineageEdgeRequest] = []
        self.existing_relations: Dict[int, List[int]] = {}
        self.custom_nodes_ix_by_name: Dict[str, int] = {}

    def get_table_by_name(self, entity_name: str) -> Table:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = self.client.get_tables(
            schema=[schema], table_name=[entity_name]
        ).tables[0]
        return table

    def get_tableau_workbook_by_name(
        self, entity_name: str, integration_name: str
    ) -> TableauWorkbook:
        integration: Integration = [
            i for i in self.client.get_integrations() if i.name == integration_name
        ][0]
        workbook = [
            w
            for w in self.client.get_integration_entities(integration_id=integration.id)
            if w.name == entity_name
        ][0]
        return workbook

    def create_node_by_name(self, entity_name: str, integration_name: str) -> DataNode:
        """Create a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            log.info(f"Creating lineage node for table: {entity_name}")
            entity_id = table.id
            node_type = SimpleDataNodeType.TABLE.to_datawatch_object()

        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            log.info(f"Creating lineage node for entity: {workbook.name}")
            entity_id = workbook.id
            node_type = SimpleDataNodeType.TABLEAU.to_datawatch_object()

        return self.client.create_data_node(
            node_type=node_type, node_entity_id=entity_id
        )

    def delete_node_by_name(self, entity_name: str, integration_name: str):
        """Delete a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting lineage node for table: {table.name}")
        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(f"Deleting lineage node for table: {workbook.name}")

        self.client.delete_data_node(data_node_id=node_id)

    def create_relation_from_name(
        self, upstream_table_name: str, downstream_table_name: str
    ) -> LineageRelationship:
        """Create a lineage relationship for 2 entities"""
        warehouse, u_schema, u_table_name = fully_qualified_table_to_elements(
            upstream_table_name
        )
        warehouse, d_schema, d_table_name = fully_qualified_table_to_elements(
            downstream_table_name
        )

        upstream: Table = self.client.get_tables(
            schema=[u_schema], table_name=[u_table_name]
        ).tables[0]
        downstream: Table = self.client.get_tables(
            schema=[d_schema], table_name=[d_table_name]
        ).tables[0]

        log.info(
            f"Creating relationship from {upstream_table_name} to {downstream_table_name}"
        )

        return self.client.create_table_lineage_relationship(
            upstream_data_node_id=upstream.data_node_id,
            downstream_data_node_id=downstream.data_node_id,
        )

    def delete_relationships_by_name(self, entity_name: str, integration_name: str):
        """Deletes all relationships for a node by name."""
        if integration_name:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(
                f"Deleting all lineage relationships for workbook: {workbook.name}"
            )
        else:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting all lineage relationships for table: {table.name}")

        self.client.delete_lineage_relationship_for_node(data_node_id=node_id)

    def get_schemas_from_selector(self, selector: str) -> List[Schema]:
        # Split selectors into patterns
        source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(selector)

        # Only take source ids that match pattern
        source_ids = [
            source.id
            for source_name, source in self.sources_by_name_ix.items()
            if source_name
            in wildcard_search(search_string=source_pattern, content=[source_name])
        ]

        # Only take schemas from those sources that match pattern
        schemas_by_name_ix: Dict[str, Schema] = {
            s.name: s for s in self.client.get_schemas(warehouse_id=source_ids).schemas
        }
        schemas = [
            schema
            for schema_name, schema in schemas_by_name_ix.items()
            if schema_name
            in wildcard_search(search_string=schema_pattern, content=[schema_name])
        ]

        # Get list of existing relations for schemas.
        self._get_existing_relations_for_schema(schemas)

        return schemas

    def get_tables_from_selector(self, selector: str) -> List[Table]:
        # Split selectors into patterns
        source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(selector)
        # Get schemas
        schema_ids = [schema.id for schema in self.get_schemas_from_selector(selector)]

        # Only take tables from those schemas that match pattern
        if not schema_ids:
            log.warning(f"No schemas found for given selector {selector}.")
            return []

        tables_by_id_ix: Dict[str, Table] = {
            t.id: t for t in self.client.get_tables_post(
                schema_ids=schema_ids,
                ignore_fields=False,
                include_data_node_ids=True
            ).tables
        }

        tables = [
            table
            for table_id, table in tables_by_id_ix.items()
            if table.name
            in wildcard_search(search_string=table_pattern, content=[table.name])
        ]

        return tables

    @staticmethod
    def infer_relationships_from_lists(
            upstream,
            downstream,
            task: Optional[SimpleEtlTask] = None,
            match_type: MatchType = MatchType.STRICT
    ):
        matching = []
        if match_type == MatchType.STRICT:
            for u in upstream:
                matching_downstream = [d for d in downstream if d.name.lower() == u.name.lower()]
                if matching_downstream:
                    for md in matching_downstream:
                        matching.append((u, md, task))
        elif match_type == MatchType.FUZZY:
            for u in upstream:
                matching_downstream = fuzzy_match(
                    search_string=u.name.lower(),
                    contents=[d.name.lower() for d in downstream],
                    min_match_score=95,
                )
                if matching_downstream:
                    for match in matching_downstream:
                        md_table = [md for md in downstream if md.name.lower() == match[1]]
                        for mdt in md_table:
                            matching.append((u, mdt, task))
        return matching

    def create_edges(self,
                     upstream: Union[Schema, Table, TableColumn, SimpleEtlTask],
                     downstream: Union[Schema, Table, TableColumn, SimpleEtlTask],
                     node_type: DataNodeType):
        if upstream.data_node_id and downstream.data_node_id:
            self.client.create_lineage_edge(upstream_data_node_id=upstream.data_node_id,
                                            downstream_data_node_id=downstream.data_node_id)
        elif upstream.data_node_id and not downstream.data_node_id:
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=upstream.data_node_id,
                                            downstream_data_node_id=d_node.id)
        elif not upstream.data_node_id and downstream.data_node_id:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=u_node.id,
                                            downstream_data_node_id=downstream.data_node_id)
        else:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=u_node.id,
                                            downstream_data_node_id=d_node.id)

    def create_relations_from_deltas(self, deltas: List[Delta]):
        for d in deltas:
            target_ids = [dc.target_table_id for dc in d.comparison_table_configurations]

            if len(target_ids) > 1:
                log.warning(f'We are unable to determine the proper lineage for deltas with more than 1 target. '
                            f'Please review the `bigeye lineage infer-relations` command for an alternative option.')
            else:
                source_table = self.client.get_tables(ids=[d.source_table.id]).tables[0]
                target_table = self.client.get_tables(ids=target_ids).tables[0]
                try:
                    self.infer_column_level_lineage_from_tables(tables=[(source_table, target_table, None)])
                except Exception as e:
                    log.warning(f'Failed to create lineage relationship between upstream table: {source_table.name} '
                                f'and downstream table: {target_table.name}. Exception: {e}')

    def get_matching_tables_from_selectors(
            self,
            upstream_selector: str,
            downstream_selector: str,
            match_type: MatchType = MatchType.STRICT
    ) -> List[Tuple[Table, Table, SimpleEtlTask]]:
        upstream_tables = self.get_tables_from_selector(upstream_selector)
        downstream_tables = self.get_tables_from_selector(downstream_selector)
        matching_tables: List[Tuple[Table, Table, SimpleEtlTask]] = self.infer_relationships_from_lists(
            upstream=upstream_tables,
            downstream=downstream_tables,
            match_type=match_type
        )
        return matching_tables

    def _search_custom_nodes(self, etl_task: SimpleEtlTask) -> SimpleEtlTask:
        search_results = self.client.search_lineage(etl_task.name).results
        matching_result = next(
            (r for r in search_results if r.node_type == etl_task.node_type and r.node_name == etl_task.name),
            None
        )
        if matching_result:
            etl_task.data_node_id = matching_result.id

        return etl_task

    def _get_or_set_custom_node(self, etl_task: SimpleEtlTask) -> SimpleEtlTask:
        """Get the data node id of a custom node, if not available then create one and
        return custom ask including node id."""
        node_id = self.custom_nodes_ix_by_name.get(etl_task.name, None)

        if node_id:
            etl_task.data_node_id = node_id
        else:
            etl_task = self._search_custom_nodes(etl_task=etl_task)
            # if task does not exist yet, then create new custom node and assign the data node id
            if not etl_task.data_node_id:
                new_task = self.client.create_lineage_node(
                    node_name=etl_task.name,
                    node_container_name=etl_task.container_name,
                    node_type=etl_task.node_type
                )
                etl_task.data_node_id = new_task.id
                self.custom_nodes_ix_by_name[etl_task.name] = new_task.id

        return etl_task

    def process_all_edge_requests(self, purge_lineage: bool = False):
        count_successful_relations = 0
        count_skipped_relations = 0
        count_failed_relations = 0
        count_deleted_relations = 0

        loading_text = "Purging Lineage..." if purge_lineage else "Generating Lineage..."

        logging.disable(level=logging.INFO)
        for r in track(self.edge_requests, description=loading_text):
            try:

                if purge_lineage:
                    "Purging lineage"
                    # TODO update once this is implemented, this current method will deletes containment relationships
                    # https://linear.app/torodata/issue/ONE-2510/[feature-request]-delete-all-relationships-for-a-node-id
                    self.client.delete_lineage_relationship_for_node(data_node_id=r.upstream.data_node_id)
                    count_deleted_relations += 1
                elif not r.etl_task:
                    existing_relations = self.existing_relations.get(r.upstream.data_node_id, None)
                    if existing_relations is None or r.downstream.data_node_id not in existing_relations:
                        self.create_edges(
                            upstream=r.upstream,
                            downstream=r.downstream,
                            node_type=r.node_type
                        )
                        count_successful_relations += 1
                    else:
                        "Skipping request because the relationship already exists."
                        count_skipped_relations += 1
                elif r.etl_task:
                    task = self._get_or_set_custom_node(etl_task=r.etl_task)
                    source_to_etl_deps = self.existing_relations.get(r.upstream.data_node_id, None)
                    etl_downstream_deps = self.existing_relations.get(task.data_node_id, None)

                    if source_to_etl_deps is None or task.data_node_id not in source_to_etl_deps:
                        self.create_edges(
                            upstream=r.upstream,
                            downstream=task,
                            node_type=r.node_type
                        )
                        count_successful_relations += 1
                    else:
                        "Skipping request because the relationship already exists."
                        count_skipped_relations += 1

                    if etl_downstream_deps is None or r.downstream.data_node_id not in etl_downstream_deps:
                        self.create_edges(
                            upstream=task,
                            downstream=r.downstream,
                            node_type=r.node_type
                        )
                        count_successful_relations += 1
                    else:
                        "Skipping request because the relationship already exists."
                        count_skipped_relations += 1
                else:
                    "Skipping request because the relationship already exists."
                    count_skipped_relations += 1
            except Exception as e:
                log.error(
                    f"Failed to create relationship between upstream {r.node_type.name}: {r.upstream.name} and "
                    f"downstream {r.node_type.name}: {r.downstream.name}. Exception {e}"
                )
                count_failed_relations += 1

        # Delete any custom nodes
        if purge_lineage:
            for name, node_id in self.custom_nodes_ix_by_name.items():
                self.client.delete_lineage_node(node_id=node_id)

        logging.disable(level=logging.NOTSET)

        log.info(
            f"\n------------LINEAGE REPORT--------------"
            f"\nCreated {count_successful_relations} edges."
            f"\nSkipped {count_skipped_relations} edges. "
            f"\nDeleted {count_deleted_relations} edges. "
            f"\nFailed {count_failed_relations} edges. "
        )

    def _get_existing_relations_for_schema(self, schemas: List[Schema]) -> None:
        """Get the existing relations for a schema. This is done at the top level to limit the number of requests
        that we have to make."""
        for s in schemas:
            if self.existing_relations.get(s.data_node_id, None) is None:
                downstream_nodes = self.client.get_downstream_nodes(node_id=s.data_node_id)
                for node in downstream_nodes.nodes.values():
                    # Not sure why but nodes in TableLineageV2Response is a Dict[int, dict].
                    ln_node = LineageNavigationNodeV2Response().from_dict(node)
                    self.existing_relations[ln_node.lineage_node.id] = [d.downstream_id for d in
                                                                        ln_node.downstream_edges]

    def _execute_lineage_workflow_from_selectors(self, selectors: List[str]):
        source_ids = []
        for s in selectors:
            # Split selectors into patterns
            source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(s)

            # Only take source ids that match pattern
            selector_source_ids = [
                source.id
                for source_name, source in self.sources_by_name_ix.items()
                if source_name
                in wildcard_search(search_string=source_pattern, content=[source_name])
            ]
            source_ids.extend([ssi for ssi in selector_source_ids if ssi not in source_ids])

        for sid in source_ids:
            self.client.rebuild_source(source_id=sid)

    def create_edges_from_table_names(
            self,
            upstream_table_name: str,
            downstream_table_name: str,
            etl_task_name: Optional[str] = None,
            etl_task_container: Optional[str] = "Python",
            column_overrides: Optional[List[LineageColumnOverride]] = None,
            infer_lineage: bool = True
    ):
        """Create a lineage edge for 2 entities"""
        upstream_table: Table = self.get_tables_from_selector(upstream_table_name)[0]
        downstream_table: Table = self.get_tables_from_selector(downstream_table_name)[0]

        etl_task = None
        if etl_task_name:
            etl_task = SimpleEtlTask(name=etl_task_name, container_name=etl_task_container)

        if column_overrides:
            u_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in upstream_table.columns}
            d_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in downstream_table.columns}

            for c_override in column_overrides:
                try:
                    up_column = u_columns_ix_by_name[c_override.upstream_column_name]
                    down_column = d_columns_ix_by_name[c_override.downstream_column_name]
                except KeyError as e:
                    log.warning(
                        f"No column found for provided column override. Please check spelling and try again."
                        f" Exception: {e}")
                    continue

                if up_column.data_node_id != down_column.data_node_id:
                    self.edge_requests.append(
                        SimpleLineageEdgeRequest(
                            upstream=u_columns_ix_by_name[c_override.upstream_column_name],
                            downstream=d_columns_ix_by_name[c_override.downstream_column_name],
                            node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                            etl_task=etl_task
                        )
                    )
            if infer_lineage:
                self.infer_column_level_lineage_from_tables(tables=[(upstream_table, downstream_table, etl_task)])

        elif not column_overrides and not infer_lineage:
            if upstream_table.data_node_id != downstream_table.data_node_id:
                self.edge_requests.append(
                    SimpleLineageEdgeRequest(
                        upstream=upstream_table,
                        downstream=downstream_table,
                        node_type=DataNodeType.DATA_NODE_TYPE_TABLE,
                        etl_task=etl_task
                    )
                )
                self.process_all_edge_requests()

        elif infer_lineage and not column_overrides:
            self.infer_column_level_lineage_from_tables(tables=[(upstream_table, downstream_table, etl_task)])

    def infer_column_level_lineage_from_file(
            self, lineage_configuration_file: SimpleLineageConfigurationFile, purge_lineage: bool = False
    ):
        matching_tables: List[Tuple[Table, Table, SimpleEtlTask]] = []

        for r in lineage_configuration_file.relations:
            upstream_tables: List[Table] = self.get_tables_from_selector(f'{r.upstream_schema_name}.*')
            downstream_tables: List[Table] = self.get_tables_from_selector(f'{r.downstream_schema_name}.*')

            matching_tables_by_name = self.infer_relationships_from_lists(
                upstream=upstream_tables,
                downstream=downstream_tables,
                task=r.etl_task
            )
            matching_tables.extend(matching_tables_by_name)

            # index tables by name for reference later
            upstream_tables_ix_by_name: Dict[str, Table] = {t.name: t for t in upstream_tables}
            downstream_tables_ix_by_name: Dict[str, Table] = {t.name: t for t in downstream_tables}

            if r.table_overrides is not None:
                for t_override in r.table_overrides:
                    try:
                        u_table = upstream_tables_ix_by_name[t_override.upstream_table_name]
                        d_table = downstream_tables_ix_by_name[t_override.downstream_table_name]
                    except KeyError as e:
                        log.warning(f"No table found for provided table override. Please check spelling and try again."
                                    f" Exception: {e}")
                        continue

                    u_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in u_table.columns}
                    d_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in d_table.columns}

                    # Loop through column exclusions and remove columns from tables if names match
                    if t_override.column_name_exclusions is not None:
                        for col_excl in t_override.column_name_exclusions:
                            u_columns_ix_by_name.pop(col_excl, None)
                            d_columns_ix_by_name.pop(col_excl, None)

                        u_table.columns = [col for name, col in u_columns_ix_by_name.items()]
                        d_table.columns = [col for name, col in d_columns_ix_by_name.items()]

                    # append to matching tables after removing columns
                    # and remove any existing entries if table names are the same
                    matched_by_name = (u_table, d_table, r.etl_task)
                    if matched_by_name in matching_tables:
                        matching_tables.remove(matched_by_name)
                    matching_tables.append((u_table, d_table, t_override.etl_task))

                    if t_override.column_overrides is not None:
                        for c_override in t_override.column_overrides:
                            try:
                                up_column = u_columns_ix_by_name[c_override.upstream_column_name]
                                down_column = d_columns_ix_by_name[c_override.downstream_column_name]
                            except KeyError as e:
                                log.warning(
                                    f"No column found for provided column override. Please check spelling and try again."
                                    f" Exception: {e}")
                                continue

                            if up_column.data_node_id != down_column.data_node_id:
                                self.edge_requests.append(
                                    SimpleLineageEdgeRequest(
                                        upstream=u_columns_ix_by_name[c_override.upstream_column_name],
                                        downstream=d_columns_ix_by_name[c_override.downstream_column_name],
                                        node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                                        etl_task=t_override.etl_task,
                                    )
                                )

        # INFER LINEAGE
        self.infer_column_level_lineage_from_tables(
            tables=matching_tables,
            purge_lineage=purge_lineage
        )

        # TODO remove once this is implemented
        # https://linear.app/torodata/issue/ONE-2510/[feature-request]-delete-all-relationships-for-a-node-id
        if purge_lineage:
            self._execute_lineage_workflow_from_selectors(
                selectors=[f'{r.upstream_schema_name}.*' for r in lineage_configuration_file.relations]
            )
            log.warning(f"Purging lineage currently requires the sources to be re-indexed. This may take a few minutes,"
                        f" do not try to rebuild the lineage until re-indexing process has completed.")

    def infer_column_level_lineage_from_tables(
            self,
            tables: List[Tuple[Table, Table, Optional[SimpleEtlTask]]],
            purge_lineage: bool = False
    ):
        for upstream, downstream, etl_task in tables:
            matching_columns: List[Tuple[TableColumn, TableColumn, SimpleEtlTask]] = self.infer_relationships_from_lists(
                upstream=upstream.columns, downstream=downstream.columns, task=etl_task
            )
            if not matching_columns and upstream.data_node_id != downstream.data_node_id:
                self.edge_requests.append(
                    SimpleLineageEdgeRequest(
                        upstream=upstream,
                        downstream=downstream,
                        node_type=DataNodeType.DATA_NODE_TYPE_TABLE,
                        etl_task=etl_task
                    )
                )

            for up_column, down_column, task in matching_columns:
                if up_column.data_node_id != down_column.data_node_id:
                    self.edge_requests.append(
                        SimpleLineageEdgeRequest(
                            upstream=up_column,
                            downstream=down_column,
                            node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                            etl_task=task
                        )
                    )

        self.process_all_edge_requests(purge_lineage=purge_lineage)
