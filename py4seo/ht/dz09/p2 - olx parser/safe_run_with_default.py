import logging


def safe_run_with_default(func, default_value):
    try:
        return func()
    except Exception as e:
        logging.debug(f"Some error on safe evaling: {e}")
        return default_value
