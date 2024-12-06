import logging
from logging.handlers import TimedRotatingFileHandler

class Logger(logging.Logger):
    def __init__(self, log_file='events.log', when='midnight', interval=1, backup_count=7, log_level="INFO", logger_name='EventLogger'):
        super().__init__(logger_name, log_level)

        handler = TimedRotatingFileHandler(log_file, when=when, interval=interval, backupCount=backup_count, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.addHandler(handler)

