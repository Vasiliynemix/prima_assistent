import sys
import os

from loguru import logger


class Logger:
    LOG_FORMAT = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
                  " <level>{level: <4}</level> |"
                  " <level><blue>{file}</blue>:</level><blue>{line}</blue> -->"
                  " <level>{message}</level>")
    COMPRESSION = "zip"
    ROTATION = "1 MB"
    INFO = "info"

    def __init__(
        self,
        log_level: str,
        log_dir_name: str,
        info_log_path: str | None = None,
    ):
        self.log_level = log_level
        self.log_dir_name = log_dir_name
        self.info_log_path = info_log_path

    def setup_logger(self) -> None:
        self.__create_log_directory_if_exists()
        log_path = self.info_log_path

        logger.remove()

        logger.add(
            log_path,
            format=self.LOG_FORMAT,
            level=self.log_level.upper(),
            rotation=self.ROTATION,
            compression=self.COMPRESSION,
        )

        logger.add(
            sys.stdout,
            format=self.LOG_FORMAT,
            level=self.log_level.upper(),
        )

    def __create_log_directory_if_exists(self) -> None:
        if not os.path.exists(self.log_dir_name):
            os.makedirs(self.log_dir_name, exist_ok=True)
