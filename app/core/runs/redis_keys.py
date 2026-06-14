PREFIX = "icarus"

def run_record_key(run_id: str) -> str:
    return f"{PREFIX}:runs:{run_id}:record"

def run_events_key(run_id: str) -> str:
    return f"{PREFIX}:runs:{run_id}:events"

def run_stop_key(run_id: str) -> str:
    return f"{PREFIX}:runs:{run_id}:stop"

