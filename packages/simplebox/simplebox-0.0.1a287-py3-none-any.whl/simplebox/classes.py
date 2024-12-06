#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
import typing
from types import GenericAlias
from typing import Optional

from .exceptions import raise_exception, InstanceException

_Final = getattr(typing, "_Final")

__all__ = ['ForceType', 'StaticClass', 'Final', 'End', 'ConstructorIntercept']


class ForceType(object):
    """
    Given a type as the type of variable, an exception is thrown if the assigned type is inconsistent with that type.

    Example:
        class Person:
            age = ForceType(int)
            name = ForceType(str)

            def __init__(self, age, name):
                self.age = age
                self.name = name

        tony = Person(15, 'Tony')
        tony.age = '15'  # raise exception
    """

    def __init__(self, *types: Optional[type]):
        self.__can_none = False
        self.__types: list[type] = []
        self.__types_append = self.__types.append
        self.__types_name = []
        self.__types_name_append = self.__types_name.append
        for t in types:
            if t is None:  # NoneType begin with Python version 3.10+
                self.__can_none = True
                self.__types_name_append("NoneType")
            elif issubclass(t_ := type(t), GenericAlias):
                t_g_alias = type(t())
                self.__types_append(t_g_alias)
                self.__types_name_append(t_g_alias.__name__)
            elif issubclass(t_, type):
                self.__types_append(t)
                self.__types_name_append(self.__get__name(t))
            elif issubclass(t_, _Final):
                self.__types_append(getattr(t, "__origin__"))
                self.__types_name_append(self.__get__name(t))
            else:
                raise TypeError(f"expected 'type' type class, but found '{t_.__name__}'")
        self.__types: type[type, ...] = tuple(self.__types)

    @staticmethod
    def __get__name(t: type) -> str:
        if issubclass(type(t), _Final):
            return getattr(t, "_name") or getattr(getattr(t, "__origin__"), "__name__")
        else:
            return t.__name__

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set_name__(self, cls, name):
        self.name = name

    def __set__(self, instance, value):
        value_type = type(value)
        if issubclass(value_type, self.__types) or (self.__can_none and value is None):
            instance.__dict__[self.name] = value
        else:
            raise TypeError(f"expected {self.__types_name}, got '{value_type.__name__}'")


class _StaticClass(type):
    def __call__(cls, *args, **kwargs):
        raise_exception(InstanceException(f"Class '{cls.__name__}' cannot be instantiated!!!"))


class StaticClass(metaclass=_StaticClass):
    """
    Create a class that cannot be instantiated
    Example:
        Class Foo(StaticClass):
            pass
        Foo() # raise exception
    """
    pass


class Final(type):
    """
    Classes that are prohibited from being inherited.
    The difference with 'End' is that 'Final' does not need to be instantiated to detect whether it inherits,
    but 'End' needs to be instantiated before it can be checked.
    usage:

        class Parent(metaclass=Final):
            pass


        class Child(Parent):
            pass

        compile and run python script  # raise exception: Class 'Parent' is a Final type, cannot be inherited
    """

    def __new__(mcs, name, bases, dict, *args, **kwargs):
        for base in bases:
            if isinstance(base, Final):
                raise TypeError("Class '{0}' is a Final type, cannot be inherited".format(base.__name__))
        return super().__new__(mcs, name, bases, dict, **kwargs)


class End:
    """
    Classes that are prohibited from being inherited.
    The difference with 'Final' is that 'Final' does not need to be instantiated to detect whether it inherits,
    but 'End' needs to be instantiated before it can be checked.

    Example:
        class Parent(End):
            pass


        class Child(Parent):
            pass

        Child()  # raise exception: Class 'Parent' is an End type, cannot be inherited
    """

    def __new__(cls, *args, **kwargs):
        cls.__handler(cls, 1)

    @classmethod
    def __handler(cls, base: type, dep):
        for clz in base.__bases__:
            if clz.__name__ == End.__name__ and dep > 1:
                raise TypeError("Class '{0}' is an End type, cannot be inherited".format(base.__name__))
            else:
                cls.__handler(clz, dep + 1)


class _ConstructorIntercept(type):
    def __call__(cls, *args, **kwargs):
        stack = inspect.stack()[1]
        if __file__ != stack.filename:
            raise RuntimeError(f"Initialization error. No instantiation functionality is provided externally")
        return type.__call__(cls, *args, **kwargs)


class ConstructorIntercept(metaclass=_ConstructorIntercept):
    """
        Some classes are not allowed to be accessed or instantiated externally,
        so use ConstructorIntercept to decorate classes that need to be restricted.
        For example, providing services externally through the wrapper function

        Subclasses will also be affected, i.e. subclasses also need to be instantiated together in the current file,
        otherwise an exception will be thrown
        usage:
            producer.py
                class People(ConstructorIntercept):
                    pass

                class Child(People):
                    pass

                # no exception
                def init_wrapper():
                    // Instantiate class People
                    // do something
                    // return

            consumer.py
                // Instantiate class People  #  raise exception


        """
    pass
