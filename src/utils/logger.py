import logging
import json
import datetime

class StructuredLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        log_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": logging.getLevelName(level),
            "message": msg,
        }
        if extra:
            log_entry.update(extra)
        if exc_info:
            log_entry["exc_info"] = self.formatException(exc_info)
        
        super()._log(level, json.dumps(log_entry), args, exc_info, extra, stack_info, stacklevel)

# Configure a custom logger class
logging.setLoggerClass(StructuredLogger)

def get_logger(name: str) -> StructuredLogger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Ensure handlers are not duplicated if get_logger is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
