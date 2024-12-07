from __future__ import annotations

import os
from typing import TYPE_CHECKING

import py_scibec
from dotenv import dotenv_values
from py_scibec import SciBecCore

from bec_lib import messages
from bec_lib.connector import ConnectorBase
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_server.scihub.repeated_timer import RepeatedTimer

from .config_handler import ConfigHandler
from .scibec_metadata_handler import SciBecMetadataHandler

if TYPE_CHECKING:
    from bec_server.scihub import SciHub

logger = bec_logger.logger


class SciBecConnectorError(Exception):
    pass


class SciBecConnector:
    token_expiration_time = 86400  # one day

    def __init__(self, scihub: SciHub, connector: ConnectorBase) -> None:
        self.scihub = scihub
        self.connector = connector
        self.scibec = None
        self.host = None
        self.target_bl = None
        self.ingestor = None
        self.ingestor_secret = None
        self.ro_user = None
        self.ro_user_secret = None
        self._env_configured = False
        self.scibec_info = {}
        self._config_request_handler = None
        self._metadata_handler = None
        self.config_handler = None
        self._scibec_account_thread = None
        self._start(connector)

    def _start(self, connector: ConnectorBase):
        self.connect_to_scibec()
        self.config_handler = ConfigHandler(self, connector)
        self._start_config_request_handler()
        self._start_metadata_handler()
        self._start_scibec_account_update()

    @property
    def config(self):
        """get the current service config"""
        return self.scihub.config

    def _load_environment(self):
        env_base = self.scihub.config.service_config.get("scibec", {}).get("env_file", "")
        env_file = os.path.join(env_base, ".env")
        if not os.path.exists(env_file):
            # check if there is an env file in the parent directory
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            env_file = os.path.join(current_dir, ".env")
            if not os.path.exists(env_file):
                return

        config = dotenv_values(env_file)
        self._update_config(**config)

    def _update_config(
        # pylint: disable=invalid-name
        self,
        SCIBEC_HOST: str = None,
        SCIBEC_TARGET: str = None,
        SCIBEC_INGESTOR: str = None,
        SCIBEC_INGESTOR_SECRET: str = None,
        SCIBEC_RO_USER: str = None,
        SCIBEC_RO_USER_SECRET: str = None,
        **kwargs,
    ) -> None:
        self.host = SCIBEC_HOST
        self.target_bl = SCIBEC_TARGET
        self.ingestor = SCIBEC_INGESTOR
        self.ingestor_secret = SCIBEC_INGESTOR_SECRET
        self.ro_user = SCIBEC_RO_USER
        self.ro_user_secret = SCIBEC_RO_USER_SECRET

        if (
            self.host
            and self.target_bl
            and self.ingestor
            and self.ingestor_secret
            and self.ro_user
            and self.ro_user_secret
        ):
            self._env_configured = True

    def _start_scibec_account_update(self) -> None:
        """
        Start a repeated timer to update the scibec account in redis
        """
        if not self._env_configured:
            return
        if not self.scibec:
            return
        try:
            self._scibec_account_update()
            self.scibec.login(username=self.ingestor, password=self.ingestor_secret)
        except Exception as exc:
            logger.warning(f"Could not connect to SciBec: {exc}")
            return
        logger.info("Starting SciBec account update timer.")
        self._scibec_account_thread = RepeatedTimer(
            self.token_expiration_time, self._scibec_account_update
        )

    def _scibec_account_update(self):
        """
        Update the scibec account in redis
        """
        logger.info("Updating SciBec account.")
        token = self.scibec.get_new_token(username=self.ro_user, password=self.ro_user_secret)
        if token:
            self.set_scibec_account(token)

    def set_scibec_account(self, token: str) -> None:
        """
        Set the scibec account in redis
        """
        self.connector.set(
            MessageEndpoints.scibec(),
            messages.CredentialsMessage(credentials={"url": self.host, "token": f"Bearer {token}"}),
        )

    def set_redis_config(self, config):
        msg = messages.AvailableResourceMessage(resource=config)
        self.connector.set(MessageEndpoints.device_config(), msg)

    def _start_metadata_handler(self) -> None:
        self._metadata_handler = SciBecMetadataHandler(self)

    def _start_config_request_handler(self) -> None:
        self._config_request_handler = self.connector.register(
            MessageEndpoints.device_config_request(),
            cb=self._device_config_request_callback,
            parent=self,
        )

    @staticmethod
    def _device_config_request_callback(msg, *, parent, **_kwargs) -> None:
        logger.info(f"Received request: {msg}")
        parent.config_handler.parse_config_request(msg.value)

    def connect_to_scibec(self):
        """
        Connect to SciBec and set the connector to the write account
        """
        self._load_environment()
        if not self._env_configured:
            logger.warning("No environment file found. Cannot connect to SciBec.")
            return
        try:
            self._update_scibec_instance()
            self._update_experiment_info()
            self._update_eaccount_in_redis()

        except Exception as exc:
            self.scibec = None
            logger.warning(f"Could not connect to SciBec: {exc}")

    def _update_scibec_instance(self):
        logger.info(f"Connecting to SciBec on {self.host}")
        self.scibec = SciBecCore(host=self.host)
        self.scibec.login(username=self.ingestor, password=self.ingestor_secret)

    def _update_experiment_info(self):
        bl_filter = py_scibec.bec.BeamlineFilterWhere(where={"name": self.target_bl})
        beamline_info = self.scibec.beamline.beamline_controller_find(bl_filter)
        if not beamline_info:
            raise SciBecConnectorError(f"Could not find a beamline with the name {self.target_bl}")
        self.scibec_info["beamline"] = beamline_info[0]
        experiment_id = beamline_info[0].active_experiment

        if not experiment_id:
            raise SciBecConnectorError(f"Could not find an active experiment on {self.target_bl}")

        experiment = self.scibec.experiment.experiment_controller_find_by_id(experiment_id)

        if not experiment:
            raise SciBecConnectorError(f"Could not find an experiment with the id {experiment_id}")
        self.scibec_info["activeExperiment"] = experiment

    def _update_eaccount_in_redis(self):
        write_account = self.scibec_info["activeExperiment"].write_account
        if write_account[0] == "p":
            write_account = write_account.replace("p", "e")
        msg = messages.VariableMessage(value=write_account)
        self.connector.set(MessageEndpoints.account(), msg)

    def shutdown(self):
        """
        Shutdown the SciBec connector
        """
        if self._scibec_account_thread:
            self._scibec_account_thread.stop()
        if self._config_request_handler:
            self._config_request_handler.shutdown()
        if self._metadata_handler:
            self._metadata_handler.shutdown()
