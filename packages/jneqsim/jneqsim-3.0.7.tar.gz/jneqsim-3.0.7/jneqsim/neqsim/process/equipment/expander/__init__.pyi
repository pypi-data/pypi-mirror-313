
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import java.util
import jneqsim.neqsim.process.equipment
import jneqsim.neqsim.process.equipment.compressor
import jneqsim.neqsim.process.equipment.stream
import typing



class ExpanderInterface(jneqsim.neqsim.process.equipment.ProcessEquipmentInterface, jneqsim.neqsim.process.equipment.TwoPortInterface):
    def equals(self, object: typing.Any) -> bool: ...
    def getEnergy(self) -> float: ...
    def hashCode(self) -> int: ...

class Expander(jneqsim.neqsim.process.equipment.compressor.Compressor, ExpanderInterface):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], streamInterface: jneqsim.neqsim.process.equipment.stream.StreamInterface): ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...

class ExpanderOld(jneqsim.neqsim.process.equipment.TwoPortEquipment, ExpanderInterface):
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], streamInterface: jneqsim.neqsim.process.equipment.stream.StreamInterface): ...
    def displayResult(self) -> None: ...
    def getEnergy(self) -> float: ...
    @typing.overload
    def run(self) -> None: ...
    @typing.overload
    def run(self, uUID: java.util.UUID) -> None: ...
    def setInletStream(self, streamInterface: jneqsim.neqsim.process.equipment.stream.StreamInterface) -> None: ...
    def setOutletPressure(self, double: float) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.process.equipment.expander")``.

    Expander: typing.Type[Expander]
    ExpanderInterface: typing.Type[ExpanderInterface]
    ExpanderOld: typing.Type[ExpanderOld]
