import asyncio
import json
import logging
import uuid

import pandas as pd
from anthropic import AsyncAnthropic
from asynciolimiter import Limiter
from jinja2 import Template
from openai import AsyncOpenAI
from tqdm import tqdm

from collinear.BaseService import BaseService
from collinear.model import Model
from collinear.model.types import ModelTypeEnum, ModelDTO


class SyntheticData(BaseService):
    def __init__(self, access_token: str, space_id: str, model_service: Model) -> None:
        super().__init__(access_token, space_id)
        self.model = model_service

    async def generate(self, model_id: uuid.UUID,
                       prompt: str,
                       examples: list[dict],
                       multiplier: int) -> uuid.UUID:
        """
        Generated synthetic data with the help of a given model
        Args:
            model_id(str): The ID for model you wish to use
            prompt(str): Prompt for the generator Model
            examples(list[dict]): Name of the column containing the response.
            multiplier(int): The number of times you want to multiply your examples

        Returns:
            dataset_id: ID of the uploaded dataset.
        """
        req_obj = {
            "model_id": model_id,
            "prompt": prompt,
            "examples": examples,
            "multiplier": multiplier
        }
        output = await self.send_request('/api/v1/synth_data/generate', "POST", req_obj)
        return pd.DataFrame(output)

    async def curate(self, data: pd.DataFrame,
                     model_id: uuid.UUID,
                     calls_per_second=10,
                     max_concurrent_tasks=5):

        model = await self.model.get_model_by_id(model_id)
        # Initialize an async progress bar
        pbar = tqdm(total=len(data))

        # Rate limiter and task limiter (for concurrent tasks)
        rate_limiter = Limiter(calls_per_second)
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def generate(example):
            async with semaphore:  # Limit concurrent tasks
                await rate_limiter.wait()  # Respect the rate limit
                try:
                    json_obj = json.loads(example['generated'])
                    json_obj = json_obj['generated_data']
                    keys = json_obj.keys()
                    s_in = ""
                    for key in keys:
                        if key not in ['conversation', 'qa']:
                            s_in += f"{key}: {json_obj[key]}\n"
                    system_prompt = "You will be rating a single response as 0 or 1 based on how well it adheres to a given scoring criteria. Follow these steps:\n1. **Understand the Criteria:** Review the scoring criteria provided.\n2. **Evaluate the Response:** Analyze the response according to these criteria.\n3. **Assign a Rating:** Choose a score from 0 and 1 that best reflects the response's adherence to the criteria.\n4. **Provide Rationale:** Justify your rating with a concise explanation.\n\nThe output format should be as follows: \"(write a rationale for criteria) [RESULT] (0 or 1)"
                    user_prompt_coherence = """
                    Please review the scoring criteria:
                    <BEGIN SCORING CRITERIA>
                    Score 0: The conversation is off-topic, lacks logical flow, or includes inconsistencies. Turns may feel disjointed, unclear, or out of alignment with participant roles, disrupting the overall coherence of the dialogue.
                    Score 1: The conversation stays on-topic and flows naturally with a logical, turn-by-turn progression. Each exchange aligns with the roles of the participants, maintaining consistency and clarity throughout without introducing contradictions or confusion.
                    <END SCORING CRITERIA>
                    Here is the conversation context:
                    <BEGIN CONVERSATION PREFIX>
                    user: Give me a conversation between a Customer and Agent
                    <END CONVERSATION PREFIX>

                    Here is the response to evaluate:
                    <BEGIN RESPONSE>
                    assistant: {{response_in}}
                    <END RESPONSE>

                    Now, please output in the following format: \"(write a rationale for criteria) [RESULT] (0 or 1)
                    """
                    user_prompt_correctness = """
                    Please review the scoring criteria:
                    <BEGIN SCORING CRITERIA>
                    Score 0: The conversation is inconsistent with the meta-data if it introduces topics, entities, or contexts that contradict or are irrelevant to the meta-data, fails to maintain the tone or perspective implied by the meta-data, or overlooks essential elements specified in the meta-data. Additionally, logical inconsistencies, factual errors related to the meta-data, or significant omissions result in a score of 0.
                    Score 1: The conversation is consistent with the meta-data if it reflects the topics, entities, and context accurately, aligns with the tone and perspective suggested by the meta-data, and avoids introducing contradictions or unrelated elements. It must integrate all critical aspects of the meta-data cohesively and maintain logical coherence throughout.
                    <END SCORING CRITERIA>
                    Here is the conversation context:
                    <BEGIN CONVERSATION PREFIX>
                    user: Can you give me a conversation that revolves around the following meta-data:{{metadata_in}}
                    <END CONVERSATION PREFIX>

                    Here is the response to evaluate:
                    <BEGIN RESPONSE>
                    {{response_in}}
                    <END RESPONSE>

                    Now, please output in the following format: \"(write a rationale for criteria) [RESULT] (0 or 1)
                    """
                    user_prompt_naturalness = """
                    Please review the scoring criteria:
                    <BEGIN SCORING CRITERIA>
                    Score 0: The conversation includes improbable or impossible events, contradictions to known facts, or fantastical scenarios without basis in reality. Statements may be exaggerated, unverifiable, or absurd, deviating from logical consistency or real-world knowledge.
                    Score 1: The conversation is based on verifiable facts and plausible scenarios, following logical sequences. It aligns with established knowledge, remains consistent with the physical world, and avoids contradictions or unrealistic elements.
                    <END SCORING CRITERIA>
                    Here is the conversation context:
                    <BEGIN CONVERSATION PREFIX>
                    user: Give me a conversation between a Customer and Agent
                    <END CONVERSATION PREFIX>

                    Here is the response to evaluate:
                    <BEGIN RESPONSE>
                    assistant: {{response_in}}
                    <END RESPONSE>

                    Now, please output in the following format: \"(write a rationale for criteria) [RESULT] (0 or 1)
                    """

                    coherence_messages = [{"role": "system", "content": system_prompt}, {"role": "user",
                                                                                         "content": Template(
                                                                                             user_prompt_coherence).render(
                                                                                             response_in=json_obj[
                                                                                                 'conversation'])}]
                    naturalness_messages = [{"role": "system", "content": system_prompt}, {"role": "user",
                                                                                           "content": Template(
                                                                                               user_prompt_naturalness).render(
                                                                                               response_in=json_obj[
                                                                                                   'conversation'])}]
                    correctness_messages = [{"role": "system", "content": system_prompt}, {"role": "user",
                                                                                           "content": Template(
                                                                                               user_prompt_correctness).render(
                                                                                               response_in=json_obj[
                                                                                                   'conversation'],
                                                                                               metadata_in=s_in)}]
                    coherence = await self.get_chat_completion(model, coherence_messages)
                    naturalness = await self.get_chat_completion(model, naturalness_messages)
                    correctness = await self.get_chat_completion(model, correctness_messages)
                    result = example.copy()
                    result['score'] = self.extract_predictions(coherence) + self.extract_predictions(
                        naturalness) + self.extract_predictions(correctness)
                    result['extra'] = {
                        'coherence': self.extract_predictions(coherence),
                        'naturalness': self.extract_predictions(naturalness),
                        'correctness': self.extract_predictions(correctness)
                    }
                    return result
                except Exception as e:
                    return {"error": str(e)}
                finally:
                    pbar.update(1)

        tasks = [generate(row) for idx, row in data.iterrows()]
        results = await asyncio.gather(*tasks)
        entries = []
        for result in results:
            try:
                entries.append({
                    'original': result['original'],
                    'generated': result['generated'],
                    'score': result['score'],
                    'extra': result['extra']
                })
            except:
                pass
        return pd.DataFrame(entries)

    def extract_predictions(self, raw_text):
        post_text = raw_text.split("[RESULT]")[-1]
        if "1" in post_text:
            return 1
        elif "0" in post_text:
            return 0
        else:
            return -1

    async def get_chat_completion(self, model: ModelDTO, messages: list[dict], generation_kwargs={}) -> str:
        if model.type == ModelTypeEnum.openai:
            openai_client = AsyncOpenAI(base_url=model.base_url, api_key=model.api_key)
            completion = await openai_client.chat.completions.create(
                model=model.name,
                messages=messages,
                **generation_kwargs
            )
            return str(completion.choices.pop().message.content)
        elif model.type == ModelTypeEnum.anthropic:
            logging.debug("Using Anthropic client")
            anthropic_client = AsyncAnthropic(api_key=model.api_key, base_url=model.base_url)
            message = await anthropic_client.messages.create(
                messages=messages,
                model=model.name,
                **generation_kwargs
            )
            logging.debug(f"Anthropic completion result: {message}")
            return str(message.content)
        else:
            logging.error(f"Unknown model type: {model.type}")
            raise ValueError(f"Unsupported model type: {model.type}")
