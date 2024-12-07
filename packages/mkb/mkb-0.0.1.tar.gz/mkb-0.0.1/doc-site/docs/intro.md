---
sidebar_position: 1
---

# Getting Started

## Another way to program a machine

When programming a machine to achieve a specific goal, we need to communicate our intent to it. Typically, this involves designing a detailed procedure and writing precise instructions in a programming language like Python.

However, some tasks are challenging to describe with step-by-step procedures because we often perform them intuitively without fully understanding the process. For example:
* Determining the sentiment of a given sentence.
* Identifying dishes mentioned in a food review.

`mkb` introduces an alternative way to express our intentions to machines. Instead of relying on imperative procedures, it uses human language instructions and examples. Under the hood, it leverages language models and few-shot learning techniques to interpret and execute these instructions.

## Getting Started

```bash
pip install mkb
```

## Hello World

```python title="An expensive hello world function in python."
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

from mkb import def_fn


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction('Print Hello World')
@def_fn.with_example(output="Hello World")
@def_fn.with_default_args('Print Hello World')
def hello_world():
    # any code you wrote here will be ignored.
    pass


out = hello_world()
print(out.value)
# hello world
```

## Quick Tutorial

### Define a function

Use decorators from `from mkb import def_fn` to define a few-shot learning based function, currently any function
definition should include at least the following decorators in their decorators chains:

* an implementation selector such as `def_fn.openai()` should be always on the top of the decorators
  chains, and you can provide custom inference parameters, for
  example: `def_fn.openai(opts=GptApiOptions(temperature=1.0))`   
  the `OpenAI` client object and any custom.
* use `def_fn.with_instruction(instruction: str)` to provide instructions.
* use `def_fn.with_example(input, output)` to provide examples.

#### def_fn.openai

```python
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction('Print Hello World')
@def_fn.with_example(output="Hello World")
@def_fn.with_default_args('Print Hello World')
def hello_world():
    pass


out = hello_world()
out

# Output: Hello World
```

#### def_fn.with_example

```python title="define a nullary function for def_fn.with_example"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction("Given a username, say welcome to the user.")
@def_fn.with_example(input='John', output="Welcome, John!")
@def_fn.with_default_args('New User')
def greet_new_user():
    # any code you wrote here will be ignored.
    pass
```

```python title="define a unary function for def_fn.with_example"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction("Extract all companies' tickers mentioned in the news title.")
@def_fn.with_example(
    input="Why Kroger, Albertsons need to merge immediately to compete with Walmart",
    output="$KR, $ACI, $WMT",
)
def find_tickers():
    # any code you wrote here will be ignored.
    pass
```

```python title="define a keyword function for def_fn.with_example"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction("Given a username, say welcome to the user.")
@def_fn.with_example(input='John', output="Welcome, John!")
@def_fn.with_default_args('New User')
def greet_new_user():
    # any code you wrote here will be ignored.
    pass
```

```python title="define function with strcutured(json/dict/list) output for def_fn.with_example"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction(
    "Extract all wikipedia entities mentioned in the text and format them in JSON as following [{name: '', url: ''}].")
@def_fn.with_example(
    input="An analog computer or analogue computer is a type of computer that uses the continuous variation"
          "aspect of physical phenomena such as electrical, mechanical, or hydraulic quantities (analog signals) "
          "to model the problem being solved.",
    output=[
        {
            "name": "computer",
            "url": "https://en.wikipedia.org/wiki/Computation",

        },
        {
            "name": "electrical",
            "url": "https://en.wikipedia.org/wiki/Electrical_network",
        },
        {
            "name": "mechanical",
            "url": "https://en.wikipedia.org/wiki/Mechanics",
        },
        {
            "name": "hydraulic",
            "url": "https://en.wikipedia.org/wiki/Hydraulics",
        },
        {
            "name": "analog signals",
            "url": "https://en.wikipedia.org/wiki/Analog_signal",
        }
    ]
)
def extract_wiki_links(text):
    # any code you wrote here will be ignored.
    pass


out = extract_wiki_links(
    "The term machine learning was coined in 1959 by Arthur Samuel, an IBM employee and pioneer in the field of computer gaming and artificial intelligence.")

# To access raw text output from LLM.
print(out.raw())

# to access output, noted this may fail if language model backed failed to produce a valid json output.
print(out.value)
```

