from dataclasses import dataclass

from typing import Optional, List, Union, Dict
from enum import Enum

FunctionInput = Union[str, Dict]
FunctionOutput = Union[str, List, Dict]


class LmOutputCastingError(Exception):
    """
    This exception will be thrown if LM output cannot be parsed using `json.loads` and cast_to_json is True.
    """

    def __init__(self, llm_output, message="cannot cast language model output"):
        """

        :param llm_output: Text output of language model
        :param message: error message
        """
        self.llm_output = llm_output
        self.message = message
        super().__init__(self.message)


class FunctionInputType(str, Enum):
    """
    TextFunctionMode control how a text function can be called.
    """
    KEYWORD = 'keyword'
    """
    KEYWORD allows calling with keyword arguments, e.g. f(a=10).
    """
    UNARY = 'unary'
    """
    UNARY allows calling with one positional argument1, e.g. f(10).
    """

    @staticmethod
    def of_value(input_args: Optional[FunctionInput], strict=True) -> Optional['FunctionInputType']:
        if isinstance(input_args, str):
            if strict and input_args == '':
                return None
            return FunctionInputType.UNARY
        elif isinstance(input_args, dict):
            if strict and input_args == {}:
                return None
            return FunctionInputType.KEYWORD
        elif input_args is None:
            return None
        else:
            raise ValueError('input vaule must be one of None, str, dict')


@dataclass
class FunctionInputConfig:
    """
    This class determine what kinds of input args is allowed for a function
    Args:
        input_type: Keyword or UNARY.
        allow_none: True if None input is allowed.
        strict_no_args: if True, the function will be a nullary function
    """
    input_type: FunctionInputType
    allow_none: bool = False
    strict_no_args: bool = False

    @staticmethod
    def unary(allow_none: bool):
        return FunctionInputConfig(
            input_type=FunctionInputType.UNARY,
            allow_none=allow_none,
            strict_no_args=False,
        )

    @staticmethod
    def keyword(allow_none: bool):
        return FunctionInputConfig(
            input_type=FunctionInputType.KEYWORD,
            allow_none=allow_none,
            strict_no_args=False,
        )

    @staticmethod
    def nullary_keyword():
        return FunctionInputConfig(
            input_type=FunctionInputType.KEYWORD,
            allow_none=True,
            strict_no_args=True,
        )

    @staticmethod
    def nullary_pos():
        return FunctionInputConfig(
            input_type=FunctionInputType.UNARY,
            allow_none=True,
            strict_no_args=True,
        )


@dataclass
class FunctionOutputConfig:
    """
    This class determine what kinds of output should be returned for a function
    Args:
        cast_to_json: cast the output str as json.
    """
    cast_to_json: bool = False


class Example:
    """
    Input and output pair example.
    The `input` field of `Example` can be one of `None`, a `str` value, or a `dict` object.
    The `output` field of `Example` can be either a `str` value, a `dict`/`list` object.

    If input is a dict, all value in input.values() must be able to render as a string with f-string i.e. `f"{value}"`.

    Args:
        input: `None`, a `str` value, or a `dict` object.
        output: `str` value, or a `dict`/`list` object.
    """
    input: Optional[FunctionInput] = None
    output: FunctionOutput

    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output

    @property
    def input_type(self) -> Optional[FunctionInputType]:
        return FunctionInputType.of_value(self.input)


@dataclass
class InputCounter:
    KEYWORD: int = 0
    POS: int = 0
    NONE: int = 0

    def count(self, input_value: Optional[FunctionInput]):
        t = FunctionInputType.of_value(input_value)
        if t is None:
            self.NONE += 1
        elif t == FunctionInputType.UNARY:
            self.POS += 1
        elif t == FunctionInputType.KEYWORD:
            self.KEYWORD += 1

    def to_config(
            self,
            default_args: Optional[FunctionInput] = None,
            strict_no_args: bool = True,
    ) -> FunctionInputConfig:
        """

        :param default_args: if default_args are provided, and has no typing conflict with examples, we will allow none.
        :param strict_no_args: if this is set to True and all examples has None as input, the function
                               will be a nullary function.
        :return:
        """
        cond = (self.has_keyword, self.has_positional, self.has_none)
        default_args_type = FunctionInputType.of_value(default_args)
        if cond == (True, True, True):
            # Keyword, Unary, and None
            raise ValueError('Example list contains both keyword and unary input.')
        elif cond == (True, True, False):
            # Keyword and Unary
            raise ValueError('Example list contains both keyword and unary input.')
        elif cond == (True, False, True):
            # Keyword and None
            if default_args_type != FunctionInputType.KEYWORD:
                raise ValueError(
                    f'default_args and example input type differ({default_args_type} != {FunctionInputType.KEYWORD}).')
            return FunctionInputConfig.keyword(True)
        elif cond == (True, False, False):
            # Has only keyword
            # if default args is provided, we will allow none
            return FunctionInputConfig.keyword(default_args_type == FunctionInputType.KEYWORD)
        elif cond == (False, True, True):
            # Has positional and None
            if default_args_type != FunctionInputType.UNARY:
                raise ValueError(
                    f'default_args and example input type differ({default_args_type} != {FunctionInputType.UNARY}).')
            return FunctionInputConfig.unary(True)
        elif cond == (False, True, False):
            # Has only positional
            # if default args is provided, we will allow none
            return FunctionInputConfig.unary(default_args_type == FunctionInputType.UNARY)
        elif cond == (False, False, True):
            # Only None input, we will determine input type using default args.
            if default_args_type == FunctionInputType.KEYWORD:
                if strict_no_args:
                    return FunctionInputConfig.nullary_keyword()
                else:
                    return FunctionInputConfig.keyword(True)
            elif default_args_type == FunctionInputType.UNARY:
                if strict_no_args:
                    return FunctionInputConfig.nullary_pos()
                else:
                    return FunctionInputConfig.unary(True)
            elif default_args_type is None:
                raise ValueError('You must provide default args for Nullary function.')
        elif cond == (False, False, False):
            raise ValueError('No example input observed')

    @property
    def has_keyword(self):
        return self.KEYWORD > 0

    @property
    def has_none(self):
        return self.NONE > 0

    @property
    def has_positional(self):
        return self.POS > 0


@dataclass
class OutputCounter:
    str_count: int = 0
    json_count: int = 0

    def count(self, output_value: FunctionOutput):
        if isinstance(output_value, str):
            self.str_count += 1
        elif isinstance(output_value, dict) or isinstance(output_value, List):
            self.json_count += 1
        else:
            raise ValueError("output_value must be str, dict or list")

    def to_config(self) -> FunctionOutputConfig:
        ret = FunctionOutputConfig()

        cond = (self.has_json, self.has_str)
        if cond == (True, True):
            raise ValueError('Example list contains both string and dict outputs.')
        elif cond == (True, False):
            # json only
            ret.cast_to_json = True
        elif cond == (False, True):
            # str only
            ret.cast_to_json = False
        else:
            raise ValueError('No example output observed.')
        return ret

    @property
    def has_json(self) -> bool:
        return self.json_count > 0

    @property
    def has_str(self) -> bool:
        return self.str_count > 0
