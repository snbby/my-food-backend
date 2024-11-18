from typing import Any, List

from django.conf import settings
import requests
from requests import Response
from pydantic import BaseModel, ValidationError


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ResponseMessage(BaseModel):
    role: str
    content: str | None = None
    function_call: FunctionCall | None = None


class Message(BaseModel):
    role: str
    content: str | None = None


# class FunctionParameters(BaseModel):
#     type: str
#     properties: dict
#
#
class Function(BaseModel):
    name: str
    parameters: dict


class Choice(BaseModel):
    index: int
    message: ResponseMessage
    logprobs: Any
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: str | None = None


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    response_format: dict
    functions: List[Function] | None = None
    max_tokens: int
    function_call: dict


class Error(BaseModel):
    message: str
    param: str | None
    type: str | None
    code: str | None


class ErrorResponse(BaseModel):
    error: Error


class BaseChatResponse(BaseModel):
    error: ErrorResponse | None = None
    ok: ChatResponse | None = None


class OpenAIClient:
    base_url = 'https://api.openai.com/v1'
    model = 'gpt-3.5-turbo'
    audio_models = [
        'tts-1-hd',  # 
        'tts-1'  # Faster, lower quality
    ]
    

    def __init__(self):
        api_key = settings.MYFOOD_OPEN_AI_API_KEY
        organization = settings.MYFOOD_OPEN_AI_ORGANIZATION
        self.session = requests.session()
        self.session.headers = {
            'Authorization': f'Bearer {api_key}',
            'Open-AI-Organization': organization
        }

    def get_media(self, url: str) -> Response:
        r = requests.get(url)
        r.raise_for_status()
        return r

    def image_generation(self, data: dict, use_dalle3: bool = False) -> Response:
        """
        Dalle not accepting images less than 1024x1024
        
        {
            "prompt": "A cute baby sea otter",
            "n": 2,
            "size": "1024x1024"
            "model": "dall-e-3"  # Optional
        }
        """
        url = self.base_url + '/images/generations'
        if use_dalle3 is True:
            data['size'] = '1024x1024'
            data['model'] = 'dall-e-3'
        response = self.session.post(url=url, json=data)
        response.raise_for_status()
        return response

    def get_models(self) -> dict:
        url = self.base_url + '/models'
        response = self.session.get(url)
        return response.json()

    def billing_usage(self) -> dict:
        url = self.base_url + '/dashboard/billing/usage'
        params = {
            'end_date': '2024-07-19',
            'start_date': '2024-06-01'
        }
        response = self.session.get(url=url, params=params)
        return response.json()

    def usage(self) -> dict:
        url = self.base_url + '/usage'
        import datetime
        date = datetime.date(2024, 7, 19)

        # Parameters for API request
        params = {'date': date.strftime('%Y-%m-%d')}
        response = self.session.get(url=url, params=params)
        return response.json()

    def create_audio(self, prompt: dict) -> dict:
        """
        Input up to 4096 symbols
        
        {
            "model": "tts-1-hd",
            "input": "OpenAI now also supports text to speech with two models: tts-1 and tts-1-hd. 
            For real-time applications, the standard tts-1 model provides the lowest latency but at a lower quality
            than the tts-1-hd model. Due to the way the audio is generated, tts-1 is likely to generate content that 
            has more static in certain situations than tts-1-hd. In some cases, the audio may not have noticeable 
            differences depending on your listening device and the individual person. The input to generate the audio 
            from can be up to 4096 characters. Supported voices are alloy, echo, fable, onyx, nova, and shimmer. 
            Supported response formats are mp3, opus, aac, and flac. It is also possible to control the speed, 
            select a value from 0.25 to 4.0. 1.0 is the default. There is no direct mechanism to control the emotional 
            output of the audio generated. Certain factors may influence the output audio like capitalization or grammar 
            but OpenAI's internal tests with these have yielded mixed results. Please note that OpenAI's Usage Policies 
            require you to provide a clear disclosure to end users that the TTS voice they are hearing is AI-generated 
            and not a human voice.",
            "voice": "alloy",
            "response_format": "mp3",
            "speed": "1.1"
        }
        
        Response: Audio file
        
        """
        url = self.base_url + '/audio/speech'
        voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        response_formats = ['mp3', 'opus', 'aac', 'flac']
        speed = ['1', '1.5']  # From 0.25 to 4.0

        data = {
            'model': self.audio_models[0],
            'input': prompt,
            'voice': voices[0],
            'response_format': response_formats[0],
            'speed': speed[0]
        }

        response = self.session.post(url=url, json=data)
        return response

    def chat(self, messages: list[Message]) -> BaseChatResponse:
        url = self.base_url + '/chat/completions'
        response_format = {'type': 'json_object'}
        # response_format = {'type': 'text'}
        data = ChatRequest(messages=messages, model=self.model, response_format=response_format,
                           max_tokens=500).model_dump(mode='json')
        response = self.session.post(url=url, json=data)
        response_obj = self.handle_response(response)
        return response_obj

    def create_spanish_verbs(self, messages: list[Message], functions: list[Function]) -> BaseChatResponse:
        url = self.base_url + '/chat/completions'
        response_format = {'type': 'text'}
        max_tokens = 500
        function_call = {'name': 'crearVerboObject'}
        data = ChatRequest(
            messages=messages,
            model=self.model,
            functions=functions,
            function_call=function_call,
            response_format=response_format,
            max_tokens=max_tokens
        ).model_dump(mode='json')
        response = self.session.post(url=url, json=data)
        response_obj = self.handle_response(response)
        return response_obj

    def handle_response(self, response: requests.models.Response) -> BaseChatResponse:
        error = None
        ok = None
        if response.status_code >= 400:
            try:
                error = ErrorResponse(**response.json())
            except Exception:
                print(response.json())
                raise
        # elif 400 > response.status_code >= 200:
        else:
            try:
                ok = ChatResponse(**response.json())
            except ValidationError:
                from pprint import pprint
                pprint(response.json())
                raise

        response = BaseChatResponse(error=error, ok=ok)

        return response


custom_open_ai_client = OpenAIClient()
