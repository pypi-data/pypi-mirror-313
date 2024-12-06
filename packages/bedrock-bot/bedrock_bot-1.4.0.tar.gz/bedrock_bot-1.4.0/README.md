# Bedrock Bot

This project is a basic CLI-based chat bot that uses Bedrock to resolve questions. It can take input from stdin, CLI arguments or interactively when no parameters have been passed.

## Installation

1. `pip install bedrock-bot`
2. You will also need some AWS credentials available in your shell (any usual way works - CLI configured IAM user access key/secret keys, environment variables, etc)
3. Bedrock requires you to opt in to models in order to use them

## Usage

```bash
Usage: bedrock [OPTIONS] [ARGS]...

Options:
  -r, --region TEXT               The AWS region to use for requests. If no
                                  default region is specified, defaults to us-
                                  east-1
  --raw-output TEXT               Don't interpret markdown in the AI response
  -m, --model [Claude-3-Haiku|Claude-3-Sonnet|Mistral-Large]
                                  The model to use for requests
  -v, --verbose                   Enable verbose logging messages
  -i, --input-file FILENAME       Read in file(s) to be used in your queries
  --help                          Show this message and exit.
```

Directly as a chat bot:

```bash
$ bedrock

Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?
My name is Claude.
```

Using CLI arguments:

```bash
$ bedrock "Hi, what is your name?"

Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?
My name is Claude. It's nice to meet you!
```

Using stdin (Note that you can only use this for one-shot questions as input is reserved by your pipe to stdin and is not an interactive TTY any more):

```bash
$ echo "Hi, what is your name?" > input-file

$ cat input-file | bedrock
Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> Hi, what is your name?

My name is Claude. I'm an AI created by Anthropic. It's nice to meet you!                                                         


Note that you can only do one-shot requests when providing input via stdin
```

Asking about a file:

```bash
$ bedrock --input-file bedrock_bot/models/base_model.py write unit tests using pytest for this file
Hello! I am an AI assistant powered by Amazon Bedrock and using the model Claude-3-Haiku. Enter 'quit' or 'exit' at any time to exit. How may I help you today?
(You can clear existing context by starting a query with 'new>' or 'reset>')

> write unit tests using pytest for this file
To write unit tests for the bedrock_bot/models/base_model.py file using pytest, you can create a test_base_model.py file in the tests directory. Here's an example of how you can structure the tests:


 import json
 from unittest.mock import patch, MagicMock
 import pytest
 from bedrock_bot.models.base_model import _BedrockModel, ConversationRole

 class TestBedrockModel:
     def setup_method(self):
         self.model = _BedrockModel("test-model-id")

     def test_reset(self):
         self.model.append_message(ConversationRole.USER, "Hello")
         assert len(self.model.messages) == 1
         self.model.reset()
         assert len(self.model.messages) == 0
...
```

## Shell auto-complete

Shell auto-complete is also supported.

### ZSH

1. `_BEDROCK_COMPLETE=zsh_source bedrock > ~/.bedrock-completion.zsh`
2. Add the following to your `~/.zshrc`: `source ~/.bedrock-completion.zsh`

### Bash

1. `_BEDROCK_COMPLETE=bash_source bedrock > ~/.bedrock-completion.bash`
2. Add the following to your `~/.bashrc`: `source ~/.bedrock-completion.bash`
