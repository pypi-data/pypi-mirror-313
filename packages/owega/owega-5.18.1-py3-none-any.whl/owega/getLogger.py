import logging
import os
import tempfile


def genFormatter(color: bool = False) -> logging.Formatter:
    clr = {
        'red': '\x1b[91m',
        'gre': '\x1b[92m',
        'yel': '\x1b[93m',
        'blu': '\x1b[94m',
        'mag': '\x1b[95m',
        'cyn': '\x1b[96m',
        'rst': '\x1b[0m'
    }
    logfmtstr = f'[{clr["mag"]}%(asctime)s{clr["rst"]}]'
    logfmtstr += f' [{clr["yel"]}%(filename)s{clr["rst"]}'
    logfmtstr += f':{clr["cyn"]}%(lineno)s{clr["rst"]}]'
    logfmtstr += f' [{clr["red"]}%(name)s{clr["rst"]}]'
    logfmtstr += f' [{clr["blu"]}%(levelname)s{clr["rst"]}]'
    logfmtstr += ': %(message)s'
    if not color:
        for esc in clr.values():
            logfmtstr = logfmtstr.replace(esc, '')
    return logging.Formatter(logfmtstr)


def getLoggerFile() -> str:
    # Get system temp directory
    temp_dir = tempfile.gettempdir()
    # Get username safely
    username = os.getenv('USERNAME') or os.getenv('USER') or 'user'
    # Create log filename
    logger_file = os.path.join(temp_dir, f'{username}.owega.log')
    return logger_file


def getLogger(name, debug: bool = False) -> logging.Logger:
    logger_file = getLoggerFile()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    cons_hand = logging.StreamHandler()
    if debug:
        cons_hand.setLevel(logging.DEBUG)
    else:
        cons_hand.setLevel(logging.WARNING)
    cons_hand.setFormatter(genFormatter(color=True))
    logger.addHandler(cons_hand)

    try:
        # File handler
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(logger_file), exist_ok=True)
        file_hand = logging.FileHandler(logger_file)
        file_hand.setLevel(logging.DEBUG)
        file_hand.setFormatter(genFormatter(color=False))
        logger.addHandler(file_hand)
    except (OSError, IOError):
        # If file logging fails, just continue with console logging
        pass

    return logger
