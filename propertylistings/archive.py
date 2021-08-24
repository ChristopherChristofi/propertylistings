import logging

def logger(logfile=None):
    logging.basicConfig(
        filename=logfile,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s : %(relativeCreated)d : %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
        )

if __name__ == '__main__':

    logger(None)
