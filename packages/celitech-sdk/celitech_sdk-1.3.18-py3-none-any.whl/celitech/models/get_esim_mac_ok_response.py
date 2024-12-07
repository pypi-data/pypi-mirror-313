from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap(
    {"smdp_address": "smdpAddress", "manual_activation_code": "manualActivationCode"}
)
class GetEsimMacOkResponseEsim(BaseModel):
    """GetEsimMacOkResponseEsim

    :param iccid: ID of the eSIM, defaults to None
    :type iccid: str, optional
    :param smdp_address: SM-DP+ Address, defaults to None
    :type smdp_address: str, optional
    :param manual_activation_code: The manual activation code, defaults to None
    :type manual_activation_code: str, optional
    """

    def __init__(
        self,
        iccid: str = None,
        smdp_address: str = None,
        manual_activation_code: str = None,
    ):
        """GetEsimMacOkResponseEsim

        :param iccid: ID of the eSIM, defaults to None
        :type iccid: str, optional
        :param smdp_address: SM-DP+ Address, defaults to None
        :type smdp_address: str, optional
        :param manual_activation_code: The manual activation code, defaults to None
        :type manual_activation_code: str, optional
        """
        self.iccid = self._define_str(
            "iccid", iccid, nullable=True, min_length=18, max_length=22
        )
        self.smdp_address = self._define_str(
            "smdp_address", smdp_address, nullable=True
        )
        self.manual_activation_code = self._define_str(
            "manual_activation_code", manual_activation_code, nullable=True
        )


@JsonMap({})
class GetEsimMacOkResponse(BaseModel):
    """GetEsimMacOkResponse

    :param esim: esim, defaults to None
    :type esim: GetEsimMacOkResponseEsim, optional
    """

    def __init__(self, esim: GetEsimMacOkResponseEsim = None):
        """GetEsimMacOkResponse

        :param esim: esim, defaults to None
        :type esim: GetEsimMacOkResponseEsim, optional
        """
        self.esim = self._define_object(esim, GetEsimMacOkResponseEsim)
