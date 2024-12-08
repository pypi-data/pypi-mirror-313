import os
import logging
import logging.handlers
import datetime
import json

## THIS IS A COMPLETELY COPIED LOG FORMAT
class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        """Create a custom format for the log records."""
        log_record = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S'),
            "level": record.levelname,
            "function": record.funcName,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

def setup_logger(file_name, debuging=False):
    """Set up the daily rotating log handler."""
    logger = logging.getLogger("JSONLogger")
    logger.setLevel(logging.DEBUG if debuging else logging.INFO)

    log_filename = file_name + "_" + datetime.datetime.now().strftime('%Y-%m-%d.log')
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    full_log_path = os.path.join(log_dir, log_filename)

    # Create daily rotating file handler
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=full_log_path, 
        when='midnight', 
        interval=1
    )
    handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(console_handler)

    return logger



