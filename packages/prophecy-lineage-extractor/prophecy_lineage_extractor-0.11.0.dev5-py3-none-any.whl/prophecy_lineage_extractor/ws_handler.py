import logging
import time

import pandas as pd
import sqlparse

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import (
    PIPELINE_ID,
    DB_COL,
    TABLE_COL,
    COLNAME_COL,
    UPSTREAM_TRANSFORMATION_COL,
    LONG_SLEEP_TIME,
    SLEEP_TIME,
    CATALOG_COL,
)
from prophecy_lineage_extractor.graphql import get_dataset_info_from_id
from prophecy_lineage_extractor.utils import (
    get_output_path,
    safe_env_variable,
    append_to_csv,
    format_sql,
)


def _get_dataset_from_summary_view(json_msg):
    logging.info("viewType is summaryView, getting datasets")
    # Step 2: Extract all datasets from `processes`
    processes = (
        json_msg.get("params", {})
        .get("lineage", {})
        .get("graph", {})
        .get("processes", {})
    )
    # Filter out all entries with component "Dataset" and collect their names
    datasets = [
        info["id"] for info in processes.values() if info.get("component") == "Dataset"
    ]
    logging.info(f"All datasets Total {len(datasets)}:\n {datasets}")
    return datasets


def _get_lineage_from_detailed_view(data):
    logging.info("viewType is detailedDatasetView, getting lineage")
    # Access columns data
    columns = data.get("value", {}).get("dataset", {}).get("columns", [])
    datasetId = data.get("value", {}).get("dataset", {}).get("id", "NA")
    # Extract lineage information for each column
    # Prepare data for DataFrame
    lineage_data = []

    for column in columns:
        column_name = column.get("name")
        # to at least add one row for every column
        # if upstream transformations are empty add self as passthrough column
        catalog_name, database_name, table_name = get_dataset_info_from_id(datasetId)
        if len(column.get("upstreamTransformations", [])) == 0:
            lineage_data.append(
                {
                    # "dataset_id": str(datasetId).split("/")[2],
                    CATALOG_COL: catalog_name,
                    DB_COL: database_name,
                    TABLE_COL: table_name,
                    COLNAME_COL: column_name,
                    UPSTREAM_TRANSFORMATION_COL: column_name,
                    # "downstream_transformation": ""
                }
            )

        # Upstream transformations
        for upstream in column.get("upstreamTransformations", []):
            # as default pass through value
            pipeline_id = upstream.get("pipeline", {}).get("id", "Unknown")
            if pipeline_id != safe_env_variable(PIPELINE_ID):
                logging.info(
                    f"skipping transformation for column {column_name} as this belongs to different pipeline: {upstream}"
                )
                continue
            transformations = upstream.get("transformations", [])
            for transformation in transformations:
                process_name = transformation.get("processName", "Unknown")
                # TODO: get expression language from project metadata and then apply this formatting
                transformation_str = format_sql(
                    transformation.get("transformation", "")
                )
                # upstream_transformation = f"{process_name}: {transformation_str}"
                upstream_transformation = f"{transformation_str}"
                lineage_data.append(
                    {
                        # "dataset_id": str(datasetId).split("/")[2],
                        CATALOG_COL: catalog_name,
                        DB_COL: database_name,
                        TABLE_COL: table_name,
                        COLNAME_COL: column_name,
                        UPSTREAM_TRANSFORMATION_COL: upstream_transformation,
                        # "downstream_transformation": ""
                    }
                )

        # # Downstream transformations
        # for downstream in column.get("downstreamTransformations", []):
        #     pipeline_name = downstream.get("pipeline", {}).get("name", "Unknown")
        #     transformations = downstream.get("transformations", [])
        #     for transformation in transformations:
        #         process_name = transformation.get("processName", "Unknown")
        #         transformation_str = transformation.get("transformation", "")
        #         # downstream_transformation = f"{process_name}: {transformation_str}"
        #         downstream_transformation = f"{transformation_str}"
        #         lineage_data.append({
        #             "dataset_id": str(datasetId).split("/")[2],
        #             "column_name": column_name,
        #             "upstream_transformation": "",
        #             "downstream_transformation": downstream_transformation
        #         })

    # Create a DataFrame
    df = pd.DataFrame(lineage_data)
    # save_excel_file(df, get_output_path())
    append_to_csv(df, get_output_path(fmt="csv"))


def handle_did_open(ws, json_msg):
    logging.info("Handling didOpen")
    view_type = (
        json_msg.get("params", {})
        .get("lineage", {})
        .get("metaInfo", {})
        .get("viewType")
    )
    if view_type == "summaryView":
        datasets = _get_dataset_from_summary_view(json_msg)
        # for every datasets run and get lineage
        for dataset in datasets:
            # change active entity
            logging.info(f"running lineage fetch for dataset {dataset}")

            ws.send(messages.change_active_entity(dataset))
            time.sleep(SLEEP_TIME)
            # get lineage
            ws.send(messages.detailed_view())
            time.sleep(LONG_SLEEP_TIME)

            logging.info(f"Going back to summary view")
            ws.send(messages.summary_view())
            time.sleep(SLEEP_TIME)


def handle_did_update(ws, json_msg):
    logging.info("Handling didUpdate")
    for change in json_msg.get("params", {}).get("changes", []):
        # Check if 'viewType' is present and equals 'detailedDatasetView'
        if (
            change.get("value", {}).get("metaInfo", {}).get("viewType")
            == "detailedDatasetView"
        ):
            try:
                _get_lineage_from_detailed_view(change)
            except Exception as e:
                logging.error(e)
                ws.close()
