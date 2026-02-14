#!/usr/bin/env python3
"""
Final, correct script to watch the Notion Action Inbox for new comments from Adrian
and trigger an 'ops' agent spawn via the Gateway's Tools Invoke API.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
NOTION_VERSION = "2022-06-28"
ACTION_INBOX_DB_ID = "ab5ae7f7-1e2d-4226-9946-b16664c8becc"
ADRIAN_USER_ID = "db392f4a-b2c9-4f94-8500-e1ed50615ea6"
STATE_PATH = Path("/home/adrian/.openclaw/workspace/memory/action-inbox-watch-state.json")
LOG_FILE = Path("/home/adrian/.openclaw/workspace/memory/notion-watcher.log")

# OpenClaw Gateway Config
GATEWAY_URL = "http://127.0.0.1:18789"
GATEWAY_TOKEN = "6b1c23e801e00898ff38c99e3e67571dbf3d902cd94fff28fc6775574debf86c"
AGENT_TO_SPAWN = "ops"
SPAWN_TASK = (
    "A new comment from Adrian is available in the Action Inbox. "
    "Find the relevant task, understand the full context, and take action immediately."
)
# --- End Configuration ---

def log_message(message: str):
    with LOG_FILE.open("a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} - {message}\\n")

def parse_iso_to_timestamp(s: str) -> float:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()

def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return {
        "lastSeenTimestamp": (datetime.now(timezone.utc).timestamp() - 5 * 60),
        "seenCommentIds": [],
    }

def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))

def get_notion_key() -> str:
    key = os.environ.get("NOTION_API_KEY")
    if key:
        return key
    p = Path.home() / ".config" / "notion" / "api_key"
    if p.exists():
        return p.read_text().strip()
    raise SystemExit("ERROR: Missing NOTION_API_KEY and ~/.config/notion/api_key")

def http_request(method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log_message(f"ERROR: HTTP {e.code} {e.reason} for {method} {url}")
        log_message(f"Response body: {e.read().decode('utf-8')}")
        raise

def query_notion_pages(db_id: str) -> list[dict]:
    key = get_notion_key()
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {key}", "Notion-Version": NOTION_VERSION, "Content-Type": "application/json",
    }
    body = {"sorts": [{"timestamp": "last_edited_time", "direction": "descending"}]}
    res = http_request("POST", url, headers, body)
    return res.get("results", [])

def get_page_comments(page_id: str) -> list[dict]:
    key = get_notion_key()
    url = f"https://api.notion.com/v1/comments?block_id={urllib.parse.quote(page_id)}"
    headers = {"Authorization": f"Bearer {key}", "Notion-Version": NOTION_VERSION}
    res = http_request("GET", url, headers)
    return res.get("results", [])

def spawn_ops_agent():
    log_message("New comment found, spawning 'ops' agent via /tools/invoke.")
    url = f"{GATEWAY_URL}/tools/invoke"
    headers = {
        "Authorization": f"Bearer {GATEWAY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "tool": "sessions_spawn",
        "args": {
            "agentId": AGENT_TO_SPAWN,
            "task": SPAWN_TASK,
            "thinking": "high",
            "label": "notion-watcher-spawn"
        },
        "sessionKey": "main"
    }
    try:
        response = http_request("POST", url, headers, payload)
        log_message(f"SUCCESS: Agent spawn request accepted by gateway. Response: {json.dumps(response)}")
    except Exception as e:
        log_message(f"FATAL: Failed to spawn agent via /tools/invoke. Error: {e}")

def main():
    log_message("--- Watcher starting run (v4-final) ---")
    state = load_state()
    last_seen_ts = float(state.get("lastSeenTimestamp", 0))
    run_start_ts = datetime.now(timezone.utc).timestamp()
    seen_ids = set(state.get("seenCommentIds", []))
    
    found_new_comment = False
    
    try:
        pages = query_notion_pages(ACTION_INBOX_DB_ID)
        
        for page in pages:
            page_id = page.get("id")
            if not page_id: continue
                
            for comment in get_page_comments(page_id):
                comment_id = comment.get("id")
                created_time = comment.get("created_time")
                author_id = (comment.get("created_by") or {}).get("id")

                if not all([comment_id, created_time, author_id]): continue

                if (author_id == ADRIAN_USER_ID and
                    parse_iso_to_timestamp(created_time) > last_seen_ts and
                    comment_id not in seen_ids):
                    
                    found_new_comment = True
                    seen_ids.add(comment_id)
    except Exception as e:
        log_message(f"ERROR: Failed to check Notion for updates. Error: {e}")
        found_new_comment = False

    state["lastSeenTimestamp"] = run_start_ts
    state["seenCommentIds"] = list(seen_ids)[-500:]
    save_state(state)

    if found_new_comment:
        spawn_ops_agent()
    else:
        log_message("No new comments found.")
    
    log_message("--- Watcher run finished ---")

if __name__ == "__main__":
    main()
