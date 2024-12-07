import abc
import json
import os
from typing import TypedDict, Literal, Any, Optional, Generator, List, Union
import re

from .constants import DEFAULT_BATCH_FOLDER
from .utils import try_parse_json


def get_path_safe_name(name: str) -> str:
    """
    Sanitize a name so it can be used as a normal filename.

    Removes or replaces characters not allowed in filenames on most operating systems.

    :param name: The original name to sanitize.
    :return: A sanitized filename-safe string.
    """
    # Remove characters that are invalid for filenames (e.g., < > : " / \ | ? *)
    safe_name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    # Limit the length to avoid filesystem limitations (e.g., 255 characters)
    safe_name = safe_name[:255]
    # Strip leading/trailing dots or spaces (not allowed in some cases)
    safe_name = safe_name.strip('. ')

    return safe_name


class LLMFunctionOutput:
    output: Union[str, List[str]]
    n: int
    preferred_format: Literal['text', 'json']

    def __init__(self, output, n, preferred_format):
        self.output = output
        self.n = n
        self.preferred_format = preferred_format

    @staticmethod
    def from_json(json_value):
        return LLMFunctionOutput(
            json_value.get('output'),
            json_value.get('n'),
            json_value.get('preferred_format')
        )

    def as_json(self):
        return json.loads(self.raw())

    def raw(self):
        return self.output

    @property
    def value(self):
        if self.preferred_format == 'json':
            if self.n == 1:
                json_value, parsed = try_parse_json(self.output)
                if parsed:
                    return json_value
            else:
                output_list = []
                for o in self.output:
                    json_value, parsed = try_parse_json(o)
                    if parsed:
                        output_list.append(json_value)
                    else:
                        output_list.append(o)
        return self.output

    def __repr__(self):
        if self.n == 1:
            return f'Output: {self.output}'
        else:
            lines = "\n".join(self.output)
            return f'Outputs: \n{lines}'

    def __str__(self):
        return self.output

    def serialize_to_dict(self):
        return dict(
            output=self.output,
            n=self.n,
            preferred_format=self.preferred_format,
        )


class LLMFunction:
    name: str

    def __repr__(self):
        return f'llm function {self.name}'

    def __init__(self, name: str):
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.handle_call(args=args, kwargs=kwargs)

    @property
    def filesafe_name(self):
        return get_path_safe_name(self.name)

    @abc.abstractmethod
    def handle_call(self, *args, **kwargs):
        pass

    def batch(self, name, base_folder=DEFAULT_BATCH_FOLDER, auto_start: bool = False):
        fn_batches_folder = os.path.join(base_folder, self.filesafe_name)
        batch_name = name
        batch_folder = os.path.join(fn_batches_folder, batch_name)
        os.makedirs(batch_folder, exist_ok=True)
        status_file = os.path.join(batch_folder, '__fn_batch_meta__.json')
        if not os.path.exists(status_file):
            with open(status_file, 'w') as out:
                json.dump({
                    'status': 'created'
                }, out)

        return self._handle_get_batch(
            name, batch_folder,
            auto_start=auto_start,
        )

    @abc.abstractmethod
    def _handle_get_batch(self, name, batch_folder, auto_start: bool = False):
        pass

    def list_batch_names(self, base_folder=DEFAULT_BATCH_FOLDER) -> Generator[str, None, None]:
        fn_batches_folder = os.path.join(base_folder, self.filesafe_name)
        ret = []
        if os.path.isdir(fn_batches_folder):
            for f in os.listdir(fn_batches_folder):
                sub_folder = os.path.join(fn_batches_folder, f)
                if os.path.isdir(sub_folder):
                    status_file = os.path.join(sub_folder, '__fn_batch_meta__.json')
                    if os.path.isfile(status_file):
                        ret.append(f)
        return ret

    def search_batch_by_prefix(self, prefix, base_folder=DEFAULT_BATCH_FOLDER):
        for b in self.list_batch_names(base_folder=base_folder):
            if b.startswith(prefix):
                yield prefix


