import logging
import os
import colorlog
import pyfiglet
from termcolor import colored
import sys
import time

# Configure logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger('echolib')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG if os.getenv('DEBUG_MODE', 'False').lower() == 'true' else logging.INFO)

def delayed_print(text: str, delay: float = 0.1) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

def display_banner() -> None:
    big_text = pyfiglet.figlet_format("ECHOLIB", font="big")
    small_text = "by Your Name"
    bottom_text = "2024 All rights reserved."

    for line in big_text.splitlines():
        delayed_print(colored(line, 'cyan'), delay=0.001)

    delayed_print(" " * (80 - len(small_text)) + colored(small_text, 'yellow'), delay=0.001)
    delayed_print("\n" + colored(bottom_text, 'magenta'), delay=0.001)

# display_banner()
