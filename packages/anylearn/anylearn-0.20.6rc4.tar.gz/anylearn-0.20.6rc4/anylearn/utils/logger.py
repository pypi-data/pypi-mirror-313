import logging

logger = logging.getLogger('ANYLEARN')
logger.setLevel(logging.INFO)
logger.handlers.clear()
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S", )
sh.setFormatter(formatter)
logger.addHandler(sh)
