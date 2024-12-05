"""Quiz data structures"""

from dataclasses import dataclass


@dataclass
class Source:
    url: str
    title: str | None = None
    description: str | None = None


@dataclass
class Image:
    url: str


@dataclass
class Answer:
    answer: str
    image: Image | None = None


@dataclass
class Choice:
    choice: str
    image: Image | None = None


@dataclass
class Question:
    question: str
    image: Image | None = None


@dataclass
class SingleChoiceQuestion:
    type = "single_choice"
    question: Question
    answer: Answer
    sources: list[Source]
    tags: list[str]
    notes: str | None = None
    hint: str | None = None


@dataclass
class MultipleChoiceQuestion:
    type = "multiple_choice"
    question: Question
    answer: Answer
    choices: list[Choice]
    sources: list[Source]
    tags: list[str]
    notes: str | None = None
    hint: str | None = None


@dataclass
class Round:
    title: str
    questions: list[MultipleChoiceQuestion | SingleChoiceQuestion]
    sub_title: str | None = None


@dataclass
class Quiz:
    title: str
    rounds: list[Round]
    sub_title: str | None = None
    slideshow: str | None = None
