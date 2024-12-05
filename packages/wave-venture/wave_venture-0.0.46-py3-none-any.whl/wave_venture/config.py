import os
import sys

from wave_venture import utils


url = os.environ.get("URL", "127.0.0.1:8000/api" if sys.platform.startswith("win") else "http://0.0.0.0:8000/api")
plotter = os.environ.get("PLOTTER", utils.find_gui_plotter())
auth_token = os.environ.get("AUTH_TOKEN", utils.find_auth_token())

websocket_max_size = os.environ.get("WEBSOCKET_MAX_SIZE", None)
websocket_max_queue = os.environ.get("WEBSOCKET_MAX_QUEUE", None)
websocket_read_limit = os.environ.get("WEBSOCKET_READ_LIMIT", 2**32)
websocket_write_limit = os.environ.get("WEBSOCKET_WRITE_LIMIT", 2**32)
websocket_close_timeout = os.environ.get("WEBSOCKET_CLOSE_TIMEOUT", 600000)
websocket_ping_interval = os.environ.get("WEBSOCKET_PING_INTERVAL", 20)
websocket_ping_timeout = os.environ.get("WEBSOCKET_PING_TIMEOUT", 600000)
