import logging
import os
from datetime import datetime
from pathlib import Path

__ALL__ = ['Logger', 'stdout_log']

def stdout_log(msg):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{dt}: {msg}")

class Logger:
    def __init__(self, name, log_dir=f"{Path.home()}/logs"):
        self.name = name
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.set_log_file()

    def set_log_file(self):
        log_filename = datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S_{self.name}.log")
        log_filepath = os.path.join(self.log_dir, log_filename)
        file_handler = logging.FileHandler(log_filepath)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
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