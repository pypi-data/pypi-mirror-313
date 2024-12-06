#!/usr/bin/env python3
import os
import sys

import click
from loguru import logger

from llm4shell.utils import check_click, llm

# Configure loguru to log messages to stderr
logger.remove()
logger.add(sys.stderr, level="INFO")

API_KEY_ENV_VAR = "OPENROUTER_API_KEY"

@check_click(model='openai/gpt-4o-mini',
            api_env_variable='OPENROUTER_API_KEY',
            openrouter_app_name = None,
            openrouter_site_url= "localhost")
@click.command()
@click.option(
    "-i",
    "--instruction",
    "instructions",
    type=str,
    required=True,
    multiple=True,
    help="Instruction prompt string. Can be specified multiple times for multiple instructions.",
)
@click.option(
    "-s",
    "--system",
    type=str,
    required=False,
    default=None,
    help="System prompt to provide context to the model.",
)
@click.option(
    "--input",
    "input_source",
    default=None,
    type=click.Path(exists=False, dir_okay=False),
    required=False,
    help='Path to input file or "-" for stdin. Provides additional context to the model.',
)
@click.option(
    "-m",
    "--model",
    type=str,
    required=True,
    help="Model identifier to be used for the API request.",
)
@click.option(
    "-o",
    "--output",
    type=str,
    default="-",
    help='Output file path or "-" for stdout. Determines where the response will be written.',
)
@click.option(
    "-t",
    "--api-token",
    type=str,
    default=os.getenv(API_KEY_ENV_VAR),
    help=f"OpenRouter.ai API token. If not provided, the tool will use the {API_KEY_ENV_VAR} environment variable.",
)
def main(
    instructions: list[str],
    system: str | None,
    input_source: str | None,
    model: str,
    output: str,
    api_token: str | None,
) -> None:
    """
    A command-line interface (CLI) tool for interacting with OpenRouter.ai's API.

    This tool allows users to send one or more instructions to an AI model and receive responses.
    It supports reading input from a file or standard input, specifying the system prompt, and
    selecting the model to use for processing. The result can be written to a file or printed
    directly to standard output.

    Parameters:
        instructions (List[str]): Instruction prompt strings to guide the model.
        system (Optional[str]): A system prompt to provide a guiding context to the model (optional).
        input_source (Optional[str]): Path to a file or '-' for standard input to provide additional data to the model.
        model (str): The identifier for the model to be used in the API call.
        output (str): Path for output file or '-' for standard output.
        api_token (Optional[str]): API token for authenticating requests. Defaults to the value in the OPENROUTER_API_KEY environment variable.

    Example:
        ./tool.py -i "Translate to Spanish" --input "data.txt" -m "text-davinci" -o result.txt --api-token "your_api_key"

    Raises:
        SystemExit: Exits the program if an error occurs during execution, such as missing API token or output file writing errors.
    """
    logger.info("Starting the CLI tool.")

    # Check if the API token is provided via CLI or environment variable
    if api_token:
        logger.info("Using API token provided via CLI option.")
        api_key = api_token
    else:
        logger.error(
            f"API key not found. Please set the {API_KEY_ENV_VAR} environment variable or use the --api-token option."
        )
        sys.exit(1)

    # Combine instruction prompts
    user_messages = list(instructions)

    # Read user message from input source
    if input_source is None:
        pass
    elif input_source == "-":
        logger.info("Reading user message from stdin.")
        user_message = sys.stdin.read().strip()
        user_messages.append(f"```\n{user_message}```")
    elif input_source:
        logger.info(f"Reading user message from file: {input_source}")
        try:
            with open(input_source, encoding="utf-8") as f:
                user_message = f.read().strip()
            user_messages.append(f"```\n{user_message}```")
        except FileNotFoundError:
            logger.error(f"Input file {input_source} not found.")
            sys.exit(1)

    # Call the llm function (interfacing with the OpenRouter.ai API)
    logger.info(f"Sending request to model '{model}' with provided instructions.")
    print(system,user_messages)

    result = llm(
        system_prompt=system,
        user_messages="\n".join(user_messages),
        model=model,
        api_key=api_key,
    )

    # Write the output to file or stdout
    try:
        if output == "-":
            logger.info("Writing output to stdout.")
            print(result)
        else:
            logger.info(f"Writing output to file: {output}")
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
    except Exception as e:
        logger.error(f"Error writing output: {e}")
        sys.exit(1)

    print(result)

    logger.info("Operation completed successfully.")


if __name__ == "__main__":
    main()
