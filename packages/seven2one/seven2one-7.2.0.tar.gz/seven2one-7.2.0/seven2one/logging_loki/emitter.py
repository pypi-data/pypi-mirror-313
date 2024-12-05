# -*- coding: utf-8 -*-

import abc
import copy
from datetime import datetime, timedelta
import functools
import logging
import time
from logging.config import ConvertingDict
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from oauthlib.oauth2 import BackendApplicationClient
import requests
from requests_oauthlib import OAuth2Session
import rfc3339

from ..utils.ut_auth import AuthData

from . import const

BasicAuth = Optional[Tuple[str, str]]


class LokiEmitter(abc.ABC):
    """Base Loki emitter class."""

    success_response_code = const.success_response_code
    level_tag = const.level_tag
    logger_tag = const.logger_tag
    label_allowed_chars = const.label_allowed_chars
    label_replace_with = const.label_replace_with
    session_class = requests.Session
    auth_data: AuthData = None


    def __init__(self, url: str, tags: Optional[dict] = None, auth: BasicAuth = None, token: str = None):
        """
        Create new Loki emitter.

        Arguments:
            url: Endpoint used to send log entries to Loki (e.g. `https://my-loki-instance/loki/api/v1/push`).
            tags: Default tags added to every log record.
            auth: Optional tuple with username and password for basic HTTP authentication.

        """
        #: Tags that will be added to all records handled by this handler.
        self.tags = tags or {}
        #: Loki JSON push endpoint (e.g `http://127.0.0.1/loki/api/v1/push`)
        self.url = url
        #: Optional tuple with username and password for basic authentication.
        self.auth = auth

        #: Optional bearer token for authorization header
        self.token = token

        self._session: Optional[requests.Session] = None

    def __call__(self, record: logging.LogRecord, line: str):
        """Send log record to Loki."""
        payload = self.build_payload(record, line)
        resp = self.session.post(self.url, json=payload)
        if resp.status_code != self.success_response_code:
            raise ValueError("Unexpected Loki API response status code: {0}".format(resp.status_code))

    @abc.abstractmethod
    def build_payload(self, record: logging.LogRecord, line) -> dict:
        """Build JSON payload with a log entry."""
        raise NotImplementedError  # pragma: no cover

    @property
    def session(self) -> OAuth2Session:
        """Create HTTP session."""
        def token_updater(new_token):
            self.auth_data.token = new_token
        if self._session is None:
            self._session = OAuth2Session(self.auth_data.client_id, 
                                          token=self.auth_data.token,
                                          auto_refresh_url=self.auth_data.token_url,
                                          auto_refresh_kwargs={'client_id': self.auth_data.client_id},
                                          token_updater=token_updater)
            self._session.auth = self.auth or None
        elif self.auth_data:
            expires_at = datetime.fromtimestamp(self.auth_data.token['expires_at'])
            if expires_at - timedelta(minutes=1) < datetime.now():
                if self.auth_data.service_account_secret is None:
                    extra = { 'client_id': self.auth_data.client_id }
                    self.auth_data.token = OAuth2Session(self.auth_data.client_id, token=self.auth_data.token).refresh_token(
                        self.auth_data.token_url, **extra)
                else:
                     # login with service account returns no refresh token so we need a new login
                    app_client = BackendApplicationClient(client_id=self.auth_data.client_id)
                    self._session = OAuth2Session(client=app_client)
                    self.auth_data.token = self._session.fetch_token(token_url=self.auth_data.token_url, 
                                                            client_id=self.auth_data.client_id, 
                                                            username=self.auth_data.service_account_name, 
                                                            password=self.auth_data.service_account_secret)
                    #self._session.headers.update({'Authorization': "Bearer " + self.auth_data.token['access_token']})

        if self.token is not None:
            self._session.headers.update({'Authorization': "Bearer " + self.token})
        return self._session

    def close(self):
        """Close HTTP session."""
        if self._session is not None:
            self._session.close()
            self._session = None

    @functools.lru_cache(const.format_label_lru_size)
    def format_label(self, label: str) -> str:
        """
        Build label to match prometheus format.

        `Label format <https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels>`_
        """
        for char_from, char_to in self.label_replace_with:
            label = label.replace(char_from, char_to)
        return "".join(char for char in label if char in self.label_allowed_chars)

    def build_tags(self, record: logging.LogRecord) -> Dict[str, Any]:
        """Return tags that must be send to Loki with a log record."""
        tags = dict(self.tags) if isinstance(self.tags, ConvertingDict) else self.tags
        tags = copy.deepcopy(tags)
        tags[self.level_tag] = record.levelname.lower()
        tags[self.logger_tag] = record.name

        extra_tags = getattr(record, "tags", {})
        if not isinstance(extra_tags, dict):
            return tags

        for tag_name, tag_value in extra_tags.items():
            cleared_name = self.format_label(tag_name)
            if cleared_name:
                tags[cleared_name] = tag_value

        return tags


class LokiEmitterV0(LokiEmitter):
    """Emitter for Loki < 0.4.0."""

    def build_payload(self, record: logging.LogRecord, line) -> dict:
        """Build JSON payload with a log entry."""
        labels = self.build_labels(record)
        ts = rfc3339.format_microsecond(record.created)
        stream = {
            "labels": labels,
            "entries": [{"ts": ts, "line": line}],
        }
        return {"streams": [stream]}

    def build_labels(self, record: logging.LogRecord) -> str:
        """Return Loki labels string."""
        labels: List[str] = []
        for label_name, label_value in self.build_tags(record).items():
            cleared_name = self.format_label(str(label_name))
            cleared_value = str(label_value).replace('"', r"\"")
            labels.append('{0}="{1}"'.format(cleared_name, cleared_value))
        return "{{{0}}}".format(",".join(labels))


class LokiEmitterV1(LokiEmitter):
    """Emitter for Loki >= 0.4.0."""

    def build_payload(self, record: logging.LogRecord, line) -> dict:
        """Build JSON payload with a log entry."""
        labels = self.build_tags(record)
        ns = 1e9
        ts = str(int(time.time() * ns))
        stream = {
            "stream": labels,
            "values": [[ts, line]],
        }
        return {"streams": [stream]}
