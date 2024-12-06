#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
import traceback
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from inspect import getfullargspec
from time import sleep
from typing import Optional, Union, Any
from urllib.parse import urlparse

from requests import Response, Session
from urllib3 import Retry

from . import RestOptions, HttpMethod, RestResponse, RestFul, Hooks, _utils, BaseRest, ApiAware, \
    BaseContextAware, BaseRestWrapper, StatsUrl, BaseContextBean
from ._constants import _OPTIONAL_ARGS_KEYS, _Constant, _HTTP_INFO_TEMPLATE
from .. import sjson as complexjson
from ..character import StringBuilder
from ..config.log import LogLevel
from ..config.rest import RestConfig
from ..converter import TimeUnit
from ..exceptions import HttpException, RestInternalException
from ..generic import T
from ..log import LoggerFactory
from ..maps import Dictionary
from ..serialize import Serializable, serializer
from ..utils.objects import ObjectsUtils
from ..utils.strings import StringUtils
from .._requests._hyper.contrib import HTTP20Adapter

__all__ = []

_LOGGER = LoggerFactory.get_logger("rest")


class RestBean(BaseContextBean):

    def __init__(self, tag: str, rest: BaseRest):
        self.__tag: str = tag
        self.__rest: BaseRest = rest
        self.__wrappers: dict[str, BaseRestWrapper] = {}

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def rest(self) -> BaseRest:
        return self.__rest

    @property
    def wrappers(self) -> dict[str, BaseRestWrapper]:
        return self.__wrappers

    def has_wrapper(self, tag: str = None, wrapper: BaseRestWrapper = None) -> bool:
        if tag is not None:
            wrap = self.__wrappers.get(tag)
            if wrap is not None:
                if wrapper is not None:
                    return wrap is wrapper
        else:
            if wrapper is not None:
                for wrap in self.wrappers.values():
                    if wrap is wrapper:
                        return True
        return False

    def get(self, tag: str, default: BaseRestWrapper = None) -> BaseRestWrapper:
        if default is not None and not isinstance(default, BaseRestWrapper):
            raise TypeError(f"'default' expected type '{BaseRestWrapper.__name__}', got a '{type(default).__name__}'")
        if not self.has_wrapper(tag, default):
            self.__wrappers[tag] = default
            return default
        return self.__wrappers.get(tag)

    def set(self, tag, wrapper: BaseRestWrapper):
        if not isinstance(wrapper, BaseRestWrapper):
            raise TypeError(f"'{tag}'\'s value '{wrapper}' expected type '{BaseRestWrapper.__name__}', "
                            f"got a '{type(wrapper).__name__}'")
        if self.has_wrapper(tag, wrapper):
            raise KeyError(f"wrapper tag '{tag}' exists in bean.")
        self.__wrappers[tag] = wrapper

    def set_all(self, **kwargs: BaseRestWrapper):
        for tag, wrapper in kwargs.items():
            self.set(tag, wrapper)

    def pop(self, tag) -> BaseRestWrapper:
        return self.__wrappers.pop(tag)

    def clean(self):
        self.__wrappers.clear()


