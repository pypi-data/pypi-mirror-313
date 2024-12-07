#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum

from ._handler._converter_handler._calculator import _Converter, _NumericType
from .enums import EnhanceEnum
from .number import Integer


class _UnitEnum(EnhanceEnum):
    """
    unit tools base class
    """
    def of(self, num: int or float) -> '_Converter':
        """
        Convert the input num to the selected enumeration
        """
        return _Converter(num, self.value)

    def to(self, unit: Enum) -> _NumericType:
        """
        equal call _UnitEnum.of(1).to(unit)
        """
        return self.of(1).to(unit)

    @staticmethod
    def format(value: [float, int, '_UnitEnum', '_Converter'], precision: int) -> str:
        """
        Formatted in a human-readable format
        :param value: The value that needs to be converted
        :param precision: The precision prec controls the number of digits (excluding the exponent)
        :return:
        """
        raise RuntimeError("Concrete implementations need to be provided")


class StorageUnit(_UnitEnum):
    """
    Storage unit conversion tool
    """
    BIT = Integer(1)
    BYTE = Integer(1 << 3)
    KB = Integer(1 << 13)
    MB = Integer(1 << 23)
    GB = Integer(1 << 33)
    TB = Integer(1 << 43)
    PB = Integer(1 << 53)
    EB = Integer(1 << 63)
    ZB = Integer(1 << 73)
    YB = Integer(1 << 83)
    BB = Integer(1 << 93)
    NB = Integer(1 << 103)
    DB = Integer(1 << 113)

    @staticmethod
    def format(value: [float, int, '_UnitEnum', '_Converter'], precision: int = 2) -> str:
        """
        Format the value into the specified storage unit.
        float, int it will be handled in Bytes.
        ex:
            StorageUnit.format(StorageUnit.MB, 2)           >> 1.0M  # Special form, the unit base is 1 case
            StorageUnit.format(StorageUnit.MB.of(2), 2)     >> 2.0M
            StorageUnit.format(StorageUnit.MB.of(10000), 2) >> 9.77GB
            StorageUnit.format(2097152, 2)                  >> 2.0M
        """
        if isinstance(value, _UnitEnum):
            _value = value.value
        elif isinstance(value, _Converter):
            _value = value.to(StorageUnit.BIT)
        else:
            _value = StorageUnit.BYTE.of(value).to(StorageUnit.BIT)
        if _value >= StorageUnit.DB.value:
            return f"{round(_value / StorageUnit.DB.value, precision)}DB"
        elif _value >= StorageUnit.NB.value:
            return f"{round(_value / StorageUnit.NB.value, precision)}NB"
        elif _value >= StorageUnit.BB.value:
            return f"{round(_value / StorageUnit.BB.value, precision)}BB"
        elif _value >= StorageUnit.YB.value:
            return f"{round(_value / StorageUnit.YB.value, precision)}YB"
        elif _value >= StorageUnit.ZB.value:
            return f"{round(_value / StorageUnit.ZB.value, precision)}ZB"
        elif _value >= StorageUnit.EB.value:
            return f"{round(_value / StorageUnit.EB.value, precision)}EB"
        elif _value >= StorageUnit.PB.value:
            return f"{round(_value / StorageUnit.PB.value, precision)}PB"
        elif _value >= StorageUnit.TB.value:
            return f"{round(_value / StorageUnit.TB.value, precision)}TB"
        elif _value >= StorageUnit.GB.value:
            return f"{round(_value / StorageUnit.GB.value, precision)}GB"
        elif _value >= StorageUnit.MB.value:
            return f"{round(_value / StorageUnit.MB.value, precision)}MB"
        elif _value >= StorageUnit.KB.value:
            return f"{round(_value / StorageUnit.KB.value, precision)}KB"
        elif _value >= StorageUnit.BYTE.value:
            return f"{round(_value / StorageUnit.BYTE.value, precision)}B"
        else:
            return f"{round(_value, precision)}bit"


class TimeUnit(_UnitEnum):
    """
    Time unit conversion tool
    """
    NANO_SECOND = Integer(1)
    MICRO_SECOND = Integer(1 * 1000)
    MILLI_SECOND = Integer(1 * 1000 * 1000)
    SECOND = Integer(1 * 1000 * 1000 * 1000)
    MINUTE = Integer(1 * 1000 * 1000 * 1000 * 60)
    HOUR = Integer(1 * 1000 * 1000 * 1000 * 60 * 60)
    DAY = Integer(1 * 1000 * 1000 * 1000 * 60 * 60 * 24)

    @staticmethod
    def format(value: [float, int, '_UnitEnum', '_Converter'], precision: int = 2) -> str:
        """
        Format the value to the specified unit of time.
        float, int it will be handled in millisecond.
        ex:
            TimeUnit.format(TimeUnit.HOUR, 2)           >> 1.0Hour(s)
            TimeUnit.format(TimeUnit.HOUR.of(2), 2)     >> 2.0Hour(s)
            TimeUnit.format(TimeUnit.HOUR.of(333), 2)   >> 13.88Day(s)
            TimeUnit.format(1699800, 2)                 >> 28.33Min(s)
        """
        if isinstance(value, _UnitEnum):
            _value = value.value
        elif isinstance(value, _Converter):
            _value = value.to(TimeUnit.NANO_SECOND)
        else:
            _value = TimeUnit.MILLI_SECOND.of(value).to(TimeUnit.NANO_SECOND)
        if _value >= TimeUnit.DAY.value:
            return f"{round(_value / TimeUnit.DAY.value, precision)} d"
        elif _value >= TimeUnit.HOUR.value:
            return f"{round(_value / TimeUnit.HOUR.value, precision)} h"
        elif _value >= TimeUnit.MINUTE.value:
            return f"{round(_value / TimeUnit.MINUTE.value, precision)} min"
        elif _value >= TimeUnit.SECOND.value:
            return f"{round(_value / TimeUnit.SECOND.value, precision)} s"
        elif _value >= TimeUnit.MILLI_SECOND.value:
            return f"{round(_value / TimeUnit.MILLI_SECOND.value, precision)} ms"
        elif _value >= TimeUnit.MICRO_SECOND.value:
            return f"{round(_value / TimeUnit.MICRO_SECOND.value, precision)} μs"
        else:
            return f"{round(_value, precision)} ns"
