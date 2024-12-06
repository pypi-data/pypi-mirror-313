from logging import Logger


class MockLogger:
    def __init__(self):
        # Initialize an empty list to store log messages
        self._log_messages = []

    @property
    def log_messages(self):
        """Returns the log messages as a list."""
        return self._log_messages

    def _log(self, level: str, message: str):
        """Internal method to add a log message with a specific level."""
        log_message = f"[{level.upper()}] {message}"
        self._log_messages.append(log_message)

    def debug(self, message: str):
        """Log a DEBUG message."""
        self._log("debug", message)

    def info(self, message: str):
        """Log an INFO message."""
        self._log("info", message)

    def warning(self, message: str):
        """Log a WARNING message."""
        self._log("warning", message)

    def error(self, message: str):
        """Log an ERROR message."""
        self._log("error", message)

    def critical(self, message: str):
        """Log a CRITICAL message."""
        self._log("critical", message)