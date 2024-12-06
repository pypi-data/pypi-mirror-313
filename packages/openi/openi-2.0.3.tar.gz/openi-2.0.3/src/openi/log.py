import logging
from logging.handlers import TimedRotatingFileHandler

from .constants import LOG_FILE


def setup_logger(log_level: str = "info"):
    """
    Output logs to a file with a rotating file handler

    1. `filename='~/.openi/log/openi.log'`: This parameter specifies the filename of the log file. In this case, it's set to `'~/.openi/log/openi.log'`, which means the log file will be located at `~/.openi/log/openi.log`, where `~` represents the user's home directory.
    2. `when="D"`: This parameter specifies the type of interval for rotating the log files. In this case, it's set to `"D"`, which stands for daily rotation. This means that a new log file will be created every day.
    3. `interval=1`: This parameter specifies the interval at which log files should be rotated. In this case, it's set to `1`, which means the rotation will occur every `1` unit of the interval type specified in the `when` parameter. Since `when` is set to `"D"`, the rotation will occur every day.
    4. `backupCount=3`: This parameter specifies the number of backup log files to retain. In this case, it's set to `3`, which means that up to `3` backup log files will be kept in addition to the current log file.
    Now, let's visualize how the log directory will look like in the future. Assuming today's date is March 1, 2024, and the log files are rotated daily:

    ```
    ~/.openi/log/
        ├── openi.log (current log file)
        ├── openi.log.20240301 (log file for March 1, 2024)
        ├── openi.log.20240302 (log file for March 2, 2024)
        ├── openi.log.20240303 (log file for March 3, 2024)
        ├── openi.log.20240304 (log file for March 4, 2024)
        └── ...
    ```

    Each day, a new log file will be created with the date appended to its filename, and the previous day's log file will be renamed accordingly. Up to `3` backup log files will be retained (`openi.log.20240301`, `openi.log.20240302`, and `openi.log.20240303`), and older log files will be deleted once the limit is reached.

    """
    # Check if logger already exists
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger

    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(funcName)s(): %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    # Define the TimedRotatingFileHandler with the specified parameters
    handler = TimedRotatingFileHandler(filename=LOG_FILE, when="D", interval=1, backupCount=3)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    # Create a logger and set its level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logger's level to DEBUG to ensure all levels are captured

    # Add the handler to the logger
    logger.addHandler(handler)

    # Define custom log levels
    logging.addLevelName(25, "HTTP")
    logging.addLevelName(26, "RESPONSE")

    # Define custom logging methods for HTTP and RESPONSE levels
    def http(self, message, *args, **kws):
        if self.isEnabledFor(25):
            self._log(25, message, args, **kws)

    def response(self, message, *args, **kws):
        if self.isEnabledFor(26):
            self._log(26, message, args, **kws)

    # Add custom logging methods to the logger
    logging.Logger.http = http
    logging.Logger.response = response

    # Set the logger's level based on the input log_level
    valid_log_levels = ["debug", "info", "warning", "error", "critical"]
    if log_level.lower() not in valid_log_levels:
        raise ValueError(f"Invalid log level: {log_level}. Choose from {valid_log_levels}")
    logger.setLevel(getattr(logging, log_level.upper()))

    return logger
