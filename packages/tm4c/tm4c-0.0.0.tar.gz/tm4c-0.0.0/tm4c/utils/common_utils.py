import logging

def create_logger(log_file=None, rank=0):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO if rank == 0 else 'ERROR')
    formatter = logging.Formatter('%(asctime)s  %(levelname)5s  %(message)s')
    # 打印到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO if rank == 0 else 'ERROR')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # 打印到日志文件
    if log_file is not None:
        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setLevel(logging.INFO if rank == 0 else 'ERROR')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.propagate = False # 不要再将该 logger 记录的日志消息传递给其父级 logger
    return logger