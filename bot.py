import logging, logging.handlers, sys
# Logging code is messy as hell, should be cleaned up in the near future
FORMAT = f'[%(levelname)s] [%(name)s] [%(asctime)s]: %(message)s'
logger = logging.getLogger("PartnersBot")
logger.setLevel(logging.INFO)
format = logging.Formatter(FORMAT, datefmt="%d/%m/%Y %H:%M")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(format)
fhandler = logging.handlers.RotatingFileHandler(
    filename='main.log', encoding='utf-8', mode='a',
    maxBytes=10**7, backupCount=5)
fhandler.setFormatter(format)
logger.addHandler(stdout_handler)
logger.addHandler(fhandler)

import partnersbot

bot = partnersbot.make_bot()

bot.run()