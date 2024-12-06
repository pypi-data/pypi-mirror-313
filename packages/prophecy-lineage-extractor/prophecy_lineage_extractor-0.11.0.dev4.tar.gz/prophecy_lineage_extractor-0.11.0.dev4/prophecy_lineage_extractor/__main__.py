import argparse
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta

import logging
import sys
import websocket

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import (
    PROJECT_ID,
    PIPELINE_ID,
    SEND_EMAIL,
    PROPHECY_PAT,
    LONG_SLEEP_TIME,
    MONITOR_TIME_DEFAULT,
    BRANCH, OUTPUT_DIR, MONITOR_TIME_ENV,
)
from prophecy_lineage_extractor.graphql import checkout_branch
from prophecy_lineage_extractor.utils import (
    delete_file,
    safe_env_variable,
    send_excel_email,
    get_ws_url,
    get_output_path,
    convert_csv_to_excel,
)
from prophecy_lineage_extractor.ws_handler import handle_did_open, handle_did_update

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the format
    datefmt="%Y-%m-%d %H:%M:%S",  # Optional: customize the date format
)

last_meaningful_message_time = datetime.now()


def update_monitoring_time():
    global last_meaningful_message_time
    last_meaningful_message_time = datetime.now()
    logging.warning(
        f"[MONITORING]: Updating idle time, current idle time"
        f"= {datetime.now() - last_meaningful_message_time}"
    )


def on_error(ws, error):
    logging.error("Error: " + str(error))
    ws.close()
    exit(1)


def on_close(ws, close_status_code, close_msg):
    logging.info("### WebSocket closed ###")

    # TODO: fix this, currently status_code is always None
    # if close_status_code != 0:
    #     logging.error(
    #         f"WebSocket closed with non-zero status code: {close_status_code} \n message :{close_msg}"
    #     )
    #     sys.exit(1)  # Exit the program with a failure status
    # else:
    #     logging.info(f"Close Status Code: {close_status_code}, Message: {close_msg}")


def on_message(ws, message):
    global last_meaningful_message_time
    logging.info(f"\n\n### RECEIVED a message### ")
    try:
        json_msg = json.loads(message)
        if "method" in json_msg:
            method = json_msg["method"]
            logging.warning(f"method: {method}")
            if method == "properties/didOpen":
                update_monitoring_time()
                handle_did_open(ws, json_msg)
            elif method == "properties/didUpdate":
                update_monitoring_time()
                handle_did_update(ws, json_msg)
            elif method == "error":
                logging.error(f"Error occurred:\n {json_msg['params']['msg']}")
                raise Exception(
                    f"Error occurred and we got method='Error'\n {json_msg}"
                )
        else:
            raise Exception("method is not found in message", json_msg)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON message: {e}")
        raise e


def on_open(ws):
    delete_file(get_output_path("csv"))
    logging.info(
        f"\n\n### SENDING INIT PIPELINE for {safe_env_variable(PIPELINE_ID)} ### "
    )
    ws.send(
        messages.init_pipeline(
            safe_env_variable(PROJECT_ID), safe_env_variable(PIPELINE_ID)
        )
    )
    time.sleep(LONG_SLEEP_TIME)


def monitor_ws(ws):
    logging.info("Monitor thread started.")

    """Monitor the WebSocket connection and terminate if inactive."""
    global last_meaningful_message_time
    time.sleep(10)
    monitor_time = os.environ.get(MONITOR_TIME_ENV, MONITOR_TIME_DEFAULT)
    logging.info(f"Monitor Time: {monitor_time}")
    while ws.keep_running:
        # logging.info("Monitoring...")
        if datetime.now() - last_meaningful_message_time > timedelta(
            seconds=monitor_time
        ):
            logging.warning(
                f"[MONITORING]: No meaningful messages received in the last {monitor_time} seconds, closing websocket"
            )
            try:
                if (
                    safe_env_variable(SEND_EMAIL) == "True"
                ):  # the value of env variable is always string
                    logging.info("sending mail as --send-email passed")
                    convert_csv_to_excel(
                        csv_path=get_output_path("csv"), output_path=get_output_path()
                    )
                    send_excel_email(get_output_path())
                else:
                    logging.info("Not sending mail not --send-email was not passed")

            except Exception as e:
                logging.error(e)
                raise e
            finally:
                ws.close()
        else:
            logging.warning(
                f"[MONITORING]: Idle time"
                f" {datetime.now() - last_meaningful_message_time} seconds"
            )
        time.sleep(10)

    logging.info("Monitor thread ended.")


def run_websocket():
    """Run WebSocket in a separate thread."""
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        get_ws_url(),
        header={"X-Auth-Token": safe_env_variable(PROPHECY_PAT)},
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_ws, args=(ws,), daemon=True)
    monitor_thread.start()

    # Start the WebSocket connection
    ws.run_forever()
    return ws


def main():
    parser = argparse.ArgumentParser(description="Prophecy Lineage Extractor")
    # Adding arguments
    parser.add_argument(
        "--project-id", type=str, required=True, help="Prophecy Project ID"
    )
    parser.add_argument(
        "--pipeline-id", type=str, required=True, help="Prophecy Pipeline ID"
    )
    parser.add_argument(
        "--send-email", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--branch",
        type=str,
        required=False,
        default="default",
        help="Branch to run lineage extractor on",
    )
    parser.add_argument(
        "--output-dir", type=str, required=True, help="Output directory inside the project"
    )

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    os.environ[PROJECT_ID] = args.project_id
    os.environ[PIPELINE_ID] = args.pipeline_id
    os.environ[SEND_EMAIL] = str(args.send_email)
    os.environ[BRANCH] = args.branch
    os.environ[OUTPUT_DIR] = args.output_dir

    checkout_branch(safe_env_variable(PROJECT_ID), safe_env_variable(BRANCH))
    logging.info("Starting WebSocket thread..")
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    ws_thread.join()


if __name__ == "__main__":
    main()
