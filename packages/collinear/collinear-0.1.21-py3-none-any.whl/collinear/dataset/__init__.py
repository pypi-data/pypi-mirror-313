import uuid

import pandas as pd

from collinear.BaseService import BaseService


class Dataset(BaseService):
    def __init__(self, access_token: str, space_id: str) -> None:
        super().__init__(access_token, space_id)

    async def upload_dataset(self, data: pd.DataFrame,
                             conv_prefix_column_name: str,
                             response_column_name: str,
                             judgement_column_name: str | None,
                             dataset_name: str,
                             space_id: uuid.UUID,
                             parent_dataset_id: uuid.UUID | None) -> uuid.UUID:
        """
        Uploads a dataset to the Collinear platform.
        Args:
            data: A pandas DataFrame containing the dataset.
            conv_prefix_column_name: Name of the column containing the conversation prefix.
            response_column_name: Name of the column containing the response.
            judgement_column_name: Name of the column containing the judgement. If not provided, the column will be ignored.
            dataset_name: Name of the dataset.
            space_id: ID of the space where the dataset will be uploaded.
            parent_dataset_id: ID of the parent dataset. If not provided, the dataset will be uploaded as a root dataset.

        Returns:
            dataset_id: ID of the uploaded dataset.
        """
        req_obj = {
            "name": dataset_name,
            "space_id": space_id,
        }
        if parent_dataset_id:
            req_obj['parent_dataset_id'] = parent_dataset_id
        conversations = []
        for index, row in data.iterrows():
            obj = {
                'conv_prefix': list(row[conv_prefix_column_name]),
                'response': row[response_column_name]['content'],
                'judgements': row[judgement_column_name] if judgement_column_name in row else {}
            }
            conversations.append(obj)
        req_obj['conversations'] = conversations
        output = await self.send_request('/api/v1/dataset', "POST", req_obj)
        return output['dataset_id']
