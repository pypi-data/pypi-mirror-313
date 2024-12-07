import json
import os
import warnings
from dataclasses import dataclass, field

from openai import OpenAI

from mkb.fn import LLMFunction, LLMFunctionBatch, LLMFunctionOutput
from mkb.core import FunctionInputConfig, FunctionOutputConfig, Example, FunctionInput, FunctionOutput, \
    FunctionInputType, LmOutputCastingError, InputCounter, OutputCounter

from typing import Optional, Union, List, Dict, Literal, Tuple

from mkb.utils import try_parse_json, extract_required_keywords

default_openai_client = None


class Role:
    """
    Role for chat message.
    https://platform.openai.com/docs/api-reference/chat/create#chat/create-role
    """
    system: Literal['system'] = 'system'
    user: Literal['user'] = 'user'
    assistant: Literal['assistant'] = 'assistant'
    function: Literal['function'] = 'function'


@dataclass
class Message:
    """Chat Model Message.

    Args:
        role: (Role for chat message)[https://platform.openai.com/docs/api-reference/chat/create#chat/create-role]
        content: (The contents of the message)[https://platform.openai.com/docs/api-reference/chat/create#chat/create-content]
        name: (The name of the author of this message)[https://platform.openai.com/docs/api-reference/chat/create#chat/create-name]
    """
    role: Literal['system', 'user', 'assistant', 'function']
    content: str
    name: Optional[str] = None

    @staticmethod
    def user(content, name=None):
        return Message(role=Role.user, content=content, name=name)

    @staticmethod
    def assistant(content, name=None):
        return Message(role=Role.assistant, content=content, name=name)

    @staticmethod
    def system(content, name=None):
        return Message(role=Role.system, content=content, name=name)

    @staticmethod
    def example_user(content):
        return Message(role=Role.system, content=content, name='example_user')

    @staticmethod
    def example_assistant(content):
        return Message(role=Role.system, content=content, name='example_assistant')

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content,
            'name': self.name,
        }


@dataclass
class GptApiOptions:
    """
    GptApiOptions used in OpenAI's ChatCompletion API.
    See [OpenAI's API reference](https://platform.openai.com/docs/api-reference/chat/create).

    Args:
        model: which model to use, the model must be compatible with [OpenAI's chatCompletion API](https://platform.openai.com/docs/models/model-endpoint-compatibility)
        temperature: What sampling temperature to use, between 0 and 2. See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        n: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        top_p: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        stream: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        stop: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        max_tokens: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        presence_penalty: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        frequency_penalty: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        logit_bias: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
        user: See [OpenAI's API Reference](https://platform.openai.com/docs/api-reference/chat/create)
    """
    model: str = 'gpt-4o-mini'
    temperature: Optional[float] = None
    n: Optional[int] = None
    top_p: Optional[float] = None
    stream: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[int, int]] = None
    user: Optional[str] = None


