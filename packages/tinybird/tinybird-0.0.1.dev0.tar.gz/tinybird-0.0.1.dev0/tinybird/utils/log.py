import logging
import logging.config

import tornado.log
import tornado.options

DEBUG_FORMAT = "%(asctime)-15s [%(levelname)8s] %(threadName)s %(message)s"

DEFAULT_LOGGING = {
    "version": 1,
    "filters": {
        "add_app_name": {
            "()": "tinybird.utils.log.ContextFilter",
        },
    },
    "formatters": {
        "tinybird": {
            "format": 'level="%(levelname)s" appName="%(app_name)s" threadName="%(threadName)s" filename="%(filename)s" function="%(funcName)s" message="%(message)s"',
        },
        "tb.web.access": {
            "format": 'level="%(levelname)s" appName="%(app_name)s" threadName="%(threadName)s" filename="%(filename)s" function="%(funcName)s" method="%(method)s" status_code="%(status_code)s" remote_ip="%(remote_ip)s" endpoint="%(endpoint)s" request_id="%(request_id)s" nginx_request_id="%(nginx_request_id)s" message="%(message)s"'
        },
    },
    "handlers": {
        "console": {
            "filters": ["add_app_name"],
            "class": "logging.StreamHandler",
            "formatter": "tinybird",
        },
        "tb.web.access": {
            "filters": ["add_app_name"],
            "class": "logging.StreamHandler",
            "formatter": "tb.web.access",
        },
    },
    "loggers": {
        "tb.web.access": {
            "handlers": ["tb.web.access"],
            "level": "INFO",  # Because we use the root logger everywhere we need to disable propagation on our custom logger otherwise logs will be emitted twice.
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


def configure_logging(app_name: str, debug: bool) -> None:
    ContextFilter.set_app_name(app_name)

    tornado_options = tornado.options.options
    tornado_options.logging = "info"
    tornado.log.enable_pretty_logging(options=tornado_options)

    logging.config.dictConfig(DEFAULT_LOGGING)

    # Use a Loki-friendly and more verbose logging format in production where we have proper app names,
    # but a simpler and more developer-friendly format during development.
    if debug:
        # Modify tornado options for logging
        tornado_options.logging = "debug"

        # Modify the root logger
        logging.root.setLevel(logging.DEBUG)
        for handler in logging.root.handlers:
            handler.setFormatter(logging.Formatter(DEBUG_FORMAT))

        # Modify the rest of the loggers
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for logger in loggers:
            if logger.name != "tornado.curl_httpclient":
                logger.setLevel(logging.DEBUG)
            if logger.name == "tb.web.access":
                for handler in logger.handlers:
                    handler.setFormatter(logging.Formatter(DEBUG_FORMAT))


class ContextFilter(logging.Filter):
    app_name = "unknown"

    @classmethod
    def set_app_name(cls, app_name: str):
        cls.app_name = app_name

    def filter(self, record):
        record.app_name = self.app_name
        return True
