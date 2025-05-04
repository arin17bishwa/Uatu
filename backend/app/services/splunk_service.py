import json
from collections import defaultdict
from typing import List, Dict, Generator

import splunklib.client as client
import splunklib.results as results
from splunklib.client import Service

from config import export_splunk_config
from models.splunk import SearchRequest, SplunkEvent, SearchResponseGroup

splunk_config = export_splunk_config()

SPLUNK_CREDENTIALS = {
    "host": splunk_config["SPLUNK_HOST"],
    "port": splunk_config["SPLUNK_PORT"],
    "splunkToken": splunk_config["SPLUNK_TOKEN"],
    "autologin": splunk_config["SPLUNK_AUTO_LOGIN"],
}


def splunk_service_creator() -> Generator[Service, None, None]:
    service: Service = client.connect(**SPLUNK_CREDENTIALS)
    # while service:
    try:
        yield service
    finally:
        _ = 0


def get_splunk_service() -> Service:
    return next(splunk_service_creator())


def splunk_job_waiter(job):
    while True:
        while not job.is_ready():
            continue
        if job["isDone"] == "1":
            break


def build_spl_query(req: SearchRequest) -> str:
    if req.raw_query:
        return req.raw_query
    # non_event_fields = ["source", "-environment"]
    non_event_fields = []
    query_parts = ["search index=api_boomi"]
    for non_event_field in non_event_fields:
        if getattr(req, non_event_field):
            query_parts.append(f"{non_event_field}={getattr(req, non_event_field)}")
    query_parts = [" | ".join(query_parts)]
    # print(req.__fields__)
    print(req)
    if req.exec_id:
        query_parts.append(f'exec_id="{req.exec_id}"')
    else:
        if req.source:
            query_parts.append(f'source="{req.source}"')
        if req.environment:
            query_parts.append(f'environment="{req.environment}"')
    query_parts = [" ".join(query_parts)]
    for kv in req.kv_filters:
        query_parts.append(f'{kv.key}="{kv.value}"')

    final_query = " ".join(query_parts)
    print(final_query)
    return final_query


def run_splunk_query(req: SearchRequest) -> List[Dict]:
    service = get_splunk_service()

    query = build_spl_query(req)

    print(query)
    kwargs_search = {
        "earliest_time": req.time_range.earliest or "-5d",
        "latest_time": req.time_range.latest or "now",
        "output_mode": "json",
    }

    print(kwargs_search)

    job = service.jobs.create(query, **kwargs_search)
    splunk_job_waiter(job)

    # print(job.results())

    output = []
    for result in results.JSONResultsReader(job.results(output_mode="json", count=0)):
        if isinstance(result, dict):
            output.append(result)

    return output


def group_and_sort_events(raw_events: List[Dict]) -> List[SearchResponseGroup]:
    grouped = defaultdict(list)

    for raw_event in raw_events:
        event_data = json.loads(raw_event["_raw"])
        exec_id = event_data.get("exec_id")
        sequence_no = int(event_data.get("sequence", -1))
        event = SplunkEvent(
            exec_id=exec_id,
            sequence_no=sequence_no,
            timestamp=raw_event.get("_time"),
            data=event_data,
            has_clob=True,  # Will be updated only when needed
        )
        grouped[exec_id].append(event)

    response = []
    for exec_id, events in grouped.items():
        sorted_events = sorted(events, key=lambda x: x.sequence_no)
        response.append(SearchResponseGroup(exec_id=exec_id, events=sorted_events))
    print(response)

    return response