class RestContext(BaseContextAware):

    def __init__(self):
        self.__beans: dict[str, BaseContextBean] = {}

    @property
    def beans(self) -> dict[str, BaseContextBean]:
        return self.__beans

    def add(self, tag, rest: BaseRest):
        if not isinstance(rest, BaseRest):
            raise TypeError(f"'{tag}'\'s value '{rest}' expected type '{BaseRest.__name__}', "
                            f"got a '{type(rest).__name__}'")
        if tag in self.__beans:
            raise KeyError(f"'{tag}' exists in context.")
        self.__beans[tag] = RestBean(tag, rest)

    def put(self, **kwargs: BaseRest):
        for k, v in kwargs.items():
            self.add(k, v)

    def update(self, rests: dict[str, BaseRest]):
        if not isinstance(rests, dict):
            raise TypeError(f"Expected type '{dict.__name__}', got a '{type(rests).__name__}'")
        self.put(**rests)

    def get(self, tag, default: BaseRest = None) -> BaseRest:
        if default is not None and not isinstance(default, BaseRest):
            raise TypeError(f"'default' expected type '{BaseRest.__name__}', got a '{type(default).__name__}'")
        if tag not in self.__beans:
            self.add(tag, default)
            return default
        return self.__beans.get(tag).rest

    def get_bean(self, tag) -> BaseContextBean:
        return self.__beans.get(tag)

    def pop(self, tag) -> BaseRest:
        return self.__beans.pop(tag).rest

    def builder(self, tag, /, name: str = None, host: str = None, headers: dict or Serializable = None,
                cookies: dict or Serializable = None, auth: tuple or Serializable = None,
                hooks: Hooks = None, show_len: int = None, http2: bool = False, check_status: bool = False,
                encoding: str = "utf-8", description: str = None, restful: dict or Serializable = None,
                retry_times: int = 10, retry_interval: int = 5, retry_exit_code_range: list = None,
                retry_exception_retry: bool = True, retry_check_handler: Callable[[Any], bool] = None,
                verify: bool = None, proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                trust_env: bool = True, max_redirects: int = 30, stats: bool = False) -> 'BaseRest':
        rest = Rest(name, host, headers, cookies, auth, hooks, show_len, http2, check_status, encoding, description,
                    restful, retry_times, retry_interval, retry_exit_code_range, retry_exception_retry,
                    retry_check_handler, verify, proxies, cert, trust_env, max_redirects, stats)
        self.add(tag, rest)
        return rest


class RestFast(object):
    """
    Quickly build a streaming HTTP request client.
    """

    def __init__(self, host, http2: bool = False, retry_times: int = 3, retry_backoff_factor: int = 5,
                 trust_env: bool = True, max_redirects: int = 30, **kwargs):
        self.__host: str = host
        self.__api: str = ""
        self.__opts: RestOptions = RestOptions()
        self.__method: HttpMethod = HttpMethod.OPTIONS
        self.__kw = kwargs
        self.__session: Session = Session()
        self.__session.trust_env = trust_env
        self.__session.max_redirects = max_redirects
        self.__resp: Optional[Response] = None
        retry = Retry(total=retry_times, backoff_factor=retry_backoff_factor)
        if http2:
            scheme = urlparse(self.__host).scheme
            if scheme != _Constant.HTTPS:
                raise HttpException(f"http2 need https protocol, but found '{scheme}'")
            self.__session.mount(f"{_Constant.HTTPS}://", HTTP20Adapter(max_retries=retry))

    def api(self, api: str) -> 'RestFast':
        """
        set server api
        """
        self.__api = api if api else ""
        return self

    def opts(self, opts: RestOptions) -> 'RestFast':
        """
        http request params, headers, data, json, files etc.
        """
        self.__opts = opts if opts else RestOptions()
        return self

    def method(self, method: Union[HttpMethod, str]) -> 'RestFast':
        """
        set http request method.
        """
        if isinstance(method, str):
            self.__method = HttpMethod.get_by_value(method.upper())
        elif isinstance(method, HttpMethod):
            self.__method = method
        else:
            raise HttpException(f"invalid http method: '{method}'")
        if not self.__method:
            raise HttpException(f"invalid http method: '{method}'")
        return self

    def send(self) -> 'RestFast':
        """
        send http request
        :return:
        """
        if StringUtils.is_empty(self.__api):
            _LOGGER.warning(f'api is empty')
        url = f"{self.__host}{self.__api}"
        self.__resp = None
        try:
            self.__resp = getattr(self.__session, self.__method.value.lower())(url=f"{url}",
                                                                               **self.__opts.opts_no_none, **self.__kw)
            return self
        finally:
            if self.__resp is not None:
                content = self.__resp.text if self.__resp else ""
                url_ = self.__resp.url if self.__resp.url else url
                msg = f"http fast request: url={url_}, method={self.__method}, " \
                      f"opts={self.__opts.opts_no_none}, response={StringUtils.abbreviate(content)}"
                _LOGGER.log(level=10, msg=msg, stacklevel=3)
            else:
                msg = f"http fast request no response: url={self.__host}{self.__api}, method={self.__method}, " \
                      f"opts={self.__opts.opts_no_none}"
                _LOGGER.log(level=10, msg=msg, stacklevel=3)
            self.__api = ""
            self.__opts = RestOptions()
            self.__method = HttpMethod.OPTIONS.value

    def response(self) -> RestResponse:
        """
        send request and get response.
        type_reference priority is greater than only_body.
        type_reference will return custom entity object.

        usage:
            type_reference example:

                @EntityType()
                class Data(Entity):
                    id: list[str]
                    OK: str
                    data: str

            response body:
                {"data":"data content","id":[1],"OK":"200"}



            resp = RestFast("http://localhost:8080").api("/hello").opts(RestOptions(params={"id": 1})).method("GET").send().response().to_entity(Data)
            print(resp)  # Data(id=[1], OK='200', data='data content')
        """
        return RestResponse(self.__resp)

    @staticmethod
    def bulk(content: str) -> dict:
        return RestWrapper.bulk(content)


