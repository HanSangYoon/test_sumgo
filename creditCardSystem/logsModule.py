import logging

loggers = {}

def set_logger(name):
    global loggers
    if loggers.get(name):
        return loggers.get(name)
    else:
        log = logging.getLogger(name)
        hdlr = logging.FileHandler('./process.log')
        hdlr.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(levelname)7s - %(message)s', '%Y-%m-%d %H:%M')
        )
        hdlr.setLevel(logging.INFO)
        log.addHandler(hdlr)
        log.setLevel(logging.INFO)
        log.disabled = False
        loggers.update(dict(logger=log))
    return log
