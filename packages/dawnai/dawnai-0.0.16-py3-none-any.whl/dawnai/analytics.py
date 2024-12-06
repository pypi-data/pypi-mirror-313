import sys
import time
import threading
from typing import Union, List, Dict, Optional
import requests
from datetime import datetime, timezone
import logging
import json
from dawnai.version import VERSION


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

write_key = None
api_url = "https://api.dawnai.com/"
max_queue_size = 10000
upload_size = 10
upload_interval = 1.0
buffer = []
flush_lock = threading.Lock()
debug_logs = False
flush_thread = None
shutdown_event = threading.Event()
max_ingest_size_bytes = 1 * 1024 * 1024  # 1 MB

def set_debug_logs(value: bool):
    global debug_logs
    debug_logs = value
    if debug_logs:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

def start_flush_thread():
    logger.debug("Opening flush thread")
    global flush_thread
    if flush_thread is None:
        flush_thread = threading.Thread(target=flush_loop)
        flush_thread.daemon = True
        flush_thread.start()

def flush_loop():
    while not shutdown_event.is_set():
        try:
            flush()
        except Exception as e:
            logger.error(f"Error in flush loop: {e}")
        time.sleep(upload_interval)

def flush() -> None:
    global buffer

    if buffer is None:
        logger.error("No buffer available")
        return

    logger.debug("Starting flush")

    with flush_lock:
        current_buffer = buffer
        buffer = []

    logger.debug(f"Flushing buffer size: {len(current_buffer)}")

    grouped_events = {}
    for event in current_buffer:
        endpoint = event["type"]
        data = event["data"]
        if endpoint not in grouped_events:
            grouped_events[endpoint] = []
        grouped_events[endpoint].append(data)

    for endpoint, events_data in grouped_events.items():
        for i in range(0, len(events_data), upload_size):
            batch = events_data[i:i+upload_size]
            logger.debug(f"Sending {len(batch)} events to {endpoint}")
            send_request(endpoint, batch)

    logger.debug("Flush complete")

def send_request(endpoint: str, data_entries: List[Dict[str, Union[str, Dict]]]) -> None:
    
    url = f"{api_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {write_key}",
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data_entries, headers=headers)
            response.raise_for_status()
            logger.debug(f"Request successful: {response.status_code}")
            break
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending request (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to send request after {max_retries} attempts")

def save_to_buffer(event: Dict[str, Union[str, Dict]]) -> None:
    global buffer

    if len(buffer) >= max_queue_size * 0.8:
        logger.warning(f"Buffer is at {len(buffer) / max_queue_size * 100:.2f}% capacity")

    if len(buffer) >= max_queue_size:
        logger.error("Buffer is full. Discarding event.")
        return

    logger.debug(f"Adding event to buffer: {event}")

    with flush_lock:
        buffer.append(event)

    start_flush_thread()

def identify(user_id: str, traits: Dict[str, Union[str, int, bool, float]]) -> None:
    if not _check_write_key():
        return
    data = {"user_id": user_id, "traits": traits}
    save_to_buffer({"type": "identify", "data": data})

def track(
    user_id: str,
    event: str,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if not _check_write_key():
        return

    data = {
        "user_id": user_id,
        "event": event,
        "properties": properties,
        "timestamp": timestamp,
    }
    data.setdefault("properties", {})["$context"] = _get_context()

    save_to_buffer({"type": "track", "data": data})

def track_ai(
    user_id: str,
    event: str,
    model: Optional[str] = None,
    user_input: Optional[str] = None,
    output: Optional[str] = None,
    convo_id: Optional[str] = None,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if not _check_write_key():
        return

    if not user_input and not output:
        raise ValueError("One of user_input or output must be provided and not empty.")

    data = {
        "user_id": user_id,
        "event": event,
        "properties": properties or {},
        "timestamp": timestamp,
        "ai_data": {
            "model": model,
            "input": user_input,
            "output": output,
            "convo_id": convo_id,
        },
    }
    data.setdefault("properties", {})["$context"] = _get_context()

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[dawn] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )

    save_to_buffer({"type": "track", "data": data})

def shutdown():
    logger.info("Shutting down Dawn analytics")
    shutdown_event.set()
    if flush_thread:
        flush_thread.join(timeout=10)
    flush()  # Final flush to ensure all events are sent

def _check_write_key():
    if write_key is None:
        logger.warning("write_key is not set. Please set it before using Dawn analytics.")
        return False
    return True

def _get_context():
    return {
        "library": {
            "name": "python-sdk",
            "version": VERSION,
        },
        "metadata": {
            "pyVersion": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        },
    }


def _get_size(event: dict[str, any]) -> int:
    try:
        data = json.dumps(event)
        return len(data.encode('utf-8'))
    except (TypeError, OverflowError) as e:
        logger.error(f"Error serializing event for size calculation: {e}")
        return 0 