@dataclass
class Definition:
    """

    Definition of a LmFunction, this should be created using LmFunction.create function.

    Args:
        instruction: what will this function do.
        examples: example input/output pairs.
        name: an optional name of this function.
        message_stack: created message stack to be sent to ChatCompletion API.
        input_config: this determines what input arguments are allowed
        output_config: this determines if the output of this function is a string or json object.
        default_args: If this value is not None, this function can be called with no arguments, and
                      the provided value will be used as default arguments instead.
        message_template: this message will be rendered with keyword arguments if kwargs are provided.
        required_args: list of required keyword args. If this value is missing and message_template is provided,
                       we will calculate required_args based on message_template.
        gpt_opts: inference parameters for ChatCompletion API.
    """
    instruction: str
    examples: List[Example]

    message_stack: List[Message]

    input_config: FunctionInputConfig
    output_config: FunctionOutputConfig

    default_args: Optional[FunctionInput] = None

    # For keyword functions
    message_template: Optional[str] = None
    required_args: Optional[List[str]] = None

    # OpenAI parameters
    gpt_opts: GptApiOptions = field(default_factory=GptApiOptions)

    name: Optional[str] = None

    @staticmethod
    def create_message_stack(
            instruction: str,
            examples: List[Example],
            input_config: FunctionInputConfig,
            output_config: FunctionOutputConfig,
            default_args: Optional[str],
            required_args: Optional[List[str]],
            message_template: Optional[str]
    ) -> List[Message]:
        message_stack = [
            Message.system(instruction)
        ]

        if examples is not None:
            for example in examples:
                assert isinstance(example, Example), "example must be an instance of Example"

                input_ = Definition.render_input(
                    input_config,
                    example.input,
                    default_args,
                    required_args,
                    message_template
                )
                output = Definition.render_output_example(
                    output_config,
                    example.output
                )

                message_stack.append(
                    Message.example_user(input_)
                )
                message_stack.append(
                    Message.example_assistant(output)
                )

        return message_stack

    @staticmethod
    def render_input(
            input_config: FunctionInputConfig,
            input_arg: Optional[FunctionInput],
            default_args: Optional[FunctionInput],
            required_args: Optional[List[str]],
            message_template: Optional[str]
    ):
        if input_config.input_type == FunctionInputType.KEYWORD:
            if input_arg is None or len(input_arg) == 0:
                if default_args is not None:
                    input_arg = default_args
                else:
                    raise ValueError("default_args is missing")

            if not isinstance(input_arg, dict):
                raise ValueError(f"function input must be a dict object for this function")

            if required_args is not None:
                for key in required_args:
                    if key not in input_arg:
                        raise ValueError(f'{key} is required but not provided')

            if message_template is not None:
                return message_template.format(**input_arg)
            else:
                return "\n".join([f"{k}: {v}" for k, v in input_arg.items()])
        elif input_config.input_type == FunctionInputType.UNARY:
            if input_arg is None:
                if default_args is not None:
                    input_arg = default_args
                else:
                    raise ValueError("default_args is missing")

            if isinstance(input_arg, str):
                return input_arg
            else:
                raise ValueError(f"function input must be a str for this function")

    @staticmethod
    def render_output_example(output_config: FunctionOutputConfig, example_output: FunctionOutput) -> str:
        if output_config.cast_to_json:
            if isinstance(example_output, list) or isinstance(example_output, dict):
                return json.dumps(example_output)
            else:
                raise ValueError("example output must be a dict or list, or set fn_output_type.cast_to_json to False")
        else:
            if isinstance(example_output, str):
                return example_output
            else:
                raise ValueError("example output must be string, or set fn_output_type.cast_to_json to True")

    @staticmethod
    def cast_lm_output(output_config: FunctionOutputConfig, llm_output: str) -> Union[List, Dict]:
        if output_config.cast_to_json:
            json_value, parsed = try_parse_json(llm_output)
            if parsed:
                return json_value
            else:
                raise LmOutputCastingError(llm_output=llm_output)
        else:
            return llm_output

    @staticmethod
    def detect_input_output_type(
            examples: List['Example'],
            default_args: Optional[FunctionInput] = None,
            strict_no_args: bool = False,
    ) -> Tuple[FunctionInputConfig, FunctionOutputConfig]:
        """

        :param examples:
        :param default_args: if default_args is provided and has no typing conflict, allow_none will be true
        :param strict_no_args:
        :return:
        """

        if len(examples) == 0:
            raise ValueError('No examples are provided.')

        observed_inputs = InputCounter()
        observed_outputs = OutputCounter()

        for example in examples:
            observed_inputs.count(example.input)
            observed_outputs.count(example.output)

        return (
            observed_inputs.to_config(default_args=default_args, strict_no_args=strict_no_args),
            observed_outputs.to_config()
        )


