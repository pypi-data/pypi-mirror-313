import logging

def init_logging_handlers(handler_list,
	logger_name=None,
	logger_level=logging.DEBUG,
	default_fmt='%(message)s',
	default_level=logging.WARNING):

	logger = logging.getLogger(logger_name)
	logger.setLevel(logger_level)

	for handler, fmt, lvl in handler_list:

		fmt = fmt or default_fmt
		fmt_style = "%" if "%" in fmt else "{"

		formatter = logging.Formatter(fmt, style=fmt_style)
		handler.setFormatter(formatter)
		handler.setLevel(lvl or default_level)

		logger.addHandler(handler)

	return logger
