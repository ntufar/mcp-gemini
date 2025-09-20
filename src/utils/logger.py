import logging
import json
import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = JsonFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger