from typing import List, Union

from collinear.BaseService import BaseService
from collinear.judge.types import ConversationMessage, ConversationInput, VeritasOutput


class Veritas(BaseService):
    def __init__(self, access_token: str, space_id: str) -> None:
        super().__init__(access_token, space_id)

    async def question_answer(self, judge_id: str, context: str, question: str,
                              answer: str) -> VeritasOutput:
        """
       Sends a question-answer request to the veritas judge.

       Args:
        context (str): The context of the question.
        question (str): The question to answer.
        answer (str): The answer provided.
        judge_id (str): The model id to use for a fine-tuned model. Default is None

       Returns:
           VeritasOutput: Contains judgement and score.

       """
        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'judge_id': judge_id,
            'type': 'qa',
            "context": context,
            "question": question,
            "answer": answer
        })
        return VeritasOutput(judgement=response['judgement'],
                             rationale=response['extra']['rationale'] if 'rationale' in response['extra'] else None,
                             score=response['extra']['score'] if 'score' in response['extra'] else None)

    async def natural_language_inference(self, judge_id: str, context: str, claim: str,
                                         ) -> VeritasOutput:
        """
        Sends a natural language inference request to the veritas judge.

        Args:
            context (str): The context of the claim.
            claim (str): The claim to check.
            judge_id (str): The model id to use for a fine-tuned model. Default is None


        Returns:
            VeritasOutput: Contains judgement and score.

        """
        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'judge_id': judge_id,
            'type': 'nli',
            "context": context,
            "claim": claim
        })
        return VeritasOutput(judgement=response['judgement'],
                             rationale=response['extra']['rationale'] if 'rationale' in response['extra'] else None,
                             score=response['extra']['score'] if 'score' in response['extra'] else None)

    async def conversation(self, judge_id: str, context: str, conv_prefix: List[Union[ConversationMessage, dict]],
                           response: Union[ConversationMessage, dict]) -> VeritasOutput:
        """
    Sends a conversation request to the Veritas judge.

    Args:
        context (str): The context of the conversation. Provide relevant background information.
        conv_prefix (List[Union[ConversationMessage, dict]]): The conversation history.
            Each message should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
            Example: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]
        response (Union[ConversationMessage, dict]): The response to be evaluated.
            Should be either a ConversationMessage object or a dict with 'role' and 'content' keys.
            Example: {"role": "assistant", "content": "How can I help you today?"}
        judge_id (str): The model id to use for a fine-tuned model. Default is None


    Returns:
        VeritasOutput: Contains the judgement and score from the Veritas judge.

    Raises:
        ValueError: If the input data is invalid or doesn't meet the required format.

    Example:
        output = await conversation(
            context="Customer service conversation",
            conv_prefix=[{"role": "user", "content": "I have a problem with my order"}],
            response={"role": "assistant", "content": "I'm sorry to hear that. Can you provide more details?"}
        )
    """
        # NOTE: Doing this to validate input data
        input_data = ConversationInput(
            context=context,
            conversation=conv_prefix,
            response=response
        )

        response = await self.send_request('/api/v1/judge/reliability', "POST", {
            'judge_id': judge_id,
            'type': 'conversation',
            "context": context,

            **input_data.dict()
        })

        return VeritasOutput(judgement=response['judgement'],
                             rationale=response['extra']['rationale'] if 'rationale' in response['extra'] else None,
                             score=response['extra']['score'] if 'score' in response['extra'] else None)
