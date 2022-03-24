import logging

logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(filename="./debug.log")
format = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")

handler.setFormatter(format)

logger = logging.getLogger("T-REST")
logger.addHandler(handler)




