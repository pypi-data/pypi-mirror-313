import asyncio
import asyncio.exceptions
import collections
from pathlib import Path
import signal

import rich
import typer

from tablequiz import serialization, server

app = typer.Typer()


@app.command()
def parse(input: Path) -> None:
    quiz = serialization.parse_file(input)
    rich.print(quiz)


@app.command()
def serve(input: Path, host: str = "127.0.0.1", port: int = 5000) -> None:
    quiz = serialization.parse_file(input)
    srv = server.create_server(host=host, port=port, quiz=quiz)
    loop = asyncio.get_event_loop()

    # Try to exit a little more gracefully when run from watchfiles. Quietens
    # down one exception but there's still a asyncio.exceptions.CancelledError
    # from the lifespan loop. It's not important, but really bugs me :D. See
    # https://github.com/encode/uvicorn/issues/2173
    def signal_handler() -> None:
        srv.should_exit = True

    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    asyncio.run(srv.serve())


def print_summary(totals: collections.Counter) -> None:
    rich.print(f"Questions: {totals['questions']}")
    rich.print(f"  Images: {totals['images']}")
    rich.print(f"  Multiple choice: {totals['multiple_choice']}")
    rich.print(f"  Single choice: {totals['single_choice']}")
    rich.print(
        f"  ratio single to multiple: {totals['single_choice'] / max(totals['multiple_choice'], 1)}"
    )
    tags = [
        (tag.split(":", 1)[1], count)
        for (tag, count) in totals.most_common()
        if tag.startswith("tag:")
    ]

    rich.print("Tags:")
    for tag, count in tags:
        rich.print(f"  {tag}: {count}")


@app.command()
def summary(input: Path) -> None:
    quiz = serialization.parse_file(input)

    rich.print(quiz.title)
    rich.print(quiz.sub_title)

    totals = collections.Counter()
    for i, round in enumerate(quiz.rounds):
        rich.print(f"\nRound {i+1}: {round.title}")
        rich.print(round.sub_title)
        round_totals = collections.Counter()
        for question in round.questions:
            round_totals["questions"] += 1
            round_totals[question.type] += 1
            round_totals["images"] += (
                1 if (question.question.image or question.answer.image) else 0
            )
            for tag in question.tags:
                round_totals[f"tag:{tag}"] += 1
            if not question.tags:
                round_totals["tag:no-tag"] += 1

        print_summary(round_totals)
        totals.update(round_totals)

    rich.print("\nQuiz totals:")

    print_summary(totals)


if __name__ == "__main__":
    typer.run(app)