#### def_fn.with_default_args

```python title="set default args for def_fn.with_default_args"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction("Given a username, say welcome to the user.")
@def_fn.with_example(input='John', output="Welcome, John!")
@def_fn.with_default_args('New User')
def greet_new_user():
    # any code you wrote here will be ignored.
    pass


out = greet_new_user()
print(out.value)
# Welcome, New User!

out = greet_new_user('Bob')
print(out.value)
# Welcome, Bob!
```

#### def_fn.require_args

You can use require_args to set the required keyword arguments for your function, and the function will throw exception
when any of those values missing from `kwargs`.

```python title="set required args for def_fn.require_args"
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction("Given a username, say welcome to the user.")
@def_fn.with_example(input={'username': 'John'}, output="Welcome, John!")
@def_fn.require_args('username')
def greet_new_user():
    # any code you wrote here will be ignored.
    pass


out = greet_new_user(username='Bob')
print(out.value)
# Welcome, Bob!

greet_new_user(user='Alice')
# This line will throw error as keyword argument `username` is required
```

### Using the output

```python
out = greet_new_user(username='Bob')
print(out.value)
```

## Batch Mode

Most language model backend nowadays offer batch mode with significant saving in cost if you can afford a delayed
response,

You can call `mkb` function in batch mode to take advantage of this, as `mkb` functions' batch mode` offers an easy
interface to submit
batch job, check status, and, fetching remote response.

```python
from mkb import def_fn
from mkb.impl.openai import GptApiOptions
from openai import OpenAI

openai_client = OpenAI(api_key='**********************')

my_gpt_opts = GptApiOptions(temperature=0)


@def_fn.openai(client=openai_client, opts=my_gpt_opts)
@def_fn.with_instruction(
    "Extract all wikipedia entities mentioned in the text and format them in JSON as following [{name: '', url: ''}].")
@def_fn.with_example(
    input="An analog computer or analogue computer is a type of computer that uses the continuous variation"
          "aspect of physical phenomena such as electrical, mechanical, or hydraulic quantities (analog signals) "
          "to model the problem being solved.",
    output=[
        {
            "name": "computer",
            "url": "https://en.wikipedia.org/wiki/Computation",

        },
        {
            "name": "electrical",
            "url": "https://en.wikipedia.org/wiki/Electrical_network",
        },
        {
            "name": "mechanical",
            "url": "https://en.wikipedia.org/wiki/Mechanics",
        },
        {
            "name": "hydraulic",
            "url": "https://en.wikipedia.org/wiki/Hydraulics",
        },
        {
            "name": "analog signals",
            "url": "https://en.wikipedia.org/wiki/Analog_signal",
        }
    ]
)
def extract_wiki_links(text):
    # any code you wrote here will be ignored.
    pass

######################
# Create a batch job
######################

batch = extract_wiki_links.create_batch('my-batch')
batch.add(
    "The term machine learning was coined in 1959 by Arthur Samuel, an IBM employee and pioneer in the field of computer gaming and artificial intelligence.")
batch.add(
    "Fermat and Lagrange found calculus-based formulae for identifying optima, while Newton and Gauss proposed iterative methods for moving towards an optimum.")

######################
# Submit the batch job to language model backend
######################
batch.start_batch()


######################
# Sync remote status, 
# batch.sync_remote() will fetch results if available.
######################
status = batch.sync_remote()
print(status)
print(status['openai']['batch_job'])

######################
# Sync remote status, 
# once the batch is completed, you can iterate through the results using `iter_outputs`
######################
 
for input_args, output in batch.iter_outputs():
    print(output)
```

## More examples