class BatchMetaType(TypedDict):
    status: Literal['created', 'processing', 'error', 'finished']
    # meta: Optional[dict[str, Any]]


class LLMFunctionBatch:
    _auto_start: bool
    folder: str
    name: str

    def __init__(self, name: str, folder: str, auto_start: bool = False):
        self.name = name
        self.folder = folder
        self._auto_start = auto_start
        self.input_writer_fd = None

    def __repr__(self):
        return f'function batch processor: {self.name} is stored at {self.folder}'

    @property
    def write_lock_file(self):
        return os.path.join(self.folder, 'mkb.write.lock')

    def _can_write(self):
        return os.path.isfile(
            self.write_lock_file
        )

    def create_lock(self):
        with open(self.write_lock_file, 'w') as out:
            out.write('1')

    def _remove_lock(self):
        os.remove(self.write_lock_file)

    def get_input_file_writer(self):
        if self.input_writer_fd is None:
            if not self._can_write():
                parent_dir = os.path.dirname(self.input_file)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)
                self.input_writer_fd = open(self.input_file, 'a')
            else:
                raise ValueError('You cannot reuse existing batch.')
        return self.input_writer_fd

    def close(self):
        if self.input_writer_fd is not None:
            if not self.input_writer_fd.closed:
                self.input_writer_fd.close()
        self.create_lock()

    def add(self, *args, **kwargs) -> None:
        input_record = {}

        if args:
            input_record['args'] = args

        if kwargs:
            meta = kwargs.get('__meta__', None)
            if meta:
                input_record['meta'] = meta
                kwargs = {k: v for k, v in kwargs.items() if k != '__meta__'}

            input_record['kwargs'] = kwargs

        self.get_input_file_writer().write(json.dumps(input_record) + '\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._auto_start:
            self.start_batch()
        else:
            self.close()
            print('auto_start is set to False, '
                  'please call batch.start_batch() to start processing this batch.')

    @property
    def meta_file(self):
        return os.path.join(self.folder, '__fn_batch_meta__.json')

    @property
    def input_file(self):
        return os.path.join(self.folder, '__input__.jsonl')

    @property
    def output_file(self):
        return os.path.join(self.folder, '__output__.jsonl')

    def meta(self) -> BatchMetaType:
        if os.path.exists(self.meta_file):
            with open(self.meta_file) as fd:
                return json.load(fd)
        else:
            return {
                'status': 'created'
            }

    def set_meta(self, meta: BatchMetaType):
        with open(self.meta_file, 'w') as out:
            return json.dump(meta, out)

    @abc.abstractmethod
    def sync_remote(self):
        pass

    @property
    def start_lock_file(self):
        return os.path.join(self.folder, 'mkb.start.lock')

    def lock_process(self):
        with open(self.start_lock_file, 'w') as out:
            out.write('1')

    def can_start_batch(self):
        return not os.path.isfile(self.start_lock_file)

    @abc.abstractmethod
    def start_batch(self):
        self.close()
        if self.can_start_batch():
            self.handle_start_batch()
        else:
            raise ValueError('Batch has already started.')
        self.lock_process()

    @abc.abstractmethod
    def handle_start_batch(self):
        pass

    def iter_inputs(self):
        if self.input_writer_fd is not None and not self.input_writer_fd.closed:
            raise ValueError('you should close the input file first.')
        with open(self.input_file) as fd:
            for line in fd:
                yield json.loads(line)

    def iter_outputs(self):
        if os.path.isfile(self.output_file):
            with open(self.output_file) as fd:
                for line in fd:
                    item = json.loads(line)
                    input_item = item['input']
                    output_item = item['output']
                    yield input_item, LLMFunctionOutput.from_json(output_item)

    def current_stage(self) -> Literal['constructing', 'processing', 'finalized']:
        if self._can_write():
            return 'constructing'
        if self.can_start_batch():
            return 'processing'
        return 'finalized'
