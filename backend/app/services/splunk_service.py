from typing import List, Dict
from models.splunk import SearchRequest, SplunkEvent, SearchResponseGroup
from collections import defaultdict
import splunklib.client as client
import splunklib.results as results

# You may want to move these to env variables or config
SPLUNK_HOST = "your-splunk-host"
SPLUNK_PORT = 8089
SPLUNK_USERNAME = "your-username"
SPLUNK_PASSWORD = "your-password"

def build_spl_query(req: SearchRequest) -> str:
    if req.raw_query:
        return req.raw_query

    query_parts = ["search index=your_index"]
    if req.process_name:
        query_parts.append(f'process_name="{req.process_name}"')
    if req.environment:
        query_parts.append(f'environment="{req.environment}"')
    if req.execution_id:
        query_parts.append(f'exec_id="{req.execution_id}"')
    for kv in req.kv_filters:
        query_parts.append(f'{kv.key}="{kv.value}"')

    return " | ".join(query_parts)

def run_splunk_query(req: SearchRequest) -> List[Dict]:
    service = client.connect(
        host=SPLUNK_HOST,
        port=SPLUNK_PORT,
        username=SPLUNK_USERNAME,
        password=SPLUNK_PASSWORD,
        scheme="https"
    )

    query = build_spl_query(req)
    kwargs_search = {
        "earliest_time": req.time_range.earliest,
        "latest_time": req.time_range.latest,
        "output_mode": "json"
    }

    job = service.jobs.create(query, **kwargs_search)
    while not job.is_done():
        pass  # You can add a timeout or sleep if needed

    output = []
    for result in results.JSONResultsReader(job.results(output_mode="json")):
        if isinstance(result, dict):
            output.append(result)

    return output

def group_and_sort_events(raw_events: List[Dict]) -> List[SearchResponseGroup]:
    grouped = defaultdict(list)

    for e in raw_events:
        exec_id = e.get("exec_id")
        sequence_no = int(e.get("sequence_no", 0))
        event = SplunkEvent(
            exec_id=exec_id,
            sequence_no=sequence_no,
            timestamp=e.get("_time"),
            data=e,
            has_clob=False  # Will be updated only when needed
        )
        grouped[exec_id].append(event)

    response = []
    for exec_id, events in grouped.items():
        sorted_events = sorted(events, key=lambda x: x.sequence_no)
        response.append(SearchResponseGroup(exec_id=exec_id, events=sorted_events))
    return response
