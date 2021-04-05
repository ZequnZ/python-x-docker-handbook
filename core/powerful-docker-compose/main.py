import logging
import logging.handlers
import socket


class LogUDPHandler(logging.handlers.SysLogHandler):
    """Class to log UDP Handler."""

    def emit(self, record):
        """
        Emit a record.
        The record is formatted, and then sent to the syslog server. If
        exception information is present, it is NOT sent to the server.
        """
        try:
            msg = self.format(record)

            # Message is a string. Convert to bytes as required by RFC 5424
            msg = msg.encode("utf-8")
            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except Exception:
            self.handleError(record)


logging.raiseExceptions = True
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

host, port = "log_server", 5237
logHandler = LogUDPHandler(address=(host, port))
# Set log format
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logHandler.setFormatter(formatter)
logHandler.setLevel(logging.DEBUG)
logger.addHandler(logHandler)

# logs with different levels
logger.debug("debug msg")
logger.info("info msg")
logger.warning("warning msg")
logger.error("error msg")
