from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class GetAccessTokenOkResponse(BaseModel):
    """GetAccessTokenOkResponse

    :param access_token: access_token, defaults to None
    :type access_token: str, optional
    :param token_type: token_type, defaults to None
    :type token_type: str, optional
    :param expires_in: expires_in, defaults to None
    :type expires_in: int, optional
    """

    def __init__(
        self, access_token: str = None, token_type: str = None, expires_in: int = None
    ):
        """GetAccessTokenOkResponse

        :param access_token: access_token, defaults to None
        :type access_token: str, optional
        :param token_type: token_type, defaults to None
        :type token_type: str, optional
        :param expires_in: expires_in, defaults to None
        :type expires_in: int, optional
        """
        self.access_token = self._define_str(
            "access_token", access_token, nullable=True
        )
        self.token_type = self._define_str("token_type", token_type, nullable=True)
        self.expires_in = self._define_number("expires_in", expires_in, nullable=True)
