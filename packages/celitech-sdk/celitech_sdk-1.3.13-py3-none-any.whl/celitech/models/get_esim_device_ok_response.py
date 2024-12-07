from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({"hardware_name": "hardwareName", "hardware_model": "hardwareModel"})
class Device(BaseModel):
    """Device

    :param oem: Name of the OEM, defaults to None
    :type oem: str, optional
    :param hardware_name: Name of the Device, defaults to None
    :type hardware_name: str, optional
    :param hardware_model: Model of the Device, defaults to None
    :type hardware_model: str, optional
    :param eid: Serial Number of the eSIM, defaults to None
    :type eid: str, optional
    """

    def __init__(
        self,
        oem: str = None,
        hardware_name: str = None,
        hardware_model: str = None,
        eid: str = None,
    ):
        """Device

        :param oem: Name of the OEM, defaults to None
        :type oem: str, optional
        :param hardware_name: Name of the Device, defaults to None
        :type hardware_name: str, optional
        :param hardware_model: Model of the Device, defaults to None
        :type hardware_model: str, optional
        :param eid: Serial Number of the eSIM, defaults to None
        :type eid: str, optional
        """
        self.oem = self._define_str("oem", oem, nullable=True)
        self.hardware_name = self._define_str(
            "hardware_name", hardware_name, nullable=True
        )
        self.hardware_model = self._define_str(
            "hardware_model", hardware_model, nullable=True
        )
        self.eid = self._define_str("eid", eid, nullable=True)


@JsonMap({})
class GetEsimDeviceOkResponse(BaseModel):
    """GetEsimDeviceOkResponse

    :param device: device, defaults to None
    :type device: Device, optional
    """

    def __init__(self, device: Device = None):
        """GetEsimDeviceOkResponse

        :param device: device, defaults to None
        :type device: Device, optional
        """
        self.device = self._define_object(device, Device)
