import pathlib

from loguru import logger  # noqa

from ambient_client_common.config import settings  # noqa

home_path = pathlib.Path.home()

logger.remove()
logger.add(
    home_path / ".ambient" / "logs" / "ambientctl.log",
    level=settings.ambient_log_level,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    rotation=settings.log_rotation,
    retention=5,
    serialize=True,
)
