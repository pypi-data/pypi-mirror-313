import json


def init_pipeline(project_id, pipeline_id):
    msg = {
        "method": "initialize",
        "params": {
            "view": "summaryView",
            "projectId": project_id,
            "pipelineId": pipeline_id,
        },
    }
    return json.dumps(msg)


def summary_view():
    msg = {
        "method": "properties/didAction",
        # "id": "0.30412215873174153",
        "params": {
            "graphPath": "$.lineageGraph",
            "actions": [
                {
                    # "elementId": "5",
                    "actionName": "summaryView"
                }
            ],
        },
    }
    return json.dumps(msg)


def change_active_entity(entity_id):
    msg = {
        "method": "properties/didAction",
        # "id": "0.7204518032978922",
        "params": {
            "graphPath": "$.lineageGraph",
            "actions": [
                {
                    # "elementId": "1",
                    "actionName": "activeEntityChange",
                    "params": {
                        # "entityId": "35835/datasets/faker"
                        "entityId": entity_id
                    },
                }
            ],
        },
    }
    return json.dumps(msg)


def detailed_view():
    msg = {
        "method": "properties/didAction",
        # "id": "0.6841601917276299",
        "params": {
            "graphPath": "$.lineageGraph",
            "actions": [
                {
                    # "elementId": "5",
                    "actionName": "detailedDatasetView"
                }
            ],
        },
    }
    return json.dumps(msg)
