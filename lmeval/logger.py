import logging as log

def set_log_level(level: str):
    if level.upper() == "DEBUG":
        log.basicConfig(level=log.DEBUG)
    elif level.upper() == "INFO":
        log.basicConfig(level=log.INFO)
    elif level.upper() == "WARNING":
        log.basicConfig(level=log.WARNING)
    elif level.upper() == "ERROR":
        log.basicConfig(level=log.ERROR)
    elif level.upper() == "CRITICAL":
        log.basicConfig(level=log.CRITICAL)
    else:
        log.basicConfig(level=log.INFO)
        log.warning(f"Invalid log level: {level}. Using INFO instead.")
