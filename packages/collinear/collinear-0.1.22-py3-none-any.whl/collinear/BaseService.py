from typing import Literal

import aiohttp


class BaseService:
    def __init__(self, access_token: str,space_id:str) -> None:
        self.base_url = 'https://api.collinear.ai'
        self.space_id = space_id
        self.access_token = access_token

    def set_access_token(self, access_token: str):
        """
        Sets the access token for the entire SDK.
        """
        self.access_token = access_token
        return self

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    async def send_request(self, url: str, method: Literal["POST", "GET", "PUT", "DELETE", "PATCH"] = "GET",
                           data: dict = None) -> dict:
        full_url = f"{self.base_url}{url}"
        data = {
            "space_id": self.space_id,
            **data
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=method,
                    url=full_url,
                    headers=self.get_headers(),
                    json=data
            ) as response:
                try:
                    if response.status>=400:
                        error_text = await response.text()
                        raise Exception(error_text)
                    else:
                        response_data = await response.json()
                        return response_data
                except aiohttp.ContentTypeError:
                    error_text = await response.text()
                    raise Exception(f"Response is not JSON: {error_text}")
                except aiohttp.ClientResponseError as e:
                    error_text = await response.text()  # Capture the response content for debugging
                    raise Exception(f"HTTP error occurred: {e.status} - {error_text}")
                except Exception as e:
                    raise Exception(f"Unexpected error: {str(e)}")
