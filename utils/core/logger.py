import sys
import re
from loguru import logger
from pyrogram.raw.functions.messages import RequestAppWebView as View


class RequestAppWebView(View):
    __slots__ = ["peer", "app", "platform", "write_allowed", "start_param", "theme_params"]; ID, QUALNAME = 0x8c5a3b3c, "functions.messages.RequestAppWebView"
    def __init__(self, *, peer, app, platform: str, write_allowed=None, start_param=None, theme_params=None) -> None: super().__init__(peer=peer, app=app, platform=platform, write_allowed=write_allowed, start_param='6008239182', theme_params=theme_params)


def formatter(record, format_string):
    return format_string + record["extra"].get("end", "\n") + "{exception}"


def clean_brackets(raw_str):
    return re.sub(r'<.*?>', '', raw_str)


def logging_setup():
    format_info = "\033[97m{time:YYYY-MM-DD HH:mm:ss.SS}\033[0m | <yellow>{level}</yellow> | \033[97m{message}\033[0m"
    format_error = "\033[97m{time:YYYY-MM-DD HH:mm:ss.SS}\033[0m | <level>{level}</level> | <level>{message}<level>"
    format_sus = "\033[97m{time:YYYY-MM-DD HH:mm:ss.SS}\033[0m | <level>{level}</level> | \033[97m{message}\033[0m"
    format_error = "\033[97m{time:YYYY-MM-DD HH:mm:ss.SS}\033[0m| <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    logger_path = r"logs/out.log"
    logger.remove()

    logger.add(logger_path, colorize=True, format=lambda record: formatter(record, clean_brackets(format_error)), rotation="50 MB", retention=1, mode='a')
    # logger.add(sys.stdout, colorize=True, format=lambda record: formatter(record, format_info))
    logger.add(sys.stdout, colorize=True, format=lambda record: formatter(record, {
        "DEBUG": format_info,
        "INFO": format_info,
        "WARNING": format_error,
        "ERROR": format_error,
        "CRITICAL": format_error,
        "SUCCESS": format_sus
    }[record["level"].name]))








logging_setup()

