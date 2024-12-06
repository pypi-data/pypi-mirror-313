#!/usr/bin/env python3

import sys
import click
from tabulate import tabulate

from .lib import TokenCounter

DEFAULT_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "o1-preview",
    "o1-mini",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20241022",
    "gemini-1.5-pro-002",
    "gemini-1.5-flash-002",
    # "gemini-1.5-flash-8b",
    "llama-3.1-8b-instruct",
]


@click.command()
@click.argument("data", type=click.File("rb"), default=sys.stdin)
@click.option(
    "--model",
    "-m",
    "models",
    multiple=True,
    type=str,
    help="Models to count tokens for",
    default=DEFAULT_MODELS,
)
@click.option(
    "--provider",
    "-p",
    type=str,
    help="Provider to use for the model",
    default="perplexity",
)
def main(data: click.File, models: tuple[str], provider: str):
    """Count tokens and estimate costs across different LLM models"""

    counter = TokenCounter(data.read())
    stats = []
    for model in models:
        try:
            stats.append(counter.for_model(model, provider))
        except Exception as e:
            click.echo(f"Error processing {model}: {e}", err=True)

    click.echo(
        tabulate(stats, headers="keys", tablefmt="simple", floatfmt=".4f", intfmt=",")
    )


if __name__ == "__main__":
    main()
