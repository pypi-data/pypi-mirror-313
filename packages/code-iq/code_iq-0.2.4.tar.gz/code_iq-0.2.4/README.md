# CodeIQ: A Next-Generation AI-Powered Development Assistant

![CI](https://github.com/youzarsiph/code-iq/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/youzarsiph/code-iq/actions/workflows/cd.yml/badge.svg)
![Black](https://github.com/youzarsiph/code-iq/actions/workflows/black.yml/badge.svg)
![Ruff](https://github.com/youzarsiph/code-iq/actions/workflows/ruff.yml/badge.svg)
[![PyPI - Version](https://img.shields.io/pypi/v/code-iq?logo=pypi&logoColor=white)](https://pypi.org/project/code-iq/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/code-iq?logo=python&logoColor=white)](https://pypi.org/project/code-iq/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/code-iq?logo=pypi&logoColor=white)](https://pypi.org/project/code-iq/)
[![PyPI - Format](https://img.shields.io/pypi/format/code-iq?logo=pypi&logoColor=white)](https://pypi.org/project/code-iq/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/code-iq?logo=pypi&logoColor=white)](https://pypi.org/project/code-iq/)
[![PyPI - License](https://img.shields.io/pypi/l/code-iq?logo=pypi&logoColor=white)](https://pypi.org/project/code-iq/)

## Overview

CodeIQ is an advanced AI-powered command-line interface (CLI) tool designed to enhance coding efficiency and productivity. Utilizing the sophisticated capabilities of Qwen2.5-Coder-32B-Instruct, CodeIQ offers intelligent code completions, error detection, and automated coding functionalities. This empowers developers to streamline their workflows with precision and ease, making it an invaluable resource for professionals at all levels.

## Key Features

- **Contextual Code Completions**: Receive accurate, contextually relevant code suggestions to accelerate development with minimal errors.
- **Natural Language Interaction**: Engage with CodeIQ using natural language for detailed explanations, debugging tips, and guidance.
- **Multi-Language Support**: Seamlessly write and execute code in over 100 programming languages with CodeIQ's comprehensive integration.
- **Personalized Learning**: Continuously improve recommendations based on user interactions, providing personalized and immediate insights.

## Getting Started

### Prerequisites

- **Python**: CodeIQ requires Python 3.10 or higher. Ensure you have the correct version installed.
- **Hugging Face Token**: Create an account on [Hugging Face](https://huggingface.co/) and obtain an API token.

### Installation

To install CodeIQ, execute the following command:

```bash
pip install code-iq
```

Ensure that your Hugging Face token is set as an environment variable:

- **Unix-based Systems (Linux, macOS):**

  ```bash
  export HF_TOKEN=hf_your_token_here
  ```

- **Windows (PowerShell):**

  ```powershell
  $env:HF_TOKEN = "hf_your_token_here"
  ```

## Usage

Launch CodeIQ with the following command:

```console
code-iq [OPTIONS] COMMAND [ARGS]...
```

### Options

- `--install-completion`: Install shell completion for CodeIQ.
- `--show-completion`: Display the completion script for the current shell.
- `--help`: Display this help message and exit.

### Commands

- `ai`: Utilize AI-driven functionalities to generate code, obtain explanations, and perform tasks.
- `chat`: Enable real-time conversations for troubleshooting, guidance, and inquiries.
- `complete`: Receive code completion suggestions based on context and best practices.
- `document`: Assist in generating and formatting documentation.
- `enhance`: Apply optimizations or improvements to code.
- `review`: Conduct thorough code reviews for quality and adherence to standards.
- `scan`: Identify vulnerabilities and potential issues within codebases.
- `test`: Facilitate the creation and execution of tests.

#### `code-iq ai`

Leverage AI functionalities to generate code snippets, obtain suggestions, and perform tasks.

**Examples:**

```bash
code-iq ai "Generate a function to calculate the area of a circle"
code-iq ai -c code.py "Explain the code"
code-iq ai -o output.md "How to install HuggingFace Transformers?"
```

**Usage:**

```console
code-iq ai [OPTIONS] PROMPT
```

**Arguments:**

- `PROMPT`: The prompt or instruction for the AI. [required]

**Options:**

- `-c, --code FILENAME`: Include a code file in the prompt.
- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 2048]
- `--help`: Display this help message and exit.

#### `code-iq chat`

Engage in real-time conversations for troubleshooting, guidance, or general inquiries.

**Examples:**

```bash
# Start a chat session
code-iq chat

# Export chat history
code-iq chat -e chat_history.json

# Import chat history
code-iq chat -h chat_history.json

# Import chat history and export after session
code-iq chat -h chat_history.json -e chat_history.json
```

**Usage:**

```console
code-iq chat [OPTIONS]
```

**Options:**

- `-e, --export FILENAME`: Export the chat history to this file.
- `-h, --history FILENAME`: Import a previous chat history from this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 2048]
- `--help`: Display this help message and exit.

#### `code-iq complete`

Receive suggestions to complete partially written code based on context and best practices.

**Examples:**

```bash
code-iq complete 'def hello_world():'
code-iq complete -l python 'def hello_world():'
code-iq complete -o code-completions.md 'def hello_world():'
```

**Usage:**

```console
code-iq complete [OPTIONS] CODE
```

**Arguments:**

- `CODE`: The code snippet for which to receive completions. [required]

**Options:**

- `-l, --lang TEXT`: Specify the programming language of the code snippet.
- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 128]
- `--help`: Display this help message and exit.

#### `code-iq document`

Generate and manage code documentation, including comments, README files, and technical documentation.

**Examples:**

```bash
code-iq document code.py
code-iq document code.py -o code-docs.md
```

**Usage:**

```console
code-iq document [OPTIONS] CODE
```

**Arguments:**

- `CODE`: The code file for which to generate documentation. [required]

**Options:**

- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 2048]
- `--help`: Display this help message and exit.

#### `code-iq enhance`

Apply improvements or optimizations to existing code, including refactoring and performance tuning.

**Examples:**

```bash
code-iq enhance code.py
code-iq enhance code.py -o code-enhancements.md
```

**Usage:**

```console
code-iq enhance [OPTIONS] CODE
```

**Arguments:**

- `CODE`: The code file to enhance. [required]

**Options:**

- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 2048]
- `--help`: Display this help message and exit.

#### `code-iq review`

Analyze code for potential issues and adherence to coding standards.

**Examples:**

```bash
code-iq review code.py
code-iq review code.py -o code-review.md
```

**Usage:**

```console
code-iq review [OPTIONS] CODE
```

**Arguments:**

- `CODE`: The code file to review. [required]

**Options:**

- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number of tokens in the response. [Default: 2048]
- `--help`: Display this help message and exit.

#### `code-iq scan`

Identify vulnerabilities, bugs, or areas for improvement within codebases.

**Examples:**

```bash
code-iq scan code.py
code-iq scan code.py -o code-scan.md
```

**Usage:**

```console
code-iq scan [OPTIONS] CODE
```

**Arguments:**

- `CODE`: The code file to scan. [required]

**Options:**

- `-o, --output FILENAME`: Write the response to this file.
- `-t, --max-tokens INTEGER`: Limit the number
