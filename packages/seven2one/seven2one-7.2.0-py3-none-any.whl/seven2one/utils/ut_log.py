import atexit
from loguru import logger

from .ut_auth import AuthData
from ..logging_loki import LokiQueueHandler, emitter
from . import __version__
from multiprocessing import Queue


class LogUtils():
    def _init_logging(
            url: str,
            auth_data: AuthData,
            log_level: str,
            sessionId: str,
            clientId: str = "S2O.TechStack.Python"):

        emitter.LokiEmitter.level_tag = "level"
        emitter.LokiEmitter.auth_data = auth_data
        handler = LokiQueueHandler(
            Queue(),
            url=url,
            tags={"client": clientId},
            version="1"
        )

        logger.add(handler, level=log_level, serialize=True,
                   backtrace=True, diagnose=True)
        logger.configure(extra={
            "version": __version__,
            "session_id": sessionId,
        })

        def _teardown_logging(handler):
            handler.listener.stop()

        atexit.register(_teardown_logging, handler)
