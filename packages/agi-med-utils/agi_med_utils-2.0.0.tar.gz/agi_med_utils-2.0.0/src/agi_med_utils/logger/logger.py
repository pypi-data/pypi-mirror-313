import sys
from uuid import UUID

from loguru import logger

from . import LogLevelEnum


def logger_init(
    log_level: LogLevelEnum, service_name: str, include_outer_context: bool = True, include_extra_uuid: bool = True
) -> None:
    logger.remove()
    default_uuid = UUID(int=0)
    format_ = f"{{time:dd-MM-YYYY HH:mm:ss:ms}} | {service_name} | {{extra[uuid]}}"
    extra: dict[str, UUID | str] = {"uuid": default_uuid}
    if include_outer_context:
        format_ = f"{format_} | {{extra[outer_context]}}"
        extra["outer_context"] = default_uuid
    if include_extra_uuid:
        format_ = f"{format_} | {{extra[extra_uuid]}}"
        extra["extra_uuid"] = default_uuid
    format_ = f"{format_} | <level>{{message}}</level>"
    logger.add(sys.stdout, colorize=True, format=format_, level=log_level)
    logger.configure(extra=extra)


def log_llm_error(
    text: str | None = None,
    vector: list[float] | None = None,
    model: str = "gigachat",
) -> None:
    if text is not None and not text:
        logger.error(f"No response from {model}!!!")
        return None
    if vector is not None and all(not item for item in vector):
        logger.error(f"No response from {model} encoder!!!")
        return None
    return None
