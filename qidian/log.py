import logging
import sys
import coloredlogs
import os

FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='green', bold=coloredlogs.CAN_USE_BOLD_FONT),
    module=dict(color='magenta'),
    name=dict(color='blue'),
    threadName=dict(color='green')
)

LEVEL_STYLES = dict(
    debug=dict(color='green'),
    info=dict(color='cyan'),
    warning=dict(color='yellow'),
    error=dict(color='red'),
    critical=dict(color='red', bold=coloredlogs.CAN_USE_BOLD_FONT)
)
PROMPT_LEVEL = os.getenv("LOGLEVEL", "WARNING")

# 参考 https://stackoverflow.com/questions/6614078/logging-setlevel-how-it-works
# logger 的等级是第一优先级，所以设为最低

logger = logging.getLogger("qidian")
logger.setLevel("DEBUG")
coloredlogs.install(
    fmt="[{levelname:^8}] [{asctime}] [{module}:{lineno}] {message}",
    style="{",
    level_styles=LEVEL_STYLES,
    field_styles=FIELD_STYLES,
    logger=logger
)
logger.handlers[0].setLevel(PROMPT_LEVEL)
_hdlr = logging.FileHandler("backupqidian.log", "at", "utf-8")
_hdlr.setFormatter(
    logging.Formatter(
        fmt="[{levelname:<8}] [{asctime}] [{pathname}:{lineno}] {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
_hdlr.setLevel("DEBUG")
logger.addHandler(_hdlr)
