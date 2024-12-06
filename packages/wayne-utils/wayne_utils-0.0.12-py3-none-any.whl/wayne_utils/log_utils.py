############################################日志工具###################################################
import logging

class CustomError(Exception):  
    def __init__(self, message, logger):  
        super().__init__(message)  
        if logger:  
            logger.error(message)

def create_logger( log_name, save_path_name, level=1 ):
    # Ceate and determine its level
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    logger = logging.getLogger(log_name)
    logger.setLevel( levels[level] )  
    
    # Create a FileHandler for writing log files 
    file_handler = logging.FileHandler( save_path_name, encoding='utf-8' )  
    file_handler.setLevel( levels[level] )  
    
    # Create a StreamHandler for outputting to the console  
    console_handler = logging.StreamHandler()  
    console_handler.setLevel( levels[level] )  
    
    # Define the output format of the handler 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    file_handler.setFormatter(formatter)  
    console_handler.setFormatter(formatter)  
    
    # Add Handler to Logger
    logger.addHandler(file_handler)  
    logger.addHandler(console_handler)  

    return logger

class SingletonLogger:  
    _instances = {}  
    @classmethod  
    def get_logger(cls, log_name, save_path_name, level=1):  
        if log_name not in cls._instances:  
            levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]  
            logger = logging.getLogger(log_name)  
            logger.setLevel(levels[level])  
  
            file_handler = logging.FileHandler(save_path_name, encoding='utf-8')  
            file_handler.setLevel(levels[level])  
  
            console_handler = logging.StreamHandler()  
            console_handler.setLevel(levels[level])  
  
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
            file_handler.setFormatter(formatter)  
            console_handler.setFormatter(formatter)  
  
            logger.addHandler(file_handler)  
            logger.addHandler(console_handler)  
  
            cls._instances[log_name] = logger  
  
        return cls._instances[log_name]