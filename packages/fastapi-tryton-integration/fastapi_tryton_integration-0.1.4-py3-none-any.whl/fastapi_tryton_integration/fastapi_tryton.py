# This file is part of fastapi_tryton_integration. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

""" Adds Tryton async support to FastAPI application.
* Tryton wrapper for Tryton objects
* tryton_transaction — a decorator for loading tryton context
"""

#__version__ = '0.1.2'
__all__ = [
    'Tryton',
    'tryton_transaction'
]


# standard modules
from functools import wraps
import time
import logging

# from tornado.options import define, options
from pydantic import BaseSettings
from fastapi.responses import JSONResponse

from trytond import __version__ as trytond_version
from trytond.config import config  
from trytond.exceptions import UserError, UserWarning, ConcurrencyException
from trytond.exceptions import RateLimitException  # Used to import and check within a third-party apps

# Initialize a logger
logger = logging.getLogger(__name__)
logger.info('Starting FastAPI-Tryton....!')

trytond_version = tuple(map(int, trytond_version.split('.')))


def retry_transaction(retry):
    """Decorator to retry a transaction if failed. The decorated method
    will be run retry times in case of DatabaseOperationalError.
    """
    from trytond import backend
    from trytond.transaction import Transaction
    try:
        DatabaseOperationalError = backend.DatabaseOperationalError
    except AttributeError:
        DatabaseOperationalError = backend.get('DatabaseOperationalError')

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for count in range(retry, -1, -1):
                try:
                    return await func(*args, **kwargs)
                except DatabaseOperationalError:
                    if count and not Transaction().readonly:
                        continue
                    raise
        return wrapper
    return decorator


class Settings(BaseSettings):
    """ Class that keep all settings """
    app_name: str = 'Awesome Tryton API'
    admin_email: str = ''
    items_per_user: int = 50
    extensions = {}
    config = {}
    url_map = {'converters': {}}


options = Settings()  # Used to import and update within a third-party apps


class Tryton(object):
    """Control Tryton integration to one or more FastAPI applications."""
    def __init__(self, app=None, configure_jinja=False):
        self.context_callback = None
        self.database_retry = None
        self.request_method = None
        self._configure_jinja = configure_jinja
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize an application for the use with this Tryton setup."""
        database = app.config.setdefault('TRYTON_DATABASE', None)
        user = app.config.setdefault('TRYTON_USER', 0)
        configfile = app.config.setdefault('TRYTON_CONFIG', None)
        dbase_config = app.config.setdefault('TRYTON_CONNECTION', None)

        config.update_etc(configfile)
        config['database']['uri'] = dbase_config if dbase_config else config['database']['uri']

        from trytond.pool import Pool
        from trytond.transaction import Transaction

        self.database_retry = config.getint('database', 'retry')
        self.pool = Pool(database)
        with Transaction().start(database, user, readonly=True):
            self.pool.init()
            
        app.extensions['Tryton'] = self

    def default_context(self, callback):
        """Set the callback for the default transaction context"""
        self.context_callback = callback
        return callback

    @property
    def language(self):
        """Return a language instance for the current request"""
        from trytond.transaction import Transaction
        Lang = self.pool.get('ir.lang')
        # Do not use Transaction.language as it fallbacks to default language
        language = Transaction().context.get('language')
        # TODO: add a languge support from a request
        # if not language:
        #     language = request.accept_languages.best_match(
        #         Lang.get_translatable_languages())
        return Lang.get(language)

    def format_date(self, value, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_date(value, lang, *args, **kwargs)

    def format_number(self, value, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_number(value, lang, *args, **kwargs)

    def format_currency(self, value, currency, lang=None, *args, **kwargs):
        from trytond.report import Report
        if lang is None:
            lang = self.language
        return Report.format_currency(value, lang, currency, *args, **kwargs)

    def format_timedelta(
            self, value, converter=None, lang=None, *args, **kwargs):
        from trytond.report import Report
        if not hasattr(Report, 'format_timedelta'):
            return str(value)
        if lang is None:
            lang = self.language
        return Report.format_timedelta(
            value, converter=converter, lang=lang, *args, **kwargs)

    def _readonly(self):
        return not (self.request_method 
                     and self.request_method in ('PUT', 'POST', 'DELETE', 'PATCH'))

    def transaction(self, readonly=None, user=None, context=None):
        """Decorator to run inside a Tryton transaction.
        The decorated method could be run multiple times in case of
        database operational error.

        If readonly is None then the transaction will be readonly except for
        PUT, POST, DELETE and PATCH request methods.

        If user is None then TRYTON_USER will be used.

        readonly, user and context can also be callable.
        """
        from trytond import backend
        from trytond.cache import Cache
        from trytond.transaction import Transaction
        try:
            DatabaseOperationalError = backend.DatabaseOperationalError
        except AttributeError:
            DatabaseOperationalError = backend.get('DatabaseOperationalError')

        def get_value(value):
            return value() if callable(value) else value

        def instanciate(value):
            if isinstance(value, _BaseProxy):
                return value()
            return value

        def decorator(func):
            """ Decorator to allow transactions without requiring `request`. """
            @retry_transaction(self.database_retry)
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                tryton = options.extensions['Tryton']
                database = options.config['TRYTON_DATABASE']
                transaction_user = get_value(user or options.config.get('TRYTON_USER'))
                transaction_context = context or {}

                try:
                    with Transaction().start(database, transaction_user, readonly=readonly, context=transaction_context):
                        result = await func(*map(instanciate, args), **{k: instanciate(v) for k, v in kwargs.items()})
                        return result
                except DatabaseOperationalError as db_error:
                    logger.error(f"Database operational error: {db_error}")
                    return JSONResponse(status_code=500, content={"error": "Database operational error"})
                except Exception as e:
                    logger.error(f"Error en la transacción: {e}")
                    return JSONResponse(status_code=500, content={"error": str(e)})
                finally:
                    logger.info(f"Total request time: {time.time() - start_time:.4f}s")
            return wrapper
        return decorator


tryton_transaction = Tryton.transaction


class _BaseProxy(object):
    pass


class _RecordsProxy(_BaseProxy):
    def __init__(self, model, ids):
        self.model = model
        self.ids = ids

    def __iter__(self):
        return iter(self.ids)

    def __call__(self):
        tryton = options.extensions['Tryton']
        Model = tryton.pool.get(self.model)
        return Model.browse(self.ids)


class _RecordProxy(_RecordsProxy):
    def __init__(self, model, id):
        super(_RecordProxy, self).__init__(model, [id])

    def __int__(self):
        return self.ids[0]

    def __call__(self):
        return super(_RecordProxy, self).__call__()[0]