class OpenAILLMFunction(LLMFunction):
    """
    A text function that call be called, the preferred way to create such function is using one of
    `NullaryFunction`, `UnaryFunction`, `KeywordFunction`.
    """

    RESERVED_KEYWORDS = ['__extra_messages', '__override', '__return_resp_obj']
    """
    RESERVED_KEYWORDS: reserved keywords:
    __extra_messages: extra messages to be carried over, it will be appended after instruction and examples but 
                    before the final message
    __override: any parameters to be override, currently you can override the following:
                    * n
                    * top_p
                    * stream
                    * stop
                    * max_tokens
                    * presence_penalty
                    * frequency_penalty
                    * logit_bias
                    * user
                (see here for details)[https://platform.openai.com/docs/api-reference/chat/create]
    __return_resp_obj: if set to true, the response from ChatCompletion API will be returned directly                
    """

    definition: Definition

    def __init__(self, definition, openai_client):
        super().__init__(definition.name)
        self.definition = definition
        self.openai_client = openai_client
        if self.openai_client is None:
            self.openai_client = default_openai_client

        if self.openai_client is None:
            self.openai_client = OpenAI()

    @staticmethod
    def create(
            instruction: str,
            examples: List[Example],

            name: Optional[str] = None,
            strict_no_args: Optional[bool] = None,

            default_args: Optional[FunctionInput] = None,
            message_template: Optional[str] = None,
            required_args: Optional[List[str]] = None,
            gpt_opts: Optional[GptApiOptions] = None,
            openai_client=None
    ):
        """
        Create a LmFunction based on instruction and examples.

        :param instruction: what will this function do.
        :param examples: example input/output pairs.
        :param name: an optional name of this function.
        :param strict_no_args: if True, this function will be a nullary function, however, this value will be ignored
                               if examples contains non-None input.
        :param default_args: If this value is not None, this function can be called with no arguments, and
                             the provided value will be used as default arguments instead.
        :param message_template: this message will be rendered with keyword arguments if kwargs are provided.
        :param required_args: list of required keyword args. If this value is missing and message_template is provided,
                              we will calculate required_args based on message_template.
        :param gpt_opts: inference parameters for ChatCompletion API.
        :param openai_client: the openai client to use.

        :return: function created.
        """

        (fn_input_type, fn_output_type) = Definition.detect_input_output_type(
            examples,
            default_args=default_args,
            strict_no_args=strict_no_args
        )

        if not fn_input_type.strict_no_args and strict_no_args is True:
            warnings.warn("strict_no_args flag is ignored")

        if message_template is not None:
            if required_args is None:
                required_args = extract_required_keywords(message_template)

        if gpt_opts is None:
            gpt_opts = GptApiOptions()

        message_stack = Definition.create_message_stack(
            instruction=instruction,
            examples=examples,
            input_config=fn_input_type,
            output_config=fn_output_type,
            default_args=default_args,
            required_args=required_args,
            message_template=message_template,
        )

        t = Definition(
            name=name,
            instruction=instruction,
            examples=examples,
            message_stack=message_stack,

            input_config=fn_input_type,
            output_config=fn_output_type,

            default_args=default_args,

            message_template=message_template,
            required_args=required_args,

            gpt_opts=gpt_opts,
        )

        return OpenAILLMFunction(t, openai_client)

    def get_call_args(self, args, kwargs, ctrl_kws):
        extra_msgs = ctrl_kws.get('__extra_messages', [])

        fn_input_args = None
        if self.definition.input_config.input_type == FunctionInputType.KEYWORD:
            if self.definition.input_config.strict_no_args:
                if len(args) > 0:
                    raise ValueError('received positional arguments for nullary function.')
                if len(kwargs) > 0:
                    raise ValueError('received keyword arguments for nullary function.')
            else:
                if len(kwargs) > 0:
                    fn_input_args = kwargs
                else:
                    fn_input_args = None
        elif self.definition.input_config.input_type == FunctionInputType.UNARY:
            if self.definition.input_config.strict_no_args:
                if len(args) > 0:
                    raise ValueError('received positional arguments for nullary function.')
                if len(kwargs) > 0:
                    raise ValueError('received keyword arguments for nullary function.')
            else:
                if len(kwargs) > 0:
                    raise ValueError('received keyword arguments for unary function.')

                if len(args) == 0:
                    fn_input_args = None
                elif len(args) == 1:
                    fn_input_args = args[0]
                else:
                    raise ValueError('received more than 1 positional arguments.')

        messages = [m for m in self.definition.message_stack]

        if extra_msgs is not None:
            for m in extra_msgs:
                if not isinstance(m, Message):
                    raise ValueError('message in extra_messages must be an instance of slambda.Message')
                messages.append(m)

        messages.append(
            Message.user(Definition.render_input(
                self.definition.input_config,
                fn_input_args,
                self.definition.default_args,
                self.definition.required_args,
                self.definition.message_template
            ))
        )

        override_params = ctrl_kws.get('__override', {})

        model = override_params.get('model', self.definition.gpt_opts.model)
        n = override_params.get('n', self.definition.gpt_opts.n)
        temperature = override_params.get('temperature', self.definition.gpt_opts.temperature)
        top_p = override_params.get('top_p', self.definition.gpt_opts.top_p)
        stream = override_params.get('stream', self.definition.gpt_opts.stream)
        stop = override_params.get('stop', self.definition.gpt_opts.stop)
        max_tokens = override_params.get('max_tokens', self.definition.gpt_opts.max_tokens)
        presence_penalty = override_params.get('presence_penalty', self.definition.gpt_opts.presence_penalty)
        frequency_penalty = override_params.get('frequency_penalty', self.definition.gpt_opts.frequency_penalty)
        logit_bias = override_params.get('logit_bias', self.definition.gpt_opts.logit_bias)
        user = override_params.get('user', self.definition.gpt_opts.user)

        call_args_dict = dict(
            messages=[
                m.to_dict() for m in messages
            ],
            model=model,
            n=n,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            user=user
        )

        call_args_dict = {k: v for k, v in call_args_dict.items() if v is not None}
        return call_args_dict

    @staticmethod
    def split_args(args, kwargs):
        all_kwargs = kwargs
        kwargs = {}
        ctrl_kws = {}
        for k, v in all_kwargs.items():
            if k in OpenAILLMFunction.RESERVED_KEYWORDS:
                ctrl_kws[k] = v
            else:
                kwargs[k] = v
        return args, kwargs, ctrl_kws

    def handle_call(self, args, kwargs):
        """
        Execute the function call based on the provided template

        :param args:
        :param kwargs:
        :return:
        """
        args, kwargs, ctrl_kws = OpenAILLMFunction.split_args(args, kwargs)

        override_params = ctrl_kws.get('__override', {})

        call_args_dict = self.get_call_args(args, kwargs, ctrl_kws)
        resp = self.openai_client.chat.completions.create(**call_args_dict)
        return self.process_llm_output(resp.model_dump(mode='json'), ctrl_kws)

    def process_llm_output(self, resp, ctrl_kws):
        override_params = ctrl_kws.get('__override', {})
        stream = override_params.get('stream', self.definition.gpt_opts.stream)
        n = override_params.get('n', self.definition.gpt_opts.n)

        return_resp_obj = ctrl_kws.get('__return_resp_obj', False) or stream is True
        if return_resp_obj:
            return resp

        output_format = 'json' if self.definition.output_config.cast_to_json else 'text'

        if n is None or n == 1:
            ret = resp['choices'][0]['message']['content']
            return LLMFunctionOutput(ret, 1, output_format)
        else:
            outs = [c['message']['content'] for c in resp['choices']]
            return LLMFunctionOutput(
                outs,
                len(resp.choices),
                preferred_format=output_format
            )

    def _handle_get_batch(self, name, batch_folder, auto_start: bool = False):
        return OpenAILLMFunctionBatch(self, name, batch_folder, auto_start=auto_start)


