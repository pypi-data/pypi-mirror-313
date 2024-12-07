from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models import GetAccessTokenOkResponse, GetAccessTokenRequest


class OAuthService(BaseService):

    @cast_models
    def get_access_token(
        self, request_body: GetAccessTokenRequest
    ) -> GetAccessTokenOkResponse:
        """This endpoint was added by liblab

        :param request_body: The request body.
        :type request_body: GetAccessTokenRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: GetAccessTokenOkResponse
        """

        Validator(GetAccessTokenRequest).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/oauth2/token", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body, "application/x-www-form-urlencoded")
        )

        response = self.send_request(serialized_request)
        return GetAccessTokenOkResponse._unmap(response)
