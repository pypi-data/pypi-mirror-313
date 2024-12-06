import logging

from rclpy.impl.logging_severity import LoggingSeverity
from rclpy.impl.rcutils_logger import RcutilsLogger


class Ros2LoggingHandler(logging.Handler):
    def __init__(self, ros_logger: RcutilsLogger):
        super().__init__()
        self.ros_logger = ros_logger

        root_logger = logging.getLogger()

        # Configure logger according to ROS log level
        match ros_logger.get_effective_level():
            case LoggingSeverity.DEBUG:
                root_logger.setLevel(logging.DEBUG)
            case LoggingSeverity.INFO:
                root_logger.setLevel(logging.INFO)
            case LoggingSeverity.WARN:
                root_logger.setLevel(logging.WARN)
            case LoggingSeverity.ERROR:
                root_logger.setLevel(logging.ERROR)
            case LoggingSeverity.FATAL:
                root_logger.setLevel(logging.FATAL)

    def emit(self, record):
        log_msg = self.format(record)

        # Map to standard logging levels
        match record.levelno:
            case logging.DEBUG:
                self.ros_logger.debug(log_msg)
            case logging.INFO:
                self.ros_logger.info(log_msg)
            case logging.WARNING:
                self.ros_logger.warn(log_msg)
            case logging.ERROR:
                self.ros_logger.error(log_msg)
            case logging.CRITICAL:
                self.ros_logger.fatal(log_msg)
            case logging.FATAL:
                self.ros_logger.fatal(log_msg)
