import logging


class LoggedObject(object):
  @property
  def logger(self):
    logger = logging.getLogger(__name__)
    return logger
