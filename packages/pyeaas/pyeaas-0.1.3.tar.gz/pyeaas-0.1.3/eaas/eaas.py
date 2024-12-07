from flask import Flask, request
from flask_restx import Api, Namespace
from flask_cors import CORS
from eaas.api import liveness_ns
from gunicorn.app.base import BaseApplication
import logging


class Eaas:
    def __init__(self, logger:logging.Logger | bool | None = None, *args, **kwargs):
        self.logger = self.__get_logger(logger)
        name = kwargs.get('name', __name__)
        version = kwargs.get('version', '1.0')
        title = kwargs.get('title', 'API')
        description = kwargs.get('description', 'A simple API')
        doc=kwargs.get('doc', '/swagger')
        self.app = Flask(name)
        CORS(self.app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        self.api = Api( self.app, version=version, title=title, description=description, doc=doc)
        self.app.before_request(self.__log_request)

    def __get_logger(self, logger:logging.Logger | bool | None) -> logging.Logger | None:
        if logger is None:
            return None
        if isinstance(logger, bool):
            if logger:
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s'
                )
                return logging.getLogger(__name__)
            return None
        return logger

    def __log_request(self):
        if self.logger: self.logger.info(
            f'{request.method} {request.endpoint} {request.remote_addr} {request.user_agent}'
        )

    def run(self):
        self.app.run()

    def add_default_namespaces(self):
        self.api.add_namespace(liveness_ns)

    def add_namespace(self, namespace: Namespace):
        self.api.add_namespace(namespace)

    def create_app(self):
        return self.app


class GunEaas(BaseApplication):
    def __init__(self, app: Flask, options: dict | None = None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if self.cfg is not None and key in self.cfg.settings and value is not None}
        if self.cfg is not None:
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
