import logging
def get_logger(log_name):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='Clients.log',
                    filemode='w')
    return logging.getLogger(log_name)
