import logging


class LoggerFormatter(logging.Formatter):
  COLOR_GREY = '\x1b[38;20m'
  COLOR_YELLOW = '\x1b[33;20m'
  COLOR_RED = '\x1b[31;20m'
  COLOR_BOLD_RED = '\x1b[31;1m'
  COLOR_RESET = '\x1b[0m'

  BASE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'

  LEVEL_FORMATS = {
    logging.DEBUG: COLOR_GREY + BASE_FORMAT + COLOR_RESET,
    logging.INFO: COLOR_GREY + BASE_FORMAT + COLOR_RESET,
    logging.WARNING: COLOR_YELLOW + BASE_FORMAT + COLOR_RESET,
    logging.ERROR: COLOR_RED + BASE_FORMAT + COLOR_RESET,
    logging.CRITICAL: COLOR_BOLD_RED + BASE_FORMAT + COLOR_RESET,
  }

  def format_record(self, record):
    # Get the format for the current log level, defaulting to grey if not specified
    log_fmt = self.LEVEL_FORMATS.get(record.levelno, self.COLOR_GREY + self.BASE_FORMAT + self.COLOR_RESET)
    formatter = logging.Formatter(log_fmt)
    return formatter.format(record)

  def format(self, record):
    return self.format_record(record)
