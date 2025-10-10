import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


class LogManager:
    """Centralized logging manager for test automation."""

    _loggers = {}

    @staticmethod
    def setup_logger(
            name: str = "test_automation",
            log_dir: str = "logs",
            log_level: int = logging.INFO,
            console_output: bool = True,
            max_bytes: int = 10 * 1024 * 1024,  # 10MB
            backup_count: int = 5
    ):
        """
        Setup and configure logger with file and console handlers.

        Args:
            name: Logger name
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Enable console output
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep

        Returns:
            Logger instance
        """
        # Return existing logger if already configured
        if name in LogManager._loggers:
            return LogManager._loggers[name]

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.propagate = False

        # Clear existing handlers
        logger.handlers.clear()

        # Create log directory
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # File handler - detailed logs with rotation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_path / f"test_execution_{timestamp}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

        # Console handler - simplified output
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(simple_formatter)
            logger.addHandler(console_handler)

        # Store logger reference
        LogManager._loggers[name] = logger

        logger.info("=" * 80)
        logger.info(f"Logging initialized - Log file: {log_file}")
        logger.info("=" * 80)

        return logger

    @staticmethod
    def get_logger(name: str = "test_automation"):
        """
        Get existing logger or create new one.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        if name not in LogManager._loggers:
            return LogManager.setup_logger(name)
        return LogManager._loggers[name]

    @staticmethod
    def log_test_start(logger, test_case_id: str, description: str = ""):
        """Log test case start."""
        logger.info("=" * 80)
        logger.info(f"TEST CASE START: {test_case_id}")
        if description:
            logger.info(f"Description: {description}")
        logger.info("=" * 80)

    @staticmethod
    def log_test_end(logger, test_case_id: str, status: str, duration: float = None):
        """Log test case end."""
        logger.info("-" * 80)
        logger.info(f"TEST CASE END: {test_case_id} | Status: {status}")
        if duration:
            logger.info(f"Duration: {duration:.2f} seconds")
        logger.info("=" * 80)
        logger.info("")

    @staticmethod
    def log_step(logger, step_no: str, action: str, locator: str = "", value: str = ""):
        """Log test step execution."""
        step_info = f"Step {step_no}: {action}"
        if locator:
            step_info += f" | Locator: {locator}"
        if value:
            step_info += f" | Value: {value}"
        logger.info(step_info)

    @staticmethod
    def log_step_result(logger, step_no: str, status: str, message: str = ""):
        """Log test step result."""
        if status.upper() == "PASS":
            logger.info(f"Step {step_no} - PASSED {f'| {message}' if message else ''}")
        elif status.upper() == "FAIL":
            logger.error(f"Step {step_no} - FAILED {f'| {message}' if message else ''}")
        else:
            logger.warning(f"Step {step_no} - {status} {f'| {message}' if message else ''}")

    @staticmethod
    def log_exception(logger, exception: Exception, context: str = ""):
        """Log exception with context."""
        logger.error(f"Exception occurred {f'in {context}' if context else ''}: {str(exception)}")
        logger.exception("Full traceback:")

    @staticmethod
    def cleanup_old_logs(log_dir: str = "logs", days: int = 7):
        """
        Delete log files older than specified days.

        Args:
            log_dir: Directory containing log files
            days: Number of days to retain logs
        """
        log_path = Path(log_dir)
        if not log_path.exists():
            return

        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for log_file in log_path.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    print(f"Deleted old log file: {log_file}")
                except Exception as e:
                    print(f"Failed to delete {log_file}: {e}")


# Convenience function for quick logger access
def get_logger(name: str = "test_automation"):
    """Get logger instance."""
    return LogManager.get_logger(name)