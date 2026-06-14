import json
import time
import redis

from app.core.runs.redis_keys import run_record_key, run_events_key, run_stop_key
from app.core.config import REDIS_URL, REDIS_RETENTION_SECONDS

class RedisRunStore:
    def __init__(self):
        redis_url = REDIS_URL
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        self.retention_seconds = REDIS_RETENTION_SECONDS

    def create_run(self, run_id: str, conversation_id: int, user_id: int = 1):
        record = {
            "run_id": run_id,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "status": "running",
            "created_at": time.time(),
            "updated_at": time.time(),
            "error": None,
        }
        key = run_record_key(run_id)
        self.client.set(key, json.dumps(record, ensure_ascii=False), ex=self.retention_seconds)

        return record
    
    def update_run(self, run_id: str, status: str, error: str | None = None):
        key = run_record_key(run_id)
        raw = self.client.get(key)

        if raw:
            record = json.loads(raw)
        else:
            record = {"run_id": run_id}

        record["status"] = status
        record["updated_at"] = time.time()
        record["error"] = error

        self.client.set(key, json.dumps(record, ensure_ascii=False), ex=self.retention_seconds)

    def get_run(self, run_id: str):
        key = run_record_key(run_id)
        raw = self.client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    
    def add_event(self, run_id: str, event_type: str, data:dict):
        key = run_events_key(run_id)
        event_id = self.client.xadd(key, {
            "type": event_type,
            "data": json.dumps(data, ensure_ascii=False),
            "ts": time.time()
        })
        self.client.expire(key, self.retention_seconds)
        self.client.expire(run_record_key(run_id), self.retention_seconds)

        return event_id
    
    def read_events(self, run_id: str, start: str = "0-0"):
        key = run_events_key(run_id)
        events = self.client.xrange(key, min=start, max="+")
        result = []
        for event_id, fields in events:
            result.append({
                "id": event_id,
                "type": fields.get("type"),
                "data": json.loads(fields.get("data", "{}")),
                "ts": fields.get("ts")
            })
        return result
    
    def request_stop(self, run_id: str):
        self.client.set(run_stop_key(run_id), user_id=1, ex=self.retention_seconds)
    
    def should_stop(self, run_id: str) -> bool:
        return self.client.exists(run_stop_key(run_id))==1
