import logging


class LoggingOptions:
    format: str | None = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    level: str | None = "info"


def setup_logging(option: LoggingOptions):
    log_format = option.format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, option.level.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
        ],
    )

    # root_logger = logging.getLogger()
    # log_file = settings.LOGGING_PATH
    # if log_file:
    #     file_handler = logging.FileHandler(log_file)
    #     file_handler.setLevel(root_logger.level)
    #     file_handler.setFormatter(logging.Formatter(log_format))
    #     root_logger.addHandler(file_handler)

    # if settings.LOKI_ENDPOINT:
    #     print(
    #         f"use loki logging handler: {settings.LOKI_USER},{settings.LOKI_ENDPOINT}"
    #     )
    #     if not settings.GRAFANA_TOKEN:
    #         print("missing GRAFANA_TOKEN, skip setup loki")
    #     else:
    #         import logging_loki

    #         handler = logging_loki.LokiHandler(
    #             url=settings.LOKI_ENDPOINT,
    #             tags={
    #                 "application": settings.app_name,
    #                 "deploy": settings.otel_deploy_name,
    #             },
    #             auth=(settings.LOKI_USER, settings.GRAFANA_TOKEN),
    #             version="1",
    #         )
    #         root_logger.addHandler(handler)

    # if settings.IS_TRACE_HTTPX:
    #     httpx_logger = logging.getLogger("httpx")
    #     httpx_logger.setLevel(logging.INFO)
