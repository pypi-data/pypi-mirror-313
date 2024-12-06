import logging

import streamlit as st

from st_iframe_postmessage import st_iframe_postmessage


def create_test_logger(
        name: str = "st-iframe-postmessage-logger",
        log_level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":

    st.title("Iframe postMessage")
    st_iframe_postmessage(message={'event': "LOAD_COMPLETE"}, console_log=True, logger=create_test_logger())
