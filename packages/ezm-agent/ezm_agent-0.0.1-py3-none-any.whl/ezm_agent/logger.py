import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from os.path import expanduser

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger('ezm_agent')

        home_dir = Path(expanduser("~"))
        log_dir = home_dir / 'logs'
        log_dir.mkdir(exist_ok=True)

        file_handler = TimedRotatingFileHandler(
            log_dir / 'ezm_agent.log',
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8',
            delay=True
        )
        file_handler.suffix = '%Y-%m-%d'
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = Logger()