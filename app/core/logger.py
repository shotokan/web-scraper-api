import logging


def get_logger(name: str = "scrapper-app") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.hasHandlers():  # Evitar añadir múltiples handlers
        logger.setLevel(logging.INFO)

        # Formato y manejadores
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Logger global
app_logger = get_logger()
