
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import jpype
import jneqsim.neqsim.process.equipment
import jneqsim.neqsim.process.mechanicaldesign
import typing



class PipelineMechanicalDesign(jneqsim.neqsim.process.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.neqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    @staticmethod
    def main(stringArray: typing.Union[typing.List[java.lang.String], jpype.JArray]) -> None: ...
    def readDesignSpecifications(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.process.mechanicaldesign.pipeline")``.

    PipelineMechanicalDesign: typing.Type[PipelineMechanicalDesign]
