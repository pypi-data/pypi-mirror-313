import json
import logging

from prophecy_lineage_extractor.constants import PROPHECY_PAT
from prophecy_lineage_extractor.utils import get_graphql_url, safe_env_variable
import requests


def _graphql_dataset_query(dataset_id):
    # Define your query
    query = f"""
    query {{
      Dataset(uid: "{dataset_id}") {{
        _id
        name
        physicalDatasets {{
          _id
          name
          versionedAspects(aspectVers: [{{ aspect: Configuration }}]) {{
            VersionedAspectName
            VersionedAspectValue
          }}
        }}
      }}
    }}
    """
    return query


def _graphql_get_default_branch(project_id):
    query = f"""
      query GitBranchQuery($projectId: String!) {{
        Project(uid: $projectId) {{
          mainBranch
          listBranches {{
            workingBranch
            checkedOutBranches
          }}
        }}
      }}
    """
    return query


def run_graphql(query, variables=None, operation_name=None):
    # Define the GraphQL endpoint
    GRAPHQL_ENDPOINT = get_graphql_url()
    # Define the headers (if required, include authentication tokens or other headers)
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": safe_env_variable(PROPHECY_PAT),  # Prophecy PAT
    }

    # Define the payload
    payload = {
        "query": query,
        "variables": (
            variables if variables else {}
        ),  # Add variables to the payload if provided
    }

    # Add operationName to the payload if provided
    if operation_name:
        payload["operationName"] = operation_name

    return requests.post(GRAPHQL_ENDPOINT, json=payload, headers=headers)


def _graphql_checkout_branch(branch_name):
    query = f"""
    mutation checkout($projectId: String!, $branchName: String!) {{
      checkout(projectUID: $projectId, branchName: $branchName) {{
        name
      }}
    }}
    """
    return query


def _checkout_branch(project_id, branch):
    variables = {"projectId": project_id, "branchName": branch}
    response = run_graphql(
        _graphql_checkout_branch(branch), variables, operation_name="checkout"
    )
    if response.status_code != 200:
        logging.error(f"Error: while checking out branch {branch}")
        raise Exception(f"Error: while checking out branch {branch}")
    return response.json()


def checkout_branch(project_id, branch=None):
    variables = {"projectId": project_id}
    response = run_graphql(_graphql_get_default_branch(project_id), variables)

    # Check the response
    if response.status_code == 200:
        response = response.json()
        main_branch = response["data"]["Project"]["mainBranch"]
        working_branch = response["data"]["Project"]["listBranches"]["workingBranch"]
        available_branches = response["data"]["Project"]["listBranches"][
            "checkedOutBranches"
        ]

        # Determine target branch
        target_branch = branch if branch != "default" else main_branch

        # Check if target branch exists
        if target_branch not in available_branches:
            error_msg = f"Branch '{target_branch}' does not exist in project id: {project_id}.\n Available branches: {', '.join(available_branches)}"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Check if we're already on the target branch
        if target_branch != working_branch:
            logging.info(
                f"Need to checkout from '{working_branch}' to '{target_branch}'"
            )
            checkout_result = _checkout_branch(project_id, target_branch)
            logging.info(
                f"Checkout success to branch '{target_branch}', response: {checkout_result}"
            )
        else:
            logging.warning(
                f"Already on the '{target_branch}' branch, ignoring checkout"
            )
    else:
        logging.error(
            f"GraphQL query failed with status code {response.status_code}: {response.text} for ProjectId: {project_id}"
        )
        raise Exception(f"Error switching to branch for {project_id}")


def get_dataset_info_from_id(dataset_id):
    # Send the request
    response = run_graphql(_graphql_dataset_query(dataset_id))
    # Check the response
    if response.status_code == 200:
        data = response.json()
        # print("GraphQL response data:")
        # print(json.dumps(data, indent=4))  # Pretty-print JSON response
        # Navigate through the nested JSON to extract the configuration
        versioned_aspects = data["data"]["Dataset"]["physicalDatasets"][0][
            "versionedAspects"
        ][0]["VersionedAspectValue"]
        config_json = json.loads(versioned_aspects)["dataset.json"]
        config = json.loads(config_json)
        # Check the format and parse accordingly
        dataset_format = config["format"]
        if dataset_format == "catalogTable":
            # Parse database and table from the path and tableName
            catalog = config["catalog"]
            path = config["path"]
            table_name = config["tableName"]
            database_name = path.split("/")[-1]
            # parsed_data = {'type': 'catalog', 'database': database, 'table': table_name}
            # logging.info(
            #     {
            #         "type": "catalog",
            #         "catalog": catalog,
            #         "database": database_name,
            #         "table": table_name,
            #     }
            # )
            return catalog, database_name, table_name
        else:
            # Parse path as source path
            # logging.info(
            #     {
            #         "type": "path",
            #         "catalog": dataset_format,
            #         "source_path": config["path"],
            #     }
            # )
            return dataset_format, "PATH", config["path"]
    else:
        logging.error(
            f"GraphQL query failed with status code {response.status_code}: {response.text} for dataset Id: {dataset_id}"
        )
        raise Exception(f"Error getting dataset info for dataset Id: {dataset_id}")