class OpenAILLMFunctionBatch(LLMFunctionBatch):
    fn: OpenAILLMFunction

    def __init__(
            self,
            fn: OpenAILLMFunction,
            name: str,
            folder: str,
            auto_start: bool = False
    ):
        super().__init__(name, folder, auto_start)
        self.fn = fn

    @property
    def batch_file(self):
        return os.path.join(self.folder, '__batch__.jsonl')

    @property
    def result_file(self):
        return os.path.join(self.folder, '__result__.jsonl')

    def create_batch_file(self):
        with open(self.batch_file, 'w') as out:
            with open(self.input_file) as f:
                for idx, line in enumerate(f):
                    input_instance = json.loads(line)
                    args, kwargs, ctrl_kws = OpenAILLMFunction.split_args(
                        input_instance.get('args', []),
                        input_instance.get('kwargs', {})
                    )

                    body = self.fn.get_call_args(
                        args, kwargs, ctrl_kws
                    )
                    call_arg = {
                        "custom_id": f'{idx}',
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": body
                    }
                    out.write(json.dumps(call_arg) + '\n')

    def handle_start_batch(self):
        self.create_batch_file()
        local_batch_file = self.batch_file
        batch_file = self.get_openai_batch_file()
        if batch_file is None:
            batch_file = self.fn.openai_client.files.create(
                file=open(local_batch_file, "rb"),
                purpose="batch"
            )
            self.set_meta({
                'status': 'processing',
                'meta': {
                    'openai': {
                        'batch_file_id': batch_file.id
                    }
                }
            })

        batch_job = self.get_openai_batch_job()
        if batch_job is None:
            batch_job = self.fn.openai_client.batches.create(
                input_file_id=batch_file.id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )

            self.set_meta({
                'status': 'processing',
                'meta': {
                    'openai': {
                        'batch_job_id': batch_job.id,
                        'batch_file_id': batch_file.id
                    }
                }
            })
        return self.meta()

    def get_openai_batch_file(self):
        batch_meta = self.meta()
        if 'meta' in batch_meta:
            if 'openai' in batch_meta['meta']:
                if 'batch_file_id' in batch_meta['meta']['openai']:
                    return self.fn.openai_client.files.retrieve(batch_meta['meta']['openai']['batch_file_id'])

    def get_openai_batch_job(self):
        batch_meta = self.meta()
        if 'meta' in batch_meta:
            if 'openai' in batch_meta['meta']:
                if 'batch_job_id' in batch_meta['meta']['openai']:
                    return self.fn.openai_client.batches.retrieve(batch_meta['meta']['openai']['batch_job_id'])

    def fetch_output(self, output_file_id):
        result = self.fn.openai_client.files.content(output_file_id).content
        with open(self.result_file, 'wb') as file:
            file.write(result)

        self.process_output()

    def process_output(self):
        id_to_output = {}
        with open(self.result_file) as f:
            for idx, line in enumerate(f):
                result_instance = json.loads(line)
                cid = result_instance['custom_id']
                id_to_output[cid] = result_instance

        with open(self.output_file, 'w') as out:
            for idx, input_instance in enumerate(self.iter_inputs()):
                cid = f'{idx}'
                args, kwargs, ctrl_kws = OpenAILLMFunction.split_args(
                    input_instance.get('args', []),
                    input_instance.get('kwargs', {})
                )
                output = id_to_output[cid]
                resp = output['response']['body']

                output = self.fn.process_llm_output(resp, ctrl_kws)

                out.write(json.dumps(
                    {
                        'input': input_instance,
                        'output': output.serialize_to_dict(),
                    }
                ) + '\n')

    def sync_remote(self):
        batch_file = self.get_openai_batch_file()
        batch_job = self.get_openai_batch_job()

        if batch_job:
            if batch_job.status == 'completed':
                self.fetch_output(batch_job.output_file_id)
                return {
                    'status': 'finished',
                    'openai': {
                        'batch_job': batch_job
                    }
                }
            elif batch_job.status in [
                "validating", "in_progress", "finalizing",
            ]:
                return {
                    'status': 'processing',
                    'openai': {
                        'batch_job': batch_job
                    }
                }
            elif batch_job.status in [
                "failed", "expired", "cancelling", "cancelled"
            ]:
                return {
                    'status': 'error',
                    'openai': {
                        'batch_job': batch_job
                    }
                }

        return {
            'status': 'created',
        }