class RestWrapper(BaseRestWrapper):
    """
    A simple http request frame.

    usage set BaseRest document.
    """

    def __init__(self, tag: str = None, wrapper_tag: str = None, rest: BaseRest = None, name: str = None, host: str = None,
                 headers: dict or Serializable = None, cookies: dict or Serializable = None,
                 auth: tuple or Serializable = None, hooks: Hooks = None, show_len: int = None,
                 http2: bool = False, check_status: bool = False, encoding: str = "utf-8", description: str = None,
                 restful: dict or Serializable = None, retry_times: int = 10, retry_interval: int = 5,
                 retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                 retry_check_handler: Callable[[Any], bool] = None, verify: bool = None,
                 proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                 trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        """
        Build a request client wrapper.
        It is recommended to use the context after the 'tag' parameter tag to manage REST objects
        """
        self.__tag: str = tag
        self.__wrapper_tag: str = wrapper_tag
        if isinstance(rest, BaseRest):
            self.__rest = rest
        else:
            self.__rest = Rest(name=name, host=host, headers=headers, cookies=cookies, auth=auth,
                               hooks=hooks, check_status=check_status, encoding=encoding, description=description,
                               restful=restful, http2=http2, retry_times=retry_times, retry_interval=retry_interval,
                               retry_exit_code_range=retry_exit_code_range, show_len=show_len,
                               retry_exception_retry=retry_exception_retry, retry_check_handler=retry_check_handler,
                               verify=verify, proxies=proxies, cert=cert, trust_env=trust_env,
                               max_redirects=max_redirects,
                               stats=stats)
        self.__rest_: Optional[BaseRest] = None
        self.__stats = stats
        self.__api_stats_do: StatsUrl = StatsUrl()

    @property
    def rest(self) -> BaseRest:
        if self.__rest_ is None:
            _LOGGER.warn("not found Rest by ApiWare, use RestWrapper default Rest.")
            return self.__rest
        return self.__rest_

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def wrapper_tag(self) -> str:
        return self.__wrapper_tag

    @property
    def api_stats_done(self) -> 'StatsUrl':
        return self.__rest_.api_stats_done if self.__rest_ else self.__rest.api_stats_done

    @property
    def api_stats_do(self) -> StatsUrl:
        return self.__api_stats_do

    def copy(self) -> 'BaseRestWrapper':
        return RestWrapper(self.tag, self.wrapper_tag, self.__rest_.copy())

    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__parser_rest(func, args)
                times_ = times if isinstance(times, int) else self.__rest_.retry_times
                interval_ = interval if isinstance(interval, int) else self.__rest_.retry_interval
                exit_code_range_ = exit_code_range if isinstance(exit_code_range,
                                                                 list) else self.__rest_.retry_exit_code_range
                ObjectsUtils.check_iter_type(exit_code_range_, int)
                exception_retry_ = exception_retry if isinstance(exception_retry,
                                                                 bool) else self.__rest_.retry_exception_retry
                check_handler_ = check_handler if callable(check_handler) else self.__rest_.retry_check_handler

                def default_check_body_call_back(res) -> bool:
                    if isinstance(res, RestResponse):
                        return res.code in exit_code_range_
                    else:
                        return True

                check_handler_ = check_handler_ if callable(check_handler_) else default_check_body_call_back
                number_ = times_ + 1
                for i in range(1, times_ + 2):
                    # noinspection PyBroadException
                    try:
                        resp = func(*args, **kwargs)
                        if check_handler_(resp):
                            return resp
                        if i == number_:
                            break
                        else:
                            _LOGGER.log(level=30, msg=f"http request retry times: {i}", stacklevel=3)
                            sleep(interval_)
                    except BaseException as e:
                        if isinstance(e, RestInternalException):
                            if exception_retry_:
                                if i == number_:
                                    break
                                else:
                                    _LOGGER.log(level=30, msg=f"http request retry times: {i}", stacklevel=3)
                                    sleep(interval_)
                            else:
                                return
                        else:
                            raise e
                else:
                    _LOGGER.log(level=40, msg=f"The maximum '{times_}' of HTTP request retries is reached",
                                stacklevel=3)

            return __wrapper

        return __inner

    def request(self, api: str, method: HttpMethod or str = None,
                allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, _utils.http_method_handler(method)))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=method,
                               allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def get(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.GET.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.GET,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def post(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.POST.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.POST,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def put(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.PUT.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.PUT,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def delete(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.DELETE.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.DELETE,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def patch(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.PATCH.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.PATCH,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def head(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.HEAD.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.HEAD,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def options(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        if self.__stats is True and stats is True:
            self.__api_stats_do.add((api, HttpMethod.OPTIONS.value))

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api=api, method=HttpMethod.OPTIONS,
                               allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                               encoding=encoding, description=description, restful=restful, stats=stats, hooks=hooks,
                               show_len=show_len, opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def __request(self, func, args, kwargs, **kw):
        self.__parser_rest(func, args)
        full_name = func.__qualname__
        if "." not in full_name:
            raise TypeError(f"Expected instance method, not a function: {func}")
        class_name = full_name.split(".")[0]
        spec = getfullargspec(func)
        func_name = func.__name__
        if "response" not in spec.args and "response" not in spec.kwonlyargs:
            raise HttpException(f"function {func_name} need 'response' args, ex: {func_name}(self, response) "
                                f"or {func_name}(self, response=None)")
        stacklevel = 5
        for i, stack in enumerate(inspect.stack()):
            if not stack:
                continue
            code_context = stack.code_context
            if not code_context:
                continue
            for content in stack.code_context:
                if class_name in content and func_name in content:
                    stacklevel = i + 3
                    break
        kw['stacklevel'] = stacklevel
        resp = getattr(self.__rest_, f"_{self.__rest_.__class__.__name__}__request")(func=func, **kw)
        kwargs['response'] = resp

    def __parser_rest(self, func, args):
        if self.__rest_ is None:
            bean: Optional[BaseContextBean] = None
            if inspect.ismethod(func) and isinstance(api_aware := func.__self__, ApiAware):
                bean: BaseContextBean = api_aware.context.get_bean(self.tag)
            elif len(args) > 0 and isinstance(api_aware := args[0], ApiAware):
                bean: BaseContextBean = api_aware.context.get_bean(self.tag)
            if bean:
                if not bean.has_wrapper(self.wrapper_tag, self) and self.wrapper_tag is not None:
                    bean.set(self.wrapper_tag, self)
                self.__rest_ = bean.rest
            else:
                self.__rest_ = self.__rest

    @staticmethod
    def bulk(content: str) -> dict:
        return _utils.bulk_header(content)


class Rest(BaseRest):
    """
    A simple http request frame.
    """

    def __init__(self, name: str = None, host: str = None, headers: dict or Serializable = None,
                 cookies: dict or Serializable = None, auth: tuple or Serializable = None,
                 hooks: Hooks = None, show_len: int = None, http2: bool = False, check_status: bool = False,
                 encoding: str = "utf-8", description: str = None, restful: dict or Serializable = None,
                 retry_times: int = 10, retry_interval: int = 5, retry_exit_code_range: list = None,
                 retry_exception_retry: bool = True, retry_check_handler: Callable[[Any], bool] = None,
                 verify: bool = None, proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                 trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        """
        Build a request client.
        """
        self.__restful: dict or Serializable = None
        self.__check_status: Optional[bool] = None
        self.__encoding: Optional[str] = None
        self.__server_name: Optional[str] = None
        self.__server: Optional[dict[str, Any]] = None
        self.__host: Optional[str] = None
        self.__headers: Optional[dict[str, str], Serializable] = None
        self.__cookies: Optional[dict[str, str], Serializable] = None
        self.__auth: Optional[tuple, Serializable] = None
        self.__description: Optional[str] = None
        self.__http2: Optional[bool] = None
        self.__session: Optional[Session] = None
        self.__retry_times: Optional[int] = None
        self.__retry_interval: Optional[int] = None
        self.__retry_exit_code_range: Optional[list] = None
        self.__retry_exception_retry: Optional[bool] = None
        self.__retry_check_handler: Optional[Callable[[Any], bool]] = None
        self.__verify: Optional[bool] = None
        self.__proxies: Optional[dict, Serializable] = None
        self.__hooks: Optional[Hooks] = None
        self.__show_len: Optional[int] = None
        self.__cert: str or tuple or Serializable = None
        self.__stats: bool = False
        self.__api_stats_done: Optional[StatsUrl] = None
        self.__initialize(name=name, host=host, headers=headers, cookies=cookies, auth=auth, hooks=hooks,
                          check_status=check_status, encoding=encoding, description=description, restful=restful,
                          http2=http2, retry_times=retry_times, retry_interval=retry_interval,
                          retry_exit_code_range=retry_exit_code_range, show_len=show_len,
                          retry_exception_retry=retry_exception_retry, retry_check_handler=retry_check_handler,
                          verify=verify, proxies=proxies, cert=cert, trust_env=trust_env, max_redirects=max_redirects,
                          stats=stats)

    def __initialize(self, name: str = None, host: str = None, headers: dict[str, str] or Serializable = None,
                     cookies: dict[str, str] or Serializable = None, auth: tuple or Serializable = None,
                     hooks: Hooks = None, show_len: int = None, check_status: bool = False,
                     encoding: str = "utf-8", description: str = None, restful: dict or Serializable = None,
                     http2: bool = False, retry_times: int = 10, retry_interval: int = 5,
                     retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                     retry_check_handler: Callable[[Any], bool] = None, verify: bool = False,
                     proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                     trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        self.__api_stats_done: Optional[StatsUrl] = StatsUrl()
        self.__restful = serializer(restful or RestFul())
        self.__check_status: bool = check_status if isinstance(check_status, bool) else False
        self.__encoding: str = encoding if isinstance(encoding, str) else "utf-8"
        self.__server_name: str = name
        self.__host: str = host
        self.__headers: dict[str, str] = serializer(headers) or {}
        self.__cookies: dict[str, str] = serializer(cookies) or {}
        self.__auth: tuple = serializer(auth) or ()
        self.__description: str = description
        self.__http2: bool = http2 if isinstance(http2, bool) else False
        self.__retry_times: int = retry_times if isinstance(retry_times, int) else 10
        self.__retry_interval: int = retry_interval if isinstance(retry_interval, int) else 5

        self.__retry_exit_code_range: int = retry_times if isinstance(retry_exit_code_range, list) else (i for i in
                                                                                                         range(200,
                                                                                                               300))
        self.__retry_exception_retry: int = retry_times if isinstance(retry_exception_retry, bool) else True
        self.__retry_check_handler: Callable[[Any], bool] = retry_check_handler
        self.__verify: bool = verify
        self.__proxies: dict or Serializable = serializer(proxies)
        self.__hooks: Optional[Hooks] = hooks if isinstance(hooks, Hooks) else Hooks()
        self.__show_len: int = _utils.get_show_len(show_len, None, None)
        self.__cert: str or tuple or Serializable = serializer(cert)
        self.__stats: bool = stats
        self.__session: Session = Session()
        self.__session.trust_env = trust_env if isinstance(trust_env, bool) else True
        self.__session.max_redirects = max_redirects if isinstance(max_redirects, int) else 30
        if http2:
            scheme = urlparse(self.__host).scheme
            if scheme != _Constant.HTTPS:
                raise HttpException(f"http2 need https protocol, but found '{scheme}'")
            self.__session.mount(f"{_Constant.HTTPS}://", HTTP20Adapter())

    @property
    def restful(self) -> RestFul:
        return self.__restful

    @restful.setter
    def restful(self, restful: RestFul):
        if not issubclass(t := type(restful), RestFul):
            raise TypeError(f"Excepted type is 'RestFul', got a '{t.__name__}'")
        self.__restful = restful

    @property
    def check_status(self) -> bool:
        return self.__check_status

    @check_status.setter
    def check_status(self, value):
        if isinstance(value, bool):
            self.__check_status = value
        else:
            raise TypeError(f"Excepted type is 'bool', got a '{type(value).__name__}'")

    @property
    def encoding(self) -> str:
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        if issubclass(value_type := type(value), str):
            self.__encoding = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def name(self) -> str:
        return self.__server_name

    @name.setter
    def name(self, value):
        if issubclass(value_type := type(value), str):
            self.__server_name = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value):
        if issubclass(value_type := type(value), str):
            self.__host = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value):
        if issubclass(value_type := type(value), str):
            self.__description = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def verify(self) -> str or bool:
        return self.__verify

    @verify.setter
    def verify(self, verify: str or bool):
        if not issubclass(t := type(verify), (str, bool)):
            raise TypeError(f"Excepted type is 'str' or 'bool', got a '{t.__name__}'")
        self.__verify = verify

    @property
    def headers(self) -> dict:
        return self.__headers

    @headers.setter
    def headers(self, headers: dict):
        if not issubclass(t := type(headers), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'.")
        self.__headers.update(headers)

    @property
    def cookies(self) -> dict:
        return self.__cookies

    @cookies.setter
    def cookies(self, cookies: dict):
        if not issubclass(t := type(cookies), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'.")
        self.__cookies = cookies

    @property
    def auth(self) -> tuple:
        return self.__auth

    @auth.setter
    def auth(self, auth: tuple):
        if not issubclass(t := type(auth), (tuple, list)):
            raise TypeError(f"Excepted type is 'tuple' or 'list', got a '{t.__name__}'.")
        self.auth = auth

    @property
    def hooks(self) -> Hooks:
        return self.__hooks

    @hooks.setter
    def hooks(self, hooks: Hooks):
        if not isinstance(hooks, Hooks):
            raise TypeError(f"Excepted type is 'Hooks', got a '{type(hooks).__name__}'.")
        if self.__hooks:
            self.__hooks.add_hook_before(hooks.before_hooks)
            self.__hooks.add_hook_after(hooks.after_hooks)
        else:
            self.__hooks = hooks

    @property
    def retry_times(self) -> int:
        return self.__retry_times

    @retry_times.setter
    def retry_times(self, retry_time: int):
        if not issubclass(t := type(retry_time), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        self.__retry_times = retry_time

    @property
    def retry_interval(self) -> int:
        return self.__retry_interval

    @retry_interval.setter
    def retry_interval(self, retry_interval: int):
        if not issubclass(t := type(retry_interval), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        self.__retry_interval = retry_interval

    @property
    def retry_exit_code_range(self) -> list:
        return self.__retry_exit_code_range

    @retry_exit_code_range.setter
    def retry_exit_code_range(self, retry_exit_code_range: list):
        if not issubclass(t := type(retry_exit_code_range), int):
            raise TypeError(f"Excepted type is 'list', got a '{t.__name__}'")
        self.__retry_exit_code_range = retry_exit_code_range

    @property
    def retry_exception_retry(self) -> bool:
        return self.__retry_exception_retry

    @retry_exception_retry.setter
    def retry_exception_retry(self, retry_exception_retry: bool):
        if not issubclass(t := type(retry_exception_retry), bool):
            raise TypeError(f"Excepted type is 'bool', got a '{t.__name__}'")
        self.__retry_exception_retry = retry_exception_retry

    @property
    def retry_check_handler(self) -> Callable[[Any], bool]:
        return self.__retry_check_handler

    @retry_check_handler.setter
    def retry_check_handler(self, retry_check_handler: Callable[[Any], bool]):
        if not issubclass(t := type(retry_check_handler), Callable):
            raise TypeError(f"Excepted type is 'callable', got a '{t.__name__}'")
        self.__retry_check_handler = retry_check_handler

    @property
    def proxies(self) -> dict:
        return self.__proxies

    @proxies.setter
    def proxies(self, proxies: dict):
        if not issubclass(t := type(proxies), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'")
        self.__proxies = proxies

    @property
    def cert(self) -> str or tuple:
        return self.__cert

    @cert.setter
    def cert(self, cert: str or tuple):
        if not issubclass(t := type(cert), (str, tuple)):
            raise TypeError(f"Excepted type is 'str' or 'tuple', got a '{t.__name__}'")
        self.__cert = cert

    @property
    def stats(self) -> bool:
        return self.__stats

    @stats.setter
    def stats(self, stats: bool):
        if not issubclass(t := type(stats), bool):
            raise TypeError(f"Excepted type is 'bool', got a '{t.__name__}'")
        self.__stats = stats

    @property
    def api_stats_done(self) -> 'StatsUrl':
        return self.__api_stats_done

    @property
    def show_len(self) -> int:
        return self.__show_len

    @show_len.setter
    def show_len(self, value: int):
        if not issubclass(t := type(value), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        if value < 0:
            raise ValueError(f"Excepted value great than 0, got a {value}")

        self.__show_len: int = value

    def copy(self) -> 'Rest':
        new = Rest()
        new.__dict__.update(self.__dict__)
        return new

    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        raise NotImplementedError()

    def request(self, api: str, method: HttpMethod or str = None,
                allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=method, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def get(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.GET, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def post(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.POST, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def put(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.PUT, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def delete(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.DELETE, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def patch(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.PATCH, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats, hooks=hooks, show_len=show_len, opts=opts)

    def head(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.HEAD, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def options(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api=api, method=HttpMethod.OPTIONS, allow_redirection=allow_redirection, headers=headers,
                              check_status=check_status, encoding=encoding, description=description, restful=restful,
                              stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def __request(self, api: str, func=None, method: HttpMethod or str = None, allow_redirection: bool = True,
                  headers: dict = None, check_status: bool = None, encoding: str = None, description: str = None,
                  restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
                  opts: RestOptions = None, **kwargs):
        if opts is None:
            opts = RestOptions()
        log_builder = StringBuilder()
        func_name = ""
        source_stack = inspect.stack()[1]
        stacklevel = 4
        if (inspect.ismethod(func) or inspect.isfunction(func)) and source_stack.filename == str(__file__) and \
                source_stack.function == "__request":
            func_name = f"<{func.__qualname__}>"
            stacklevel = kwargs.get("stacklevel", 5)
        _utils.build_log_message(log_builder, f' [{func_name}Request Start] '.center(81, '*'))
        method = _utils.http_method_handler(method)
        optional_args: dict = Dictionary(opts)
        optional_args[_Constant.ALLOW_REDIRECTS] = allow_redirection
        _utils.header_handler(optional_args, method.upper(), self.headers, headers, opts.get(_Constant.HEADERS))

        check_status_: bool = self.__check_status if not check_status else check_status
        _encoding: str = self.__encoding if not encoding else encoding
        req_args = {'auth': self.__auth, 'proxies': self.__proxies, 'cert': self.__cert, 'verify': self.__verify}
        _show_len = _utils.get_show_len(self.show_len, show_len, optional_args.get("show_len"))

        for k in list(optional_args.keys()):
            if k in _OPTIONAL_ARGS_KEYS:
                v = optional_args.pop(k)
                if v:
                    req_args[k] = serializer(v)
        _utils.cookies_handler(req_args, self.cookies, opts.get("cookies"))
        _utils.files_handler(req_args)
        resp: Optional[Response] = None
        start_time, end_time = None, None
        rest_resp = RestResponse(None)
        url: str = _utils.url_handler(self.host, api,
                                      _utils.restful_handler(self.restful, restful,
                                                             serializer(optional_args.pop(_Constant.RESTFUL, None)),
                                                             None))
        # noinspection PyBroadException
        try:
            req_args = _utils.run_before_hooks(self.__hooks, hooks or Hooks(),
                                               optional_args.get("hooks") or Hooks(), req_args)
            start_time = datetime.now()
            resp, start_time, end_time = _utils.action(self.__session, method.lower(), url, **req_args)
            if check_status_:
                if 200 > resp.status_code or resp.status_code >= 300:
                    _LOGGER.log(level=40, msg=f"check http status code is not success: {resp.status_code}",
                                stacklevel=4)
                    raise HttpException(f"http status code is not success: {resp.status_code}")

            rest_resp = RestResponse(resp)

        except BaseException as e:
            _LOGGER.log(level=40, msg=f"An exception occurred when a request was sent without a response:\n"
                                      f"{traceback.format_exc()}", stacklevel=4)
            raise RestInternalException(f"An exception occurred during the http request process: "
                                        f"url is {url}: {e}")
        finally:
            if end_time is None:
                end_time = datetime.now()
            _url = url if not resp else resp.url
            arguments_list = []
            for k, v in req_args.items():
                if not v:
                    continue
                if k in ['json', 'headers', 'data', 'params']:
                    # noinspection PyBroadException
                    try:
                        arguments_list.append(f'\t{k.ljust(20, " ")} => {complexjson.dumps(v or "")}')
                    except BaseException:
                        arguments_list.append(f'\t{k.ljust(20, " ")} => {v or ""}')
                else:
                    arguments_list.append(f'\t{k.ljust(20, " ")} => {v or ""}')
            arguments = '\n'.join(arguments_list)
            try:
                content = rest_resp.content.decode(_encoding)
            except BaseException as e:
                _LOGGER.log(level=LogLevel.WARNING.value, msg=f"RestResponse content decode error: {str(e)}",
                            stacklevel=2)
                content = rest_resp.text
            if 0 < _show_len < len(content):
                content = f"{content[:_show_len]}..."
            _utils.build_log_message(log_builder,
                                     _HTTP_INFO_TEMPLATE.format(
                                         self.description,
                                         description,
                                         'url'.ljust(20, ' '), _url,
                                         'method'.ljust(20, ' '), method.upper(),
                                         arguments,
                                         'http status'.ljust(20, " "), rest_resp.code,
                                         _show_len,
                                         'resp body'.ljust(20, ' '), content.strip(),
                                         'headers'.ljust(20, ' '), rest_resp.headers,
                                         'start time'.ljust(20, ' '), start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                         'end time'.ljust(20, ' '), end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                         'use time'.ljust(20, ' '), TimeUnit.format(
                                             TimeUnit.MICRO_SECOND.of((end_time - start_time).microseconds), 3)
                                     ))
            _utils.build_log_message(log_builder, f" [{func_name}Request End] ".center(83, '*'))
            _LOGGER.log(level=RestConfig.http_log_level.value, msg=log_builder, stacklevel=stacklevel)
            rest_resp = _utils.run_after_hooks(self.__hooks, hooks or Hooks(),
                                               optional_args.get("hooks") or Hooks(), rest_resp)
            if self.__stats is True and stats is True:
                self.__api_stats_done.add((_url, method))
            return rest_resp

    @staticmethod
    def bulk(content: str) -> dict:
        return _utils.bulk_header(content)
