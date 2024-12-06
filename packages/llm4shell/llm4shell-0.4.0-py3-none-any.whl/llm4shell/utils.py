#!/usr/bin/env python3
import difflib
import os
from pathlib import Path
import sys

import click
import litellm
import parse
from click.testing import CliRunner
from colored import Fore, Style
from litellm import (  # Ensure litellm is installed: pip install litellm
    ModelResponse,
    completion,
)
from loguru import logger


def highlight_differences(s1, s2):
    # Split the strings into lists of characters
    s1_chars = list(s1)
    s2_chars = list(s2)

    # Generate the diff output
    diff = difflib.ndiff(s1_chars, s2_chars)

    result = ""
    last_color = None
    for c in diff:
        code = c[0:2]
        char = c[2:]
        if code == "  ":  # No change
            color = Fore.white
        elif code == "- ":  # Deletion
            color = Fore.red
        elif code == "+ ":  # Insertion
            color = Fore.green
        else:
            continue  # Ignore lines starting with '? '
        if color != last_color:
            result += color
            last_color = color
        result += char
    result += Style.reset
    return result


def check_click(model:str='openai/gpt-4o-mini',
                api_env_variable:str='OPENROUTER_API_KEY',
                openrouter_app_name: str|None = None,
                openrouter_site_url: str|None = "localhost",

                ):
    if api_env_variable is not None:
        litellm.openrouter_key = os.getenv(api_env_variable)
    if openrouter_site_url is not None:
        os.environ["OR_SITE_URL"] = openrouter_site_url

    def decorator(cmd):
        # Store the original main function of the Click command
        original_main = cmd.main

        def new_main(*args, **kwargs):
            try:
                # Set standalone_mode=False to prevent Click from exiting on exceptions
                kwargs["standalone_mode"] = False
                return original_main(*args, **kwargs)

            except click.ClickException as e:
                logger.warning(e)

                # An error occurred; get the help message
                help_message = cmd.help

                # Get the command-line arguments
                args = [Path(sys.argv[0]).name]
                for arg in sys.argv[1:]:
                    if ' ' in arg:
                        args.append(f'"{arg}"')
                    else:
                        args.append(arg)

                if openrouter_app_name is None or openrouter_app_name == 'auto':
                    os.environ["OR_APP_NAME"] = args[0]
                else:
                    os.environ["OR_APP_NAME"] = openrouter_app_name

                # Call the fix_click function with args and help_message
                try:
                    fix_click(args, e, help_message, model=model)
                except Exception:
                    logger.warning("Exception during LLM call")
                    raise e
            except Exception as e:
                raise e

        # Replace the main function with our custom one
        cmd.main = new_main
        return cmd

    return decorator


def fix_click(args, exception, help_message, model="openai/gpt-4o-mini"):
    logger.warning(f"Let's invoke {model} for fixing it.")
    args = " ".join(args)
    user_messages = [
        f"""
        During execution the following exception happened:
        ```
        {repr(exception).strip()}
        ```

        Command line was:
        ```
        {args}
        ```
        The tool has the following help message:
        ```
        {help_message.strip()}
        ```
        Provide a short explanation what went wrong and provide a fix command inside triple-backticks block.
        """
    ]

    response = llm(
        system_prompt="Act as an expert Linux user, proficient in command lines and every tools. Fix the command line call!",
        user_messages=user_messages,
        model=model,
    )

    if "```" in response:
        try:
            explanation, code_block, _ = parse.parse("{}```{}```{}", response)
            code_block = code_block.strip().split("\n")[-1]
            print(f"{Fore.white}{explanation.strip()}\n\n", file=sys.stderr)
            print("Changes:\n", file=sys.stderr)
            print(
                highlight_differences(args.strip(), code_block.strip()), file=sys.stderr
            )
            print("\nFixed command:\n", file=sys.stderr)
            print(f"{Fore.green}{code_block.strip()}{Style.reset}\n", file=sys.stderr)
        except Exception:  # parsing error, let's ignore it for now
            print(response, file=sys.stderr)
    else:
        print(response, file=sys.stderr)


def llm(
    system_prompt,
    user_messages,
    model,
    api_key=None,
    or_site_url=None,
    or_app_name=None,
):
    """
    Send prompts to OpenRouter.ai using LiteLLM and receive responses.
    """

    if not model.startswith('openrouter'):
        model=f'openrouter/{model}'

    if litellm.openrouter_key is None:
        raise RuntimeError(
            "API key not found. Please set the OPENROUTER_API_KEY environment variable to provide an API key."
        )
    if or_site_url:
        logger.info(f"Using OR_SITE_URL: {or_site_url}")
        os.environ["OR_SITE_URL"] = or_site_url
    if or_app_name:
        logger.info(f"Using OR_APP_NAME: {or_app_name}")
        os.environ["OR_APP_NAME"] = or_app_name

    # Construct messages array
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if user_messages:
        messages.extend([{"role": "user", "content": c} for c in user_messages])

    # Send the request using LiteLLM
    try:
        response = completion(model=model, messages=messages)
    except Exception as e:
        logger.error(f"An error occurred while communicating with OpenRouter.ai: {e}")
        raise

    # Process the response
    try:
        if isinstance(response, ModelResponse):
            choices = response.get("choices", [])
            if choices and isinstance(choices, list):
                result = choices[0].get("message", {}).get("content", "").strip()
            else:
                logger.error("No 'choices' found in the response.")
                raise RuntimeError("No 'choices' found in the response.")
        elif isinstance(response, str):
            result = response.strip()
        else:
            logger.error("Unexpected response format.")
            sys.exit(1)

        if not result:
            logger.error("Received empty response from OpenRouter.ai.")
            raise RuntimeError("Received empty response from OpenRouter.ai.")

    except Exception as e:
        logger.error(f"Error processing the response: {e}")
        raise RuntimeError(f"Error processing the response: {e}")

    return result
