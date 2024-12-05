import argparse
import ast
import logging
import time
import zlib

from mqttsn.client import Callback, Client

_dataflow = {}
all_tasks = {}


def translate_from_provlight_to_dfanalyzer(_message_server):
    start = time.time()
    if _message_server["status"] == 1:  # Just need to save first message of each task
        all_tasks[_message_server["id"]] = _message_server
    # logging.info(f"type={type(_message_server)}")
    # logging.info(f"_message_server={_message_server}")
    dfanalyzer_data = {}
    dependency = {"tags": [], "ids": []}
    sets = []
    performances = []
    dfanalyzer_data["tag"] = _message_server["transformation_id"]
    for dep_task in _message_server["dependencies"]:
        dependency["tags"].append({"tag": all_tasks[dep_task]["transformation_id"]})
        dependency["ids"].append({"id": str(dep_task)})
    dfanalyzer_data["dependency"] = dependency
    for ds in _message_server["dataset"]:
        final_list = []
        for sv in ds["attributes"].values():
            for s in sv:
                final_list.append(f"{s}")
        sets.append({"tag": ds["id"], "elements": [list(final_list)]})
    dfanalyzer_data["sets"] = sets
    dfanalyzer_data["status"] = (
        "RUNNING" if _message_server["status"] == 1 else "FINISHED"
    )
    dfanalyzer_data["dataflow"] = _message_server["wf_id"]
    dfanalyzer_data["transformation"] = _message_server["transformation_id"]
    dfanalyzer_data["id"] = str(_message_server["id"])
    if _message_server["status"] == 2:  # 'FINISHED'
        performances.append(
            {
                "startTime": all_tasks[_message_server["id"]]["time"],
                "endTime": _message_server["time"],
            }
        )
    dfanalyzer_data["performances"] = performances
    end = time.time()
    logging.info("#" * 80 + f" translation time (sec) = {end - start}")
    logging.info(f"* * dfanalyzer_data = {dfanalyzer_data}")
    logging.info(f"translation time (sec) = {end - start}")
    return dfanalyzer_data


def dfa_save(message):
    """Send a post request to the Dataflow Analyzer API to store the Task."""
    import requests

    r = requests.post(
        "http://localhost:22000/pde/task/json",
        json=translate_from_provlight_to_dfanalyzer(message),
    )
    logging.info(r.status_code)


class DfaTaskResource(Callback):
    def message_arrived(self, topic_name, payload, qos, retained, msgid):
        logging.info(
            f"{self} | topic_name: {topic_name} | msgid {msgid} | "
            f"qos {qos} | retained {retained} | payload: {payload}"
        )
        client_message = ast.literal_eval(zlib.decompress(payload).decode("ascii"))
        logging.info(f" * * client_message = {client_message}")
        dfa_save(client_message)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="synthetic-workload")
    parser.add_argument(
        "--topic_id",
        type=str,
        required=True,
        help="Topic ID.",
    )
    parser.add_argument(
        "--log",
        type=str,
        required=True,
        help="Path to log file.",
    )
    args = parser.parse_args()

    if args.log is not None:
        logging.basicConfig(filename=args.log, level=logging.INFO)

    aclient = Client(f"translator{args.topic_id}", port=1883)
    aclient.register_callback(DfaTaskResource())
    aclient.connect()
    rc, topic1 = aclient.subscribe(topic=f"provlight{args.topic_id}", qos=0)
    logging.info("*" * 80 + f"topic id is: {topic1}")

    try:
        while True:
            continue
    except KeyboardInterrupt:
        logging.info("Closing the client")
        aclient.disconnect()
