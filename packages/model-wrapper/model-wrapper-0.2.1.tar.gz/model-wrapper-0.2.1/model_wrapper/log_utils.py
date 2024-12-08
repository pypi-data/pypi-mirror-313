from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def info(message):
	logger.info(message)


def warn(message):
	logger.warning(message)
