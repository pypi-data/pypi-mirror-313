from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models import (
    GetEsimDeviceOkResponse,
    GetEsimHistoryOkResponse,
    GetEsimMacOkResponse,
    GetEsimOkResponse,
)


class ESimService(BaseService):

    @cast_models
    def get_esim(self, iccid: str) -> GetEsimOkResponse:
        """Get eSIM Status

        :param iccid: ID of the eSIM
        :type iccid: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: GetEsimOkResponse
        """

        Validator(str).min_length(18).max_length(22).validate(iccid)

        serialized_request = (
            Serializer(f"{self.base_url}/esim", self.get_default_headers())
            .add_query("iccid", iccid)
            .serialize()
            .set_method("GET")
            .set_scopes({})
        )

        response = self.send_request(serialized_request)
        return GetEsimOkResponse._unmap(response)

    @cast_models
    def get_esim_device(self, iccid: str) -> GetEsimDeviceOkResponse:
        """Get eSIM Device

        :param iccid: ID of the eSIM
        :type iccid: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: GetEsimDeviceOkResponse
        """

        Validator(str).min_length(18).max_length(22).validate(iccid)

        serialized_request = (
            Serializer(
                f"{self.base_url}/esim/{{iccid}}/device", self.get_default_headers()
            )
            .add_path("iccid", iccid)
            .serialize()
            .set_method("GET")
            .set_scopes({})
        )

        response = self.send_request(serialized_request)
        return GetEsimDeviceOkResponse._unmap(response)

    @cast_models
    def get_esim_history(self, iccid: str) -> GetEsimHistoryOkResponse:
        """Get eSIM History

        :param iccid: ID of the eSIM
        :type iccid: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: GetEsimHistoryOkResponse
        """

        Validator(str).min_length(18).max_length(22).validate(iccid)

        serialized_request = (
            Serializer(
                f"{self.base_url}/esim/{{iccid}}/history", self.get_default_headers()
            )
            .add_path("iccid", iccid)
            .serialize()
            .set_method("GET")
            .set_scopes({})
        )

        response = self.send_request(serialized_request)
        return GetEsimHistoryOkResponse._unmap(response)

    @cast_models
    def get_esim_mac(self, iccid: str) -> GetEsimMacOkResponse:
        """Get eSIM MAC

        :param iccid: ID of the eSIM
        :type iccid: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: GetEsimMacOkResponse
        """

        Validator(str).min_length(18).max_length(22).validate(iccid)

        serialized_request = (
            Serializer(
                f"{self.base_url}/esim/{{iccid}}/mac", self.get_default_headers()
            )
            .add_path("iccid", iccid)
            .serialize()
            .set_method("GET")
            .set_scopes({})
        )

        response = self.send_request(serialized_request)
        return GetEsimMacOkResponse._unmap(response)
