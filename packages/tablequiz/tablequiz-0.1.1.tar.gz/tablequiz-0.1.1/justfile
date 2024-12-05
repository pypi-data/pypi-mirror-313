project := "tablequiz"
quiz := "example_quiz.yaml"

default: serve

summary quiz=quiz:
  tablequiz summary {{quiz}}

develop quiz=quiz:
  watchfiles "tablequiz serve {{quiz}}" .

serve quiz=quiz:
  tablequiz serve {{quiz}}

lint:
  ruff check
  ruff format --check
  mypy --strict {{project}}

fix:
  ruff check --fix
  ruff format

uv-sync:
  uv sync
