import logging
from colorama import Fore


class CustomFormatter(logging.Formatter):
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Fore.WHITE + format + Fore.RESET,
        logging.INFO: Fore.CYAN + format + Fore.RESET,
        logging.WARNING: Fore.YELLOW + format + Fore.RESET,
        logging.ERROR: Fore.RED + format + Fore.RESET,
        logging.CRITICAL: Fore.MAGENTA + format + Fore.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# FORMAT = '%(asctime)s %(name)s: %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.WARNING)

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.INFO)
da_logger = logging.getLogger("DigitalArz")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

da_logger.addHandler(ch)

da_logger.propagate = False