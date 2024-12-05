import threading
import time
import ssl
import json
from json import dumps, loads
from logger import logger

import websocket


class Socket:
    """Socket Class."""

    def __init__(self, parent, inactivity_threshold=60):
        """Class constructor."""
        self.parent = parent
        self._ws_app = None
        self.reconnect_delay = 5
        self.ws_thread = None
        self.last_message_time = time.time()
        self.inactivity_threshold = inactivity_threshold
        self.inactivity_thread = None
        self.lock = threading.Lock()
        self.external_on_message = None

    def __on_open(self, ws):
        logger.info("Socket connection open...")
        params = {
            "action": "VALIDATE_AUTH_TOKEN",
            "payload": self.parent.user.get("authToken"),
        }
        ws.send(dumps(params))
        self.last_message_time = time.time()
        logger.info("Initializing inactivity checker")
        self.inactivity_thread = threading.Thread(target=self._inactivity_checker, args=(ws,), daemon=True)
        self.inactivity_thread.start()
        logger.info("Inactivity checker thread started")

    def __on_error(self, ws, error):
        logger.error(f"Socket error: {error}")
        logger.info("on_error callback triggered.")

    def __on_close(self, ws, close_status_code, close_msg):
        logger.warning(f"Socket closed. Status code: {close_status_code}, Message: {close_msg}")
        logger.info("on_close callback triggered.")

    def __on_message_wrapper(self, ws, message):
        """
        Internal message handler that processes the message and then forwards it to the external handler.
        """
        try:
            data = loads(message)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message: {e}")
            return

        if data.get('error'):
            logger.error("Error received. Closing WebSocket to trigger reconnection.")
            ws.close()
            return

        self.last_message_time = time.time()

        if self.external_on_message:
            try:
                self.external_on_message(ws, message)
            except Exception as e:
                logger.error(f"Exception in external on_message handler: {e}")

    def _inactivity_checker(self, ws):
        """Check for inactivity and close WebSocket if threshold is exceeded."""
        while True:
            time.sleep(30)
            elapsed_time = time.time() - self.last_message_time
            if elapsed_time > self.inactivity_threshold:
                logger.warning(
                    f"No message received in the last {self.inactivity_threshold / 60} minutes. Closing WebSocket to reconnect.")
                try:
                    ws.close()
                except Exception as e:
                    logger.error(f"Exception while closing WebSocket due to inactivity: {e}")
                logger.info("Called ws.close() due to inactivity.")
                break

    def connect(self, on_message=None):
        """Attempt to connect to the WebSocket endpoint."""
        self.external_on_message = on_message
        if on_message is None:
            logger.info("No external on_message handler provided.")
        else:
            logger.info("External on_message handler provided.")

        def run_ws():
            attempt = 0
            max_delay = 20
            while True:
                try:
                    logger.info(f"Attempting to connect to WebSocket at {self.parent.ws_url}...")
                    with self.lock:
                        login_success = False
                        try:
                            login_success = self.parent.auth.login_rsa()
                        except Exception as e:
                            logger.error(f"Exception during login: {e}")
                    if not login_success:
                        logger.error("Login failed. Waiting before retrying...")
                        attempt += 1
                        delay = min(self.reconnect_delay * (2 ** attempt), max_delay)
                        logger.info(f"Retrying login in {delay} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        attempt = 0

                    logger.debug(f"Using auth token: {self.parent.user.get('authToken')}")
                    headers = {
                        "Origin": "https://app.canary.ithacanoemon.tech"
                    }

                    self._ws_app = websocket.WebSocketApp(
                        url=self.parent.ws_url,
                        header=headers,
                        on_message=self.__on_message_wrapper,
                        on_error=self.__on_error,
                        on_close=self.__on_close,
                        on_open=self.__on_open,
                    )
                    sslopt = (
                        {"cert_reqs": ssl.CERT_NONE}
                        if "localhost" in self.parent.base_url
                        else {}
                    )
                    self._ws_app.run_forever(ping_interval=14, sslopt=sslopt)
                    logger.info("run_forever() exited.")
                except Exception as e:
                    logger.error(f"Exception in WebSocket connection: {e}")

                logger.info(f"WebSocket connection lost. Reconnecting in {self.reconnect_delay} seconds...")
                time.sleep(self.reconnect_delay)

        self.ws_thread = threading.Thread(target=run_ws)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def close(self):
        """Manually close the WebSocket connection."""
        if self._ws_app:
            try:
                self._ws_app.close()
                logger.info("WebSocket connection closed manually.")
            except Exception as e:
                logger.error(f"Exception while closing WebSocket manually: {e}")
