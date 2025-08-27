import logging
import sys
from datetime import datetime
from typing import Optional
import json
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
class CustomFormatter(logging.Formatter):
    """Custom formatter with structured logging for better readability"""
    
    def format(self, record):
        # Create structured log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage()
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry, indent=2)

def setup_logger(name: str, log_file: Optional[str] = None, level: str = "INFO") -> logging.Logger:
    """Setup a logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = CustomFormatter()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create specific loggers for different components
lost_and_found_logger = setup_logger(
    "lost_and_found", 
    log_file="logs/lost_and_found.log"
)

api_logger = setup_logger(
    "api", 
    log_file="logs/api.log"
)

database_logger = setup_logger(
    "database", 
    log_file="logs/database.log"
)

# Utility function for structured logging
def log_lost_and_found_event(
    event_type: str,
    user_id: Optional[str] = None,
    qr_id: Optional[str] = None,
    action: Optional[str] = None,
    details: Optional[dict] = None,
    error: Optional[Exception] = None,
    level: str = "INFO"
):
    """Log lost and found events with structured data"""
    
    extra_fields = {
        "event_type": event_type,
        "component": "lost_and_found"
    }
    
    if user_id:
        extra_fields["user_id"] = user_id
    if qr_id:
        extra_fields["qr_id"] = qr_id
    if action:
        extra_fields["action"] = action
    if details:
        extra_fields["details"] = details
    
    log_record = logging.LogRecord(
        name="lost_and_found",
        level=getattr(logging, level.upper()),
        pathname="",
        lineno=0,
        msg=f"Lost and Found Event: {event_type}",
        args=(),
        exc_info=(type(error), error, error.__traceback__) if error else None
    )
    log_record.extra_fields = extra_fields
    
    lost_and_found_logger.handle(log_record)

def log_api_request(
    endpoint: str,
    method: str,
    user_id: Optional[str] = None,
    request_data: Optional[dict] = None,
    response_status: Optional[int] = None,
    error: Optional[Exception] = None,
    level: str = "INFO"
):
    """Log API requests with structured data"""
    
    extra_fields = {
        "endpoint": endpoint,
        "method": method,
        "component": "api"
    }
    
    if user_id:
        extra_fields["user_id"] = user_id
    if request_data:
        extra_fields["request_data"] = request_data
    if response_status:
        extra_fields["response_status"] = response_status
    
    log_record = logging.LogRecord(
        name="api",
        level=getattr(logging, level.upper()),
        pathname="",
        lineno=0,
        msg=f"API Request: {method} {endpoint}",
        args=(),
        exc_info=(type(error), error, error.__traceback__) if error else None
    )
    log_record.extra_fields = extra_fields
    
    api_logger.handle(log_record)
