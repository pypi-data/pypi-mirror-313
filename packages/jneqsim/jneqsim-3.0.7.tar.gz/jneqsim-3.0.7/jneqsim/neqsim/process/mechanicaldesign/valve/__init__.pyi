
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import jneqsim.neqsim.process.equipment
import jneqsim.neqsim.process.mechanicaldesign
import typing



class ValveMechanicalDesign(jneqsim.neqsim.process.mechanicaldesign.MechanicalDesign):
    def __init__(self, processEquipmentInterface: jneqsim.neqsim.process.equipment.ProcessEquipmentInterface): ...
    def calcDesign(self) -> None: ...
    def displayResults(self) -> None: ...
    def readDesignSpecifications(self) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("jneqsim.neqsim.process.mechanicaldesign.valve")``.

    ValveMechanicalDesign: typing.Type[ValveMechanicalDesign]
