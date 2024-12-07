from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models import ListDestinationsOkResponse


class DestinationsService(BaseService):

    @cast_models
    def list_destinations(self) -> ListDestinationsOkResponse:
        """List Destinations

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Successful Response
        :rtype: ListDestinationsOkResponse
        """

        serialized_request = (
            Serializer(f"{self.base_url}/destinations", self.get_default_headers())
            .serialize()
            .set_method("GET")
            .set_scopes({})
        )

        response = self.send_request(serialized_request)
        return ListDestinationsOkResponse._unmap(response)
