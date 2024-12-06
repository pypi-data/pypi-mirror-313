# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from superlinked.framework.common.logging import LoggerConfigurator
from superlinked.framework.common.util.custom_structlog_processor import (
    CustomStructlogProcessor,
)

from superlinked.server.configuration.app_config import AppConfig


class ServerLoggerConfigurator:
    @staticmethod
    def setup_logger(app_config: AppConfig, logs_to_suppress: list[str] | None = None) -> None:
        processors = LoggerConfigurator._get_structlog_processors(  # noqa:SLF001 Private member
            app_config.JSON_LOG_FILE, app_config.EXPOSE_PII, app_config.LOG_AS_JSON
        )
        processors += [CustomStructlogProcessor.drop_color_message_key]  # Drop color must be the last processor
        LoggerConfigurator.configure_structlog_logger(
            app_config.JSON_LOG_FILE,
            processors,
            app_config.EXPOSE_PII,
            app_config.LOG_AS_JSON,
        )

        logging.getLogger("").setLevel(app_config.LOG_LEVEL)

        for _log in logs_to_suppress or []:
            logging.getLogger(_log).setLevel(logging.WARNING)

        # Disable uvicorn logging
        for _log in ["uvicorn", "uvicorn.error"]:
            logging.getLogger(_log).handlers.clear()
            logging.getLogger(_log).propagate = True

        logging.getLogger("uvicorn.access").handlers.clear()
        logging.getLogger("uvicorn.access").propagate = False
