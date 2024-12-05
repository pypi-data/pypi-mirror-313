#!/usr/bin/env python
# -*- coding:utf-8 -*

from abc import abstractmethod, ABCMeta, ABC
from collections.abc import Callable
from typing import Any

from . import HttpMethod, RestFul, Hooks, StatsUrl, RestOptions
from ..config.rest import RestConfig
from ..generic import T
from ..serialize import Serializable

__all__ = []


class __BaseRestAdvice(metaclass=ABCMeta):

    @property
    @abstractmethod
    def restful(self) -> RestFul:
        pass

    @restful.setter
    @abstractmethod
    def restful(self, restful: RestFul):
        pass

    @property
    @abstractmethod
    def check_status(self) -> bool:
        pass

    @check_status.setter
    @abstractmethod
    def check_status(self, value):
        pass

    @property
    @abstractmethod
    def encoding(self) -> str:
        pass

    @encoding.setter
    @abstractmethod
    def encoding(self, value):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def host(self) -> str:
        pass

    @host.setter
    @abstractmethod
    def host(self, value):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value):
        pass

    @property
    @abstractmethod
    def verify(self) -> str or bool:
        pass

    @verify.setter
    @abstractmethod
    def verify(self, verify: str or bool):
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        pass

    @headers.setter
    @abstractmethod
    def headers(self, headers: dict):
        pass

    @property
    @abstractmethod
    def cookies(self) -> dict:
        pass

    @cookies.setter
    @abstractmethod
    def cookies(self, cookies: dict):
        pass

    @property
    @abstractmethod
    def auth(self) -> tuple:
        pass

    @auth.setter
    @abstractmethod
    def auth(self, auth: tuple):
        pass

    @property
    @abstractmethod
    def hooks(self) -> Hooks:
        pass

    @hooks.setter
    @abstractmethod
    def hooks(self, hooks: Hooks):
        pass

    @property
    @abstractmethod
    def retry_times(self) -> int:
        pass

    @retry_times.setter
    @abstractmethod
    def retry_times(self, retry_time: int):
        pass

    @property
    @abstractmethod
    def retry_interval(self) -> int:
        pass

    @retry_interval.setter
    @abstractmethod
    def retry_interval(self, retry_interval: int):
        pass

    @property
    @abstractmethod
    def retry_exit_code_range(self) -> list:
        pass

    @retry_exit_code_range.setter
    @abstractmethod
    def retry_exit_code_range(self, retry_exit_code_range: list):
        pass

    @property
    @abstractmethod
    def retry_exception_retry(self) -> bool:
        pass

    @retry_exception_retry.setter
    @abstractmethod
    def retry_exception_retry(self, retry_exception_retry: bool):
        pass

    @property
    @abstractmethod
    def retry_check_handler(self) -> Callable[[Any], bool]:
        pass

    @retry_check_handler.setter
    @abstractmethod
    def retry_check_handler(self, retry_check_handler: Callable[[Any], bool]):
        pass

    @property
    @abstractmethod
    def proxies(self) -> dict:
        pass

    @proxies.setter
    @abstractmethod
    def proxies(self, proxies: dict):
        pass

    @property
    @abstractmethod
    def cert(self) -> str or tuple:
        pass

    @cert.setter
    @abstractmethod
    def cert(self, cert: str or tuple):
        pass

    @property
    @abstractmethod
    def stats(self) -> bool:
        pass

    @stats.setter
    @abstractmethod
    def stats(self, stats: bool):
        pass

    @property
    @abstractmethod
    def api_stats_done(self) -> 'StatsUrl':
        """
        The URL of the HTTP request that was made.
        :return:
        """
        pass

    @property
    @abstractmethod
    def show_len(self) -> int:
        pass

    @show_len.setter
    @abstractmethod
    def show_len(self, value: int):
        pass

    @abstractmethod
    def copy(self) -> '__BaseRestAdvice':
        """
        Copies the current object.
        !!!!!!WARNING!!!!!!
        Shallow Copy.
        !!!!!!WARNING!!!!!!
        """

    @abstractmethod
    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        """
        if http request fail or exception, will retry.
        :param check_handler: This parameter is a callback function, if function return value check fail,
                              the retry is also triggered.
        it will determine whether to continue (make) the retry by checking the key of the body
        :param times: Number of retries
        :param interval: Retry interval
        :param exit_code_range: The expected HTTP status,
        if the response status code of the HTTP request is within this range, will exit the retry. The range is closed.
        default value [200, 299].
        :param exception_retry: Whether to retry when an exception occurs. True will try again

        If all of the above parameters are provided, the default values are used.

        Example:
            class Api:
                rest = Rest("rest.json", host="http://localhost:8080", description="demo domain")

                @rest.retry(times=2)
                @rest.get(description="打印hello")
                def test_case2(self,  response) -> RestResponse:
                    return response
        """

    @abstractmethod
    def request(self, api: str, method: HttpMethod or str = None,
                allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True, hooks: Hooks = None,
                show_len: int = None, opts: RestOptions = None) -> T:
        """
        http  request, need to specify the request method.
        Configure the interface information
        Important: requests arguments must be keyword arguments
        :param hooks: send request before and after run.
                      Order of execution, opts.hooks > request.hooks > rest.hooks.
        :param description: api's description info
        :param encoding: parse response's text or content encode
        :param check_status: check http response status, default false
        :param api: service http interface, which takes precedence over this parameter when specified
        :param method: interface request method, which is used in preference after specified
        :param allow_redirection: Whether to automatically redirect, the default is
        :param headers: custom http request header, if allow_redirection parameter is included,
        the allow_redirection in the header takes precedence
        :param restful: if it is a restful-style URL, it is used to replace the keywords in the URL,
        and if the keyword is missing, KeyError will be thrown
        :param stats: Whether the API is counted
        :param show_len: When the response is large, the maximum number of characters that can be displayed.
        :param opts: http request params.

        The parameters of the func only need a 'response', others, such as params, data, etc.,
        can be specified directly in the argument as keyword arguments.
        Keyword parameter restrictions only support the following parameters,include "params", "data", "json",
        "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies", "verify", "stream", "cert",
        "stream", "hooks".
        if requests module have been added new parameters, Options object is recommended because it is not limited by
        the parameters above.
        usage:
            normal use:
                class User:
                    rest = Rest(host)

                    @rest.get(api="/get_user", method=Method.GET)
                    def get_info(self, response):
                        return response
                user = User()


            type_reference:
                @EntityType()
                class Data(Entity):
                    id: list[str]
                    OK: str


                class User:
                    rest = Rest(host)

                    @rest.get(api="/get_user", method=Method.GET, type_reference=Data)
                    def get_info(self, response):
                        return response
                user = User()
                print(user.get_info())  # Data(id=[1], OK='200')






            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def get(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        """
        http get request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.get(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def post(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
             restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
             opts: RestOptions = None) -> T:
        """
        http POST request method.
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.post(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def put(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        """
        http PUT request method.
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.put(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def delete(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        """
        http DELETE request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.delete(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def patch(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        """
        http PATCH request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.patch(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def head(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        """
        http HEAD request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.head(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def options(self, api: str, allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        """
        http OPTIONS request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.options(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @staticmethod
    @abstractmethod
    def bulk(content: str) -> dict:
        """
        Convert headers copied from the browser to dicts
        :param content: copied header from the browser
        :return: python dict object
        example:
            header = Rest.bulk(r'''
                :method:POST
                :scheme:https
                Accept:*/*
                Accept-Encoding:gzip, deflate, br
                Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
                Content-Encoding:gzip
                Content-Length:367
                Content-Type:application/x-protobuf
                Origin:https://zhuanlan.zhihu.com
                Sec-Ch-Ua:"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"
                Sec-Ch-Ua-Mobile:?0
                Sec-Ch-Ua-Platform:"Windows"
                Sec-Fetch-Dest:empty
                Sec-Fetch-Mode:cors
                Sec-Fetch-Site:same-site
                User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
                X-Za-Batch-Size:1
                X-Za-Log-Version:3.3.74
                X-Za-Platform:DesktopWeb
                X-Za-Product:Zhihu
                    ''')
            print(header)  =>  {':method': 'POST', ':scheme': 'https', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Content-Encoding': 'gzip', 'Content-Length': '367', 'Content-Type': 'application/x-protobuf', 'Origin': 'https://zhuanlan.zhihu.com', 'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0', 'X-Za-Batch-Size': '1', 'X-Za-Log-Version': '3.3.74', 'X-Za-Platform': 'DesktopWeb', 'X-Za-Product': 'Zhihu'}

        """


class BaseRestWrapper(__BaseRestAdvice, ABC):
    """
    BaseRest wrapper object, used to decorate, the http request method interface is consistent with BaseRest.
    """

    @property
    @abstractmethod
    def tag(self) -> str:
        pass

    @property
    @abstractmethod
    def wrapper_tag(self) -> str:
        pass
    @property
    def restful(self) -> RestFul:
        raise NotImplementedError(f"not support restful method.")

    @property
    def check_status(self) -> bool:
        raise NotImplementedError(f"not support check_status method.")

    @property
    def encoding(self) -> str:
        raise NotImplementedError(f"not support encoding method.")

    @property
    def name(self) -> str:
        raise NotImplementedError(f"not support name method.")

    @property
    def host(self) -> str:
        raise NotImplementedError(f"not support host method.")

    @property
    def description(self) -> str:
        raise NotImplementedError(f"not support description method.")

    @property
    def verify(self) -> str or bool:
        raise NotImplementedError(f"not support verify method.")

    @property
    def headers(self) -> dict:
        raise NotImplementedError(f"not support headers method.")

    @property
    def cookies(self) -> dict:
        raise NotImplementedError(f"not support cookies method.")

    @property
    def auth(self) -> tuple:
        raise NotImplementedError(f"not support auth method.")

    @property
    def hooks(self) -> Hooks:
        raise NotImplementedError(f"not support hooks method.")

    @property
    def retry_times(self) -> int:
        raise NotImplementedError(f"not support retry_times method.")

    @property
    def retry_interval(self) -> int:
        raise NotImplementedError(f"not support retry_interval method.")

    @property
    def retry_exit_code_range(self) -> list:
        raise NotImplementedError(f"not support retry_exit_code_range method.")

    @property
    def retry_exception_retry(self) -> bool:
        raise NotImplementedError(f"not support retry_exception_retry method.")

    @property
    def retry_check_handler(self) -> Callable[[Any], bool]:
        raise NotImplementedError(f"not support retry_check_handler method.")

    @property
    def proxies(self) -> dict:
        raise NotImplementedError(f"not support proxies method.")

    @property
    def cert(self) -> str or tuple:
        raise NotImplementedError(f"not support cert method.")

    @property
    def stats(self) -> bool:
        raise NotImplementedError(f"not support stats method.")

    @property
    def show_len(self) -> int:
        raise NotImplementedError(f"not support show_len method.")

    @property
    @abstractmethod
    def api_stats_done(self) -> 'StatsUrl':
        pass

    @property
    @abstractmethod
    def api_stats_do(self) -> StatsUrl:
        """
        The statistics are for APIs that are assembled but do not initiate HTTP requests.
        :return:
        """
        pass

    @property
    @abstractmethod
    def rest(self) -> 'BaseRest':
        pass

    def copy(self) -> 'BaseRestWrapper':
        pass


class BaseRest(__BaseRestAdvice, ABC):
    """
    http request client.


    usage:
    class BizApi(ApiAware):
        rest = RestWrapper()
        def __init__(self, context, tag):
            self.__context = context
            self.__tag = tag

        @property
        def context(self):
            return self.__context

        @property
        def tag(self):
            return self.__tag

        @rest.post(api="/hello")
        def hello(self, response):
            # do something
            return response

    context = RestContext()
    rest = Rest(host="http://localhost:8080")
    context.put(biz=rest)

    biz = BizApi(context, 'biz')

    # This is just an example, and the parameters are actually passed according to their own business
    biz.hello(opts=RestOptions(params={}, data={}, json={}))
    """

    @abstractmethod
    def copy(self) -> 'BaseRest':
        pass


class BaseContextBean(metaclass=ABCMeta):
    """"""
    @property
    @abstractmethod
    def tag(self) -> str:
        """
        bean tag, same as rest tag.
        :return:
        """

    @property
    @abstractmethod
    def rest(self) -> BaseRest:
        """
        it is context bean
        :return:
        """

    @property
    @abstractmethod
    def wrappers(self) -> dict[str, BaseRestWrapper]:
        """
        it is a dict, key is wrapper tag
        :return:
        """

    @abstractmethod
    def has_wrapper(self, tag: str = None, wrapper: BaseRestWrapper = None) -> bool:
        """
        :param tag:
        :param wrapper:
        :return:
        """

    @abstractmethod
    def get(self, tag) -> BaseRestWrapper:
        """
        :param tag: wrapper tag
        :return:
        """

    @abstractmethod
    def set(self, tag, wrapper: BaseRestWrapper):
        """
        :param tag: wrapper tag
        :param wrapper:
        :return:
        """
    @abstractmethod
    def set_all(self, **kwargs: BaseRestWrapper):
        pass

    @abstractmethod
    def pop(self, tag) -> BaseRestWrapper:
        """
        :param tag: wrapper tag
        :return:
        """

    @abstractmethod
    def clean(self):
        """
        clean wrappers.
        :return:
        """


class BaseContextAware(metaclass=ABCMeta):
    """
    manage context of rest wrapper.
    usage see BaseRest document.
    """

    @property
    @abstractmethod
    def beans(self) -> dict[str, BaseContextBean]:
        pass

    @abstractmethod
    def add(self, tag, rest: BaseRest):
        """
        Add rest
        """
        pass

    @abstractmethod
    def put(self, **kwargs: BaseRest):
        """
        Add tags and REST objects in the form of keywords, key is tag, value is BaseRest
        """
        pass

    @abstractmethod
    def update(self, rests: dict[str, BaseRest]):
        """
        Add tags and REST objects in dictionary form.
        """
        pass

    @abstractmethod
    def get(self, tag, default: BaseRest = None) -> BaseRest:
        """
        Get the REST object by using the tag.
        When a REST object is obtained, default is returned and default is stored in the context.
        """
        pass

    @abstractmethod
    def get_bean(self, tag) -> BaseContextBean:
        """

        :param tag: rest tag
        :return:
        """
        pass

    @abstractmethod
    def pop(self, tag) -> BaseRest:
        """
        remove tag and return tag value
        :param tag:
        :return:
        """

    @abstractmethod
    def builder(self, tag, name: str = None, host: str = None, headers: dict or Serializable = None,
                cookies: dict or Serializable = None, auth: tuple or Serializable = None,
                hooks: Hooks = None, show_len: int = None, http2: bool = False, check_status: bool = False,
                encoding: str = "utf-8", description: str = None, restful: dict or Serializable = None,
                retry_times: int = 10, retry_interval: int = 5, retry_exit_code_range: list = None,
                retry_exception_retry: bool = True, retry_check_handler: Callable[[Any], bool] = None,
                verify: bool = None, proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                trust_env: bool = True, max_redirects: int = 30, stats: bool = False) -> 'BaseRest':
        """
        fast build a rest and add to context.
        """
        pass


class ApiAware(metaclass=ABCMeta):
    """
    use rest wrapper's object.
    Provide data penetration capabilities
    usage see BaseRest document
    """

    @property
    @abstractmethod
    def context(self) -> BaseContextAware:
        """
        BaseContext
        :return:
        """
        pass
