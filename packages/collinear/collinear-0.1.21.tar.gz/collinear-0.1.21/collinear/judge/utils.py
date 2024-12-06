from typing import List, Dict, Any

from collinear.exceptions.ValidationError import ValidationError

example_qa_few_shot = [
    {
        "document": "Hey, I am a document",
        "question": "Hey, I am a question",
        "answer": "Hey, I am an answer",
        "output": 1,
        "rationale": "Hey, I am a rationale"
    }
]


def validate_qa_few_shot(qa_few_shot: List[Dict[str, Any]]) -> None:
    required_keys = {
        "document": str,
        "question": str,
        "answer": str,
        "output": int,
        "rationale": str
    }

    if not isinstance(qa_few_shot, list):
        raise ValidationError(
            "Invalid format: `qa_few_shot` should be a list of dictionaries.",
            example=example_qa_few_shot
        )

    for index, item in enumerate(qa_few_shot):
        if not isinstance(item, dict):
            raise ValidationError(
                f"Invalid format at index {index}: Each item in `qa_few_shot` must be a dictionary.",
                example=example_qa_few_shot
            )

        for key, expected_type in required_keys.items():
            if key not in item:
                raise ValidationError(
                    f"Missing key '{key}' in `qa_few_shot` item at index {index}.",
                    example=example_qa_few_shot
                )
            if not isinstance(item[key], expected_type):
                raise ValidationError(
                    f"Incorrect type for key '{key}' in `qa_few_shot` item at index {index}. "
                    f"Expected {expected_type.__name__}, got {type(item[key]).__name__}.",
                    example=example_qa_few_shot
                )


example_nli_few_shot = [
    {
        "document": "Hey, I am a document",
        "claim": "Hey, I am an answer",
        "output": 1,
        "rationale": "Hey, I am a rationale"
    }
]


def validate_nli_few_shot(nli_few_shot: List[Dict[str, Any]]) -> None:
    required_keys = {
        "document": str,
        "claim": str,
        "output": int,
        "rationale": str
    }

    if not isinstance(nli_few_shot, list):
        raise ValidationError(
            "Invalid format: `nli_few_shot` should be a list of dictionaries.",
            example=example_nli_few_shot
        )

    for index, item in enumerate(nli_few_shot):
        if not isinstance(item, dict):
            raise ValidationError(
                f"Invalid format at index {index}: Each item in `nli_few_shot` must be a dictionary.",
                example=example_nli_few_shot
            )

        for key, expected_type in required_keys.items():
            if key not in item:
                raise ValidationError(
                    f"Missing key '{key}' in `nli_few_shot` item at index {index}.",
                    example=example_nli_few_shot
                )
            if not isinstance(item[key], expected_type):
                raise ValidationError(
                    f"Incorrect type for key '{key}' in `nli_few_shot` item at index {index}. "
                    f"Expected {expected_type.__name__}, got {type(item[key]).__name__}.",
                    example=example_nli_few_shot
                )


example_conv_few_shot = [
    {
        "conversation": [
            {"role": "user", "content": "Hey"},
            {"role": "assistant", "content": "Hello, how can I help you?"}
        ],
        "document": "Example document content",
        "output": 1,
        "rationale": "Example rationale",
        "response": {
            "role": "assistant",
            "content": "Example response content"
        }
    }
]


