import logging
import os
from logging import Logger

import streamlit.components.v1 as components

_RELEASE = True

if os.getenv('_ST_IFRAME_POSTMESSAGE_NOT_RELEASE_'):
    _RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_iframe_postmessage",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_iframe_postmessage", path=build_dir)


def st_iframe_postmessage(
        message: str | dict,
        target_origin: str = "*",
        console_log: bool = False,
        logger: Logger = None,
        logger_level=logging.INFO,
):
    """

    Parameters
    ----------
    message: str|dict
        message to be sent
    target_origin: str
        target origin for post message
        defaults to "*" - for security reason change
    console_log: bool
        logs message to console to console log
    logger: Logger
        Python logger instance
    logger_level: int
        Python logger logging level
    Returns
    -------
    None
    """
    component_value = _component_func(
        message=message,
        target_origin=target_origin,
        console_log=console_log,
        default=None,
    )
    if logger:
        logger.log(level=logger_level, msg=f"message: {message}, target_origin: {target_origin}")

    return component_value
