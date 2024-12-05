from ploomber_cloud import api_key


class PloomberBaseClient:
    """A base client to call Ploomber APIs"""

    def __init__(self) -> None:
        self.api_key = api_key.get()

    def _get_headers(self):
        """Return headers to use in requests"""
        return {
            "accept": "application/json",
            "api_key": self.api_key,
        }
