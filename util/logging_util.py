import logging


def get_logger(log_file):
    logger_dbg = logging.getLogger("dbg")
    logger_dbg.setLevel(logging.DEBUG)
    fh_dbg_log = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    fh_dbg_log.setLevel(logging.DEBUG)

    # Print time, logger-level and the call's location in a source file.
    formatter = logging.Formatter(
        '%(asctime)s-%(levelname)s(%(module)s:%(lineno)d)  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    fh_dbg_log.setFormatter(formatter)

    logger_dbg.addHandler(fh_dbg_log)
    logger_dbg.propagate = False
    return logger_dbg