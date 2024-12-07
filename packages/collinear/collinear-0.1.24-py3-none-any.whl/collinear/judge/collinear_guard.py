import uuid
from typing import List, Union, Optional, Literal

from collinear.BaseService import BaseService
from collinear.judge.types import ConversationMessage, CollinearGuardNanoOutput, \
    ScoringCriteria, ClassificationInput, PointwiseInput, CollinearGuardPointwiseOutput


class CollinearGuard(BaseService):
    def __init__(self, access_token: str,space_id:str) -> None:
        super().__init__(access_token,space_id)

    async def classification(self, judge_id: str,
                             conv_prefix: List[Union[ConversationMessage, dict]],
                             response: Union[ConversationMessage, dict]) -> CollinearGuardNanoOutput:
        """
        Sends a classification request to the Collinear Guard Nano model.
        Args:
            judge_id (str): The judge id for collinear guard nano model
            response (Union[ConversationMessage, dict]): The response to be evaluated.
                Should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
                Example: {"role": "assistant", "content": "How can I help you today?"}
            conv_prefix (List[Union[ConversationMessage, dict]]): The conversation history.
                Each message should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
                Example: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]
        Raises:
            ValueError: If scoring criteria is not None and does not have 2 elements

        Returns:
            CollinearGuardNanoOutput: Contains judgement

        """
        input_data = ClassificationInput(
            conversation=conv_prefix,
            response=response,
            judge_id=judge_id
        )
        response = await self.send_request('/api/v1/judge/safety', "POST", {
            'model_name': 'collinear_guard_classifier',
            **input_data.dict()
        })
        return CollinearGuardNanoOutput(judgement=response['judgement'])

    async def pointwise(self,
                        judge_id: str,
                        conv_prefix: List[Union[ConversationMessage, dict]],
                        response: Union[ConversationMessage, dict],
                        ) -> CollinearGuardPointwiseOutput:
        """
        Sends a pointwise request to the Collinear Guard model.
        Args:
            response (Union[ConversationMessage, dict]): The response to be evaluated.
                Should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
                Example: {"role": "assistant", "content": "How can I help you today?"}
            conv_prefix (List[Union[ConversationMessage, dict]]): The conversation history.
                Each message should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
                Example: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]
            judge_id (str): The judge id for collinear guard model
        Raises:
            ValidationError: If any validation error occurs
        Returns:
            CollinearGuardPointwiseOutput: Contains judgement and rationale


        """
        input_data = PointwiseInput(
            conversation=conv_prefix,
            response=response,
            judge_id=judge_id
        )
        response = await self.send_request('/api/v1/judge/safety', "POST", {
            'model_name': 'collinear_guard',
            **input_data.dict()
        })

        return CollinearGuardPointwiseOutput(judgement=response['judgement'], rationale=response['extra']['rationale'])
