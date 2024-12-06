import uuid
from typing import List, Optional, Literal, Any, Dict

from collinear.BaseService import BaseService
from collinear.exceptions.ValidationError import ValidationError
from collinear.judge.types import QAFewShotExample, \
    NLIFewShotExample, ConversationFewShotExample, ConversationCGFewShotExample
from collinear.judge.utils import validate_qa_few_shot, validate_nli_few_shot, validate_conv_few_shot, \
    validate_conv_cg_few_shot


class Create(BaseService):
    def __init__(self, access_token: str) -> None:
        super().__init__(access_token)

    async def veritas(self, judge_name: str,
                      model_name: Literal['veritas', 'veritas_nano'],
                      space_id: uuid.UUID,
                      qa_few_shot: Optional[List[QAFewShotExample]] = None,
                      nli_few_shot: Optional[List[NLIFewShotExample]] = None,
                      conv_few_shot: Optional[List[ConversationFewShotExample]] = None,
                      rag_api_key: Optional[str] = None,
                      rag_index: Optional[str] = None,
                      rag_namespace: Optional[str] = None,
                      rag_top_k: Optional[int] = None,
                      rag_host: Optional[str] = None) -> dict:
        """
    Creates a new Veritas judge in the specified space.

    The Veritas judge is an entity configured with few-shot examples and optional
    RAG (Retrieval-Augmented Generation) parameters for enhanced question-answering,
    natural language inference, and conversation tasks.

    Args:
        model_name(str): The name of the model to use for the judge. Allowed values are 'veritas' and 'veritas_nano'.
        judge_name (str): The name assigned to the judge being created.
        space_id (uuid.UUID): The unique identifier for the space where the judge will be created.
        qa_few_shot (Any): Few-shot examples to guide the QA (Question-Answering) model.
        nli_few_shot (Any): Few-shot examples to assist the NLI (Natural Language Inference) model.
        conv_few_shot (Any): Few-shot examples tailored for the conversation model.
        rag_api_key (Optional[str], optional): API key for the RAG service, if required. Defaults to None.
        rag_index (Optional[str], optional): Index identifier for RAG. Specifies which document index to use. Defaults to None.
        rag_namespace (Optional[str], optional): Namespace for organizing RAG data. Useful for multi-tenant setups. Defaults to None.
        rag_top_k (Optional[int], optional): Number of top results to return from RAG. Controls retrieval result granularity. Defaults to None.
        rag_host (Optional[str], optional): Host URL for the RAG service. Required if using an external RAG service. Defaults to None.

    Returns:
        dict: A dictionary containing the response data, including status and metadata about the created judge.

    Raises:
        Exception: If the request fails or the server returns an error response.

    Example:
        response = await self.veritas(
            judge_name="ExampleJudge",
            space_id=UUID("12345678-1234-5678-1234-567812345678"),
            qa_few_shot=qa_examples,
            nli_few_shot=nli_examples,
            conv_few_shot=conv_examples,
            rag_api_key="your_rag_api_key",
            rag_index="default_index",
            rag_namespace="your_namespace",
            rag_top_k=5,
            rag_host="https://rag-service-host.com"
        )

    This method initiates the creation of a judge configured with specific few-shot learning
    examples and optional RAG settings
    """

        if qa_few_shot:
            validate_qa_few_shot(qa_few_shot)
        if nli_few_shot:
            validate_nli_few_shot(nli_few_shot)
        if conv_few_shot:
            validate_conv_few_shot(conv_few_shot)
        response = await self.send_request('/api/v1/judge/create/sdk', "POST", {
            'model_name': model_name,
            'space_id': space_id,
            'judge_name': judge_name,
            'qa_few_shot': qa_few_shot,
            'nli_few_shot': nli_few_shot,
            'conv_few_shot': conv_few_shot,
            'rag_api_key': rag_api_key,
            'rag_index': rag_index,
            'rag_namespace': rag_namespace,
            'rag_top_k': rag_top_k,
            'rag_host': rag_host
        })
        return response

    async def collinear_guard(self, judge_name: str,
                              model_name: Literal['collinear_guard_nano', 'collinear_guard'],
                              space_id: uuid.UUID,
                              nano_model_type: Optional[
                                  Literal['prompt_evaluation', 'response_evaluation', 'refusal_evaluation']] = None,
                              conv_few_shot: Optional[List[ConversationCGFewShotExample]] = None) -> dict:

        if model_name == 'collinear_guard':
            if nano_model_type:
                raise ValidationError("nano_model_type is not required for collinear_guard model")

        if conv_few_shot:
            validate_conv_cg_few_shot(conv_few_shot)
        response = await self.send_request('/api/v1/judge/create/sdk', "POST", {
            'model_name': model_name,
            'space_id': space_id,
            'judge_name': judge_name,
            'conv_few_shot': conv_few_shot,
            'nano_model_type': nano_model_type
        })
        return response
