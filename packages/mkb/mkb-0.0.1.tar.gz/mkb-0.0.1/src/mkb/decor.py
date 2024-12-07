from typing import Union, Callable, Optional, List

from .core import FunctionInput, FunctionOutput, Example
from .impl.openai import OpenAILLMFunction, GptApiOptions


class LMFunctionBuilder:
    name: str

    instruction: str
    examples: list[Example]

    required_args: Optional[List[str]] = None
    strict_no_args: bool = False
    default_args: Optional[FunctionInput] = None

    def __init__(self, name):
        self.name = name
        self.instruction = None
        self.examples = []

    @staticmethod
    def from_function(func: Union['LMFunctionBuilder', Callable]) -> 'LMFunctionBuilder':
        if not isinstance(func, LMFunctionBuilder):
            return LMFunctionBuilder(name=func.__name__)
        else:
            return func

    def build_openai(
            self,
            openai_client=None,
            gpt_opts: Optional[GptApiOptions] = None,
    ):
        return OpenAILLMFunction.create(
            name=self.name,
            instruction=self.instruction,
            examples=self.examples,
            openai_client=openai_client,
            gpt_opts=gpt_opts,
            default_args=self.default_args,
            required_args=self.required_args,
            strict_no_args=self.strict_no_args,
        )


class DefineLLMFunction:

    @staticmethod
    def openai(
            name=None,
            client=None,
            opts: Optional[GptApiOptions] = None
    ):
        def decorator(func):
            func_name = name
            builder = LMFunctionBuilder.from_function(func)
            if func_name is None:
                func_name = builder.name
            builder.name = func_name
            return builder.build_openai(
                openai_client=client,
                gpt_opts=opts,
            )

        return decorator

    @staticmethod
    def with_instruction(instruction: str):
        def decorator(func):
            builder = LMFunctionBuilder.from_function(func)
            builder.instruction = instruction
            return builder

        return decorator

    @staticmethod
    def with_example(
            input: Optional[FunctionInput] = None,
            output: Optional[FunctionOutput] = None
    ):
        def decorator(func):
            builder = LMFunctionBuilder.from_function(func)
            builder.examples.append(Example(input=input, output=output))
            return builder

        return decorator

    @staticmethod
    def require_args(
            *args: List[str]
    ):
        def decorator(func):
            builder = LMFunctionBuilder.from_function(func)
            builder.required_args = args
            return builder

        return decorator

    @staticmethod
    def strict_no_args(value=True):
        def decorator(func):
            builder = LMFunctionBuilder.from_function(func)
            builder.strict_no_args = value
            return builder

        return decorator

    @staticmethod
    def with_default_args(value: FunctionInput):
        def decorator(func):
            builder = LMFunctionBuilder.from_function(func)
            builder.default_args = value
            return builder

        return decorator


def_fn = DefineLLMFunction()
