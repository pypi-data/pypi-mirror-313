import http.server
import socket
import threading
from functools import partial

from loguru import logger

PORT_RANGE = (8000, 8100)


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Override log_message to use loguru for logging requests
    def log_message(self, format, *args):
        logger.debug(
            f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}"
        )


def find_available_port(port_range=PORT_RANGE):
    for port in range(*port_range):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    raise RuntimeError("No available port found in the specified range.")


class LocalHTTPServer:
    def __init__(self, directory, port_range=PORT_RANGE):
        self.directory = directory
        self.port_range = port_range
        self.server = None
        self.server_thread = None
        self.port = None

    def start(self):
        self.__enter__()

    def stop(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        # Start the server
        self.port = find_available_port(self.port_range)

        handler_class = partial(CustomHTTPRequestHandler, directory=self.directory)

        self.server = http.server.ThreadingHTTPServer(
            ("localhost", self.port), handler_class
        )
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        logger.debug(
            f"Server started on port {self.port}, serving directory: {self.directory}"
        )

        return self  # Return self so that it can be used within the with block

    def __exit__(self, exc_type, exc_value, traceback):
        # Shutdown the server
        if self.server:
            logger.debug("Shutting down the server...")
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            logger.debug("Server shut down cleanly.")
            logger.complete()  # Flush the log file

    # Optional method to get a server URL
    def get_server_url(self, relative_path):
        return f"http://localhost:{self.port}/{relative_path}"


def test():
    directory = "."  # Serve the current directory
    with LocalHTTPServer(directory) as server:
        # Perform arbitrary actions here
        # For example, make a request to the server
        import requests

        response = requests.get(server.get_server_url() + "FILENAME-TO-FETCH")
        print(response.text)

        # Any code here will have the server running

    # The server has been shut down automatically here


if __name__ == "__main__":
    test()
