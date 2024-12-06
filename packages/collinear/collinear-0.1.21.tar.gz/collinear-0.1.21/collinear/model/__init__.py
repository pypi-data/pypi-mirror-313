import uuid
from collinear.BaseService import BaseService
from collinear.model.types import ModelDTO


class Model(BaseService):
    def __init__(self, access_token: str,space_id:str) -> None:
        super().__init__(access_token,space_id)

    async def get_model_by_id(self,
                              model_id: uuid.UUID,
                              ) -> ModelDTO:
        output = await self.send_request(f'/api/v1/model/{model_id}', "GET")
        return ModelDTO(id=output['id'],
                        name=output['name'],
                        space_id=output['space_id'],
                        nickname=output['nickname'],
                        base_url=output['base_url'],
                        api_key=output['api_key'],
                        type=output['model_type'])
