from typing import Dict, List

from pydantic import BaseModel


class DiffusionInstructions(BaseModel):
    prompt: str
    image_identifier: str
    negative_prompt: str | None = None
    num_inference_steps: int | None = None
    guidance_scale: float | None = None
    width: int | None = None
    height: int | None = None


class ImageToImageInstructions(DiffusionInstructions):
    image_to_image: bool = True
    base_image_identifier: str
    strength: float | None = None


class TextToImageInstructions(DiffusionInstructions):
    text_to_image: bool = True


class ChatInstructions(BaseModel):
    chat: bool = True
    prompt: str
    max_new_tokens: int | None = None
    temperature: float | None = None
    repetition_penalty: float | None = None


class DiscoveryInstructions(BaseModel):
    message: str


class PromptTemplateInstructions(BaseModel):
    prompt_name: str
    input_variables: Dict[str, str] | None = None


class Errand(BaseModel):
    instructions: (TextToImageInstructions
                   | ImageToImageInstructions
                   | ChatInstructions
                   | PromptTemplateInstructions
                   | DiscoveryInstructions)
    origin: str
    destination: str
    errand_identifier: str
    timestamp: float


class DiffusionReply(BaseModel):
    image_identifier: str


class ChatReply(BaseModel):
    message: str

class DiscoveryReply(BaseModel):
    discovery_result: List[str]


class Echo(BaseModel):
    errand: Errand
    reply: DiffusionReply | ChatReply
