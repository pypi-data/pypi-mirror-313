"""Harp device types"""

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class _HarpDeviceTypeModel(BaseModel):
    """Base model for platform"""

    model_config = ConfigDict(frozen=True)
    whoami: int = Field(..., title="Harp whoami value")
    name: str = Field(..., title="Harp device type name")


class _Behavior(_HarpDeviceTypeModel):
    """Model Behavior"""

    name: Literal["Behavior"] = "Behavior"
    whoami: Literal[1216] = 1216


class _Camera_Controller(_HarpDeviceTypeModel):
    """Model Camera Controller"""

    name: Literal["Camera Controller"] = "Camera Controller"
    whoami: Literal[1168] = 1168


class _Clock_Synchronizer(_HarpDeviceTypeModel):
    """Model Clock Synchronizer"""

    name: Literal["Clock Synchronizer"] = "Clock Synchronizer"
    whoami: Literal[1152] = 1152


class _Cuttlefish(_HarpDeviceTypeModel):
    """Model Cuttlefish"""

    name: Literal["Cuttlefish"] = "Cuttlefish"
    whoami: Literal[1403] = 1403


class _Generic_Harp_Device(_HarpDeviceTypeModel):
    """Model Generic Harp Device"""

    name: Literal["Generic Harp Device"] = "Generic Harp Device"
    whoami: Literal[0] = 0


class _Input_Expander(_HarpDeviceTypeModel):
    """Model Input Expander"""

    name: Literal["Input Expander"] = "Input Expander"
    whoami: Literal[1106] = 1106


class _Lickety_Split(_HarpDeviceTypeModel):
    """Model Lickety Split"""

    name: Literal["Lickety Split"] = "Lickety Split"
    whoami: Literal[1400] = 1400


class _Load_Cells(_HarpDeviceTypeModel):
    """Model Load Cells"""

    name: Literal["Load Cells"] = "Load Cells"
    whoami: Literal[1232] = 1232


class _Olfactometer(_HarpDeviceTypeModel):
    """Model Olfactometer"""

    name: Literal["Olfactometer"] = "Olfactometer"
    whoami: Literal[1140] = 1140


class _Sniff_Detector(_HarpDeviceTypeModel):
    """Model Sniff Detector"""

    name: Literal["Sniff Detector"] = "Sniff Detector"
    whoami: Literal[1401] = 1401


class _Sound_Card(_HarpDeviceTypeModel):
    """Model Sound Card"""

    name: Literal["Sound Card"] = "Sound Card"
    whoami: Literal[1280] = 1280


class _Stepper_Driver(_HarpDeviceTypeModel):
    """Model Stepper Driver"""

    name: Literal["Stepper Driver"] = "Stepper Driver"
    whoami: Literal[1130] = 1130


class _Synchronizer(_HarpDeviceTypeModel):
    """Model Synchronizer"""

    name: Literal["Synchronizer"] = "Synchronizer"
    whoami: Literal[1104] = 1104


class _Timestamp_Generator_Gen_1(_HarpDeviceTypeModel):
    """Model Timestamp Generator Gen 1"""

    name: Literal["Timestamp Generator Gen 1"] = "Timestamp Generator Gen 1"
    whoami: Literal[1154] = 1154


class _Timestamp_Generator_Gen_3(_HarpDeviceTypeModel):
    """Model Timestamp Generator Gen 3"""

    name: Literal["Timestamp Generator Gen 3"] = "Timestamp Generator Gen 3"
    whoami: Literal[1158] = 1158


class _Treadmill(_HarpDeviceTypeModel):
    """Model Treadmill"""

    name: Literal["Treadmill"] = "Treadmill"
    whoami: Literal[1402] = 1402


class HarpDeviceType:
    """Harp device types"""

    BEHAVIOR = _Behavior()
    CAMERA_CONTROLLER = _Camera_Controller()
    CLOCK_SYNCHRONIZER = _Clock_Synchronizer()
    CUTTLEFISH = _Cuttlefish()
    GENERIC_HARP_DEVICE = _Generic_Harp_Device()
    INPUT_EXPANDER = _Input_Expander()
    LICKETY_SPLIT = _Lickety_Split()
    LOAD_CELLS = _Load_Cells()
    OLFACTOMETER = _Olfactometer()
    SNIFF_DETECTOR = _Sniff_Detector()
    SOUND_CARD = _Sound_Card()
    STEPPER_DRIVER = _Stepper_Driver()
    SYNCHRONIZER = _Synchronizer()
    TIMESTAMP_GENERATOR_GEN_1 = _Timestamp_Generator_Gen_1()
    TIMESTAMP_GENERATOR_GEN_3 = _Timestamp_Generator_Gen_3()
    TREADMILL = _Treadmill()

    ALL = tuple(_HarpDeviceTypeModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(_HarpDeviceTypeModel.__subclasses__())], Field(discriminator="name")]