def validate_conv_few_shot(conv_few_shot: List[Dict[str, Any]]) -> None:
    required_keys = {
        "conversation": list,
        "document": str,
        "output": int,
        "rationale": str,
        "response": dict
    }
    conversation_example = {"role": "user", "content": "Hey"}
    response_example = {"role": "assistant", "content": "Hello!"}

    if not isinstance(conv_few_shot, list):
        raise ValidationError(
            "Invalid format: `conv_few_shot` should be a list of dictionaries.",
            example=example_conv_few_shot
        )

    for index, item in enumerate(conv_few_shot):
        if not isinstance(item, dict):
            raise ValidationError(
                f"Invalid format at index {index}: Each item in `conv_few_shot` must be a dictionary.",
                example=example_conv_few_shot
            )

        # Validate top-level keys and types
        for key, expected_type in required_keys.items():
            if key not in item:
                raise ValidationError(
                    f"Missing key '{key}' in `conv_few_shot` item at index {index}.",
                    example=example_conv_few_shot
                )
            if not isinstance(item[key], expected_type):
                raise ValidationError(
                    f"Incorrect type for key '{key}' in `conv_few_shot` item at index {index}. "
                    f"Expected {expected_type.__name__}, got {type(item[key]).__name__}.",
                    example=example_conv_few_shot
                )

        # Validate `conversation` structure
        for msg_index, msg in enumerate(item["conversation"]):
            if not isinstance(msg, dict):
                raise ValidationError(
                    f"Invalid format in `conversation` at index {index}, message {msg_index}. "
                    "Each message should be a dictionary.",
                    example=conversation_example
                )
            if "role" not in msg or "content" not in msg:
                raise ValidationError(
                    f"Each message in `conversation` at index {index}, message {msg_index} "
                    "must contain 'role' and 'content' keys.",
                    example=conversation_example
                )
            if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
                raise ValidationError(
                    f"Invalid types in `conversation` at index {index}, message {msg_index}. "
                    "'role' and 'content' should be strings.",
                    example=conversation_example
                )

        # Validate `response` structure
        response = item["response"]
        if "role" not in response or "content" not in response:
            raise ValidationError(
                f"Missing keys in `response` for `conv_few_shot` item at index {index}. "
                "'response' must contain 'role' and 'content'.",
                example=response_example
            )
        if not isinstance(response["role"], str) or not isinstance(response["content"], str):
            raise ValidationError(
                f"Invalid types in `response` for `conv_few_shot` item at index {index}. "
                "'role' and 'content' should be strings.",
                example=response_example
            )


def validate_conv_cg_few_shot(conv_few_shot: List[Dict[str, Any]]) -> None:
    required_keys = {
        "conversation": list,
        "output": int,
        "rationale": str,
        "response": dict
    }
    conversation_example = {"role": "user", "content": "Hey"}
    response_example = {"role": "assistant", "content": "Hello!"}

    if not isinstance(conv_few_shot, list):
        raise ValidationError(
            "Invalid format: `conv_few_shot` should be a list of dictionaries.",
            example=example_conv_few_shot
        )

    for index, item in enumerate(conv_few_shot):
        if not isinstance(item, dict):
            raise ValidationError(
                f"Invalid format at index {index}: Each item in `conv_few_shot` must be a dictionary.",
                example=example_conv_few_shot
            )

        # Validate top-level keys and types
        for key, expected_type in required_keys.items():
            if key not in item:
                raise ValidationError(
                    f"Missing key '{key}' in `conv_few_shot` item at index {index}.",
                    example=example_conv_few_shot
                )
            if not isinstance(item[key], expected_type):
                raise ValidationError(
                    f"Incorrect type for key '{key}' in `conv_few_shot` item at index {index}. "
                    f"Expected {expected_type.__name__}, got {type(item[key]).__name__}.",
                    example=example_conv_few_shot
                )

        # Validate `conversation` structure
        for msg_index, msg in enumerate(item["conversation"]):
            if not isinstance(msg, dict):
                raise ValidationError(
                    f"Invalid format in `conversation` at index {index}, message {msg_index}. "
                    "Each message should be a dictionary.",
                    example=conversation_example
                )
            if "role" not in msg or "content" not in msg:
                raise ValidationError(
                    f"Each message in `conversation` at index {index}, message {msg_index} "
                    "must contain 'role' and 'content' keys.",
                    example=conversation_example
                )
            if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
                raise ValidationError(
                    f"Invalid types in `conversation` at index {index}, message {msg_index}. "
                    "'role' and 'content' should be strings.",
                    example=conversation_example
                )

        # Validate `response` structure
        response = item["response"]
        if "role" not in response or "content" not in response:
            raise ValidationError(
                f"Missing keys in `response` for `conv_few_shot` item at index {index}. "
                "'response' must contain 'role' and 'content'.",
                example=response_example
            )
        if not isinstance(response["role"], str) or not isinstance(response["content"], str):
            raise ValidationError(
                f"Invalid types in `response` for `conv_few_shot` item at index {index}. "
                "'role' and 'content' should be strings.",
                example=response_example
            )
