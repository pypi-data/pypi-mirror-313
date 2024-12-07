from typing import Literal, List, Optional

from pydantic import BaseModel


class ConversationMessage(BaseModel):
    """
       Represents a single message in a conversation.

       Attributes:
           content (str): The text content of the message.
           role (Literal["user", "assistant", "system"]): The role of the entity sending the message.
               Must be one of "user", "assistant", or "system".

       Example:
           >>> message = ConversationMessage(content="Hello, how can I help?", role="assistant")
       """
    content: str
    role: Literal["user", "assistant", "system"]


class ConversationInput(BaseModel):
    context: str
    conversation: List[ConversationMessage]
    response: ConversationMessage

    class Config:
        populate_by_name = True

class VeritasOutput(BaseModel):
    """
       Represents the output from the Veritas Judge.

       Attributes:
           judgement (int): The numerical judgement. 1 means the input is factual, 0 means it is hallucinated.
           rationale (Optional[str]): The rationale for the judgement.
           score(Optional[float]): A float value representing confidence.

       Example:
           >>> output = VeritasOutput(judgement=1, score=0.9)
       """
    judgement: int
    rationale: Optional[str] = None
    score:Optional[float] = None


class CollinearGuardNanoOutput(BaseModel):
    """
    Represents the output from the Collinear Guard Nano system.

    Attributes:
        judgement (int): The numerical judgement. 1 means the input is safe, 0 means it is unsafe.

    Example:
        >>> output = CollinearGuardNanoOutput(judgement=1)
    """
    judgement: int


class ScoringCriteria(BaseModel):
    """
    Represents the scoring criteria for the Collinear Guard.

    Attributes:
        score (float): The score to assign to a scoring criteria
        description (str): Description you want to give to the scoring criteria

    Example:
        >>> criteria = ScoringCriteria(score=1, description="Score is Assigned")
    """
    score: int
    description: str


class CollinearGuardPointwiseOutput(BaseModel):
    """
    Represents the output from the Collinear Guard model.

    Attributes:
        judgement (int): The numerical judgement. It can range based on scoring criteria.
        rationale (str): The rationale for the judgement.
    Examples:
          >>> output = CollinearGuardPointwiseOutput(judgement=5, rationale="The response is safe.")

    """
    judgement: int
    rationale: str


class ClassificationInput(BaseModel):
    conversation: List[ConversationMessage]
    response: ConversationMessage
    judge_id:str


class PointwiseInput(BaseModel):
    conversation: List[ConversationMessage]
    response: ConversationMessage
    judge_id:str


class QAFewShotExample(BaseModel):
    """
       Represents a question-answering (QA) few-shot example that provides context to help guide the QA model.

       Attributes:
           document (str): The context document where the QA interaction is based.
           question (str): The question posed within the context of the document.
           answer (str): The expected answer to the question based on the document content.
           output (int): A numerical representation of the answer's accuracy or other metrics.
           rationale (str): An explanation or justification for why the given answer is correct or relevant.
       """
    document: str
    question: str
    answer: str
    output: int
    rationale: str


class NLIFewShotExample(BaseModel):
    """
       Represents a natural language inference (NLI) few-shot example to help prime the NLI model.

       Attributes:
           document (str): The reference document or premise where the inference is drawn.
           claim (str): A statement or claim made that needs to be evaluated against the document.
           output (int): Numeric output typically representing a validity measure of the claim (e.g., true, false, uncertain).
           rationale (str): An explanation that supports the determination or conclusion regarding the claim.
    """
    document: str
    claim: str
    output: int
    rationale: str


class ConversationFewShotExample(BaseModel):
    """
       Provides a structured example for conversation models that includes a snapshot of an
       interaction and its related context.

       Attributes:
           conversation (List[ConversationMessage]): A list of conversation messages encapsulating
                                                     a dialogue exchange, where each message has a role and content.
           document (str): An associated document providing context or content relevant to the conversation.
           output (int): A numerical output often used for training or evaluation, indicating some assessment of the conversation.
           rationale (str): Rationale providing reasoning or explanation for the conversation's evaluation.
           response (ConversationMessage): An expected response or closing remark in the conversation, also structured
                                          as a role-content message.
       """
    conversation: List[ConversationMessage]
    document: str
    output: int
    rationale: str
    response: ConversationMessage


class ConversationCGFewShotExample(BaseModel):
    """
       Provides a structured example for conversation models that includes a snapshot of an
       interaction and its related context.

       Attributes:
           conversation (List[ConversationMessage]): A list of conversation messages encapsulating
                                                     a dialogue exchange, where each message has a role and content.
           output (int): A numerical output often used for training or evaluation, indicating some assessment of the conversation.
           rationale (str): Rationale providing reasoning or explanation for the conversation's evaluation.
           response (ConversationMessage): An expected response or closing remark in the conversation, also structured
                                          as a role-content message.
       """
    conversation: List[ConversationMessage]
    output: int
    rationale: str
    response: ConversationMessage