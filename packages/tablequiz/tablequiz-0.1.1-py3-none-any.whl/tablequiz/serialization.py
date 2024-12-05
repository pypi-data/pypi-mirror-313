"""Reads quizes from files"""

from pathlib import Path
from typing import Optional
import string

import yaml
from pydantic import BaseModel, HttpUrl
from . import quiz as quiz_dataclasses


class Source(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None

    def to_dataclass(self) -> quiz_dataclasses.Source:
        return quiz_dataclasses.Source(
            description=self.description, url=str(self.url), title=self.title
        )


class Answer(BaseModel):
    answer: str
    image: Optional[str] = None

    def to_dataclass(self) -> quiz_dataclasses.Answer:
        return quiz_dataclasses.Answer(
            answer=self.answer,
            image=quiz_dataclasses.Image(url=self.image)
            if self.image is not None
            else None,
        )


class Question(BaseModel):
    question: str
    image: Optional[str] = None

    def to_dataclass(self) -> quiz_dataclasses.Question:
        return quiz_dataclasses.Question(
            question=self.question,
            image=quiz_dataclasses.Image(url=self.image)
            if self.image is not None
            else None,
        )


class SingleChoiceQuestion(BaseModel):
    question: str | Question
    answer: str | Answer
    source: Optional[str | Source] = None
    sources: Optional[list[str | Source]] = None
    tag: Optional[str] = None
    tags: Optional[list[str]] = None
    notes: str | None = None
    hint: str | None = None

    def to_dataclass(self) -> quiz_dataclasses.SingleChoiceQuestion:
        sources: list[str | Source] = [] if self.sources is None else self.sources
        if self.source:
            sources.append(self.source)
        tags = self.tags if self.tags is not None else []
        if self.tag:
            tags.append(self.tag)
        return quiz_dataclasses.SingleChoiceQuestion(
            answer=quiz_dataclasses.Answer(answer=self.answer)
            if isinstance(self.answer, str)
            else self.answer.to_dataclass(),
            question=quiz_dataclasses.Question(question=self.question)
            if isinstance(self.question, str)
            else self.question.to_dataclass(),
            sources=[
                quiz_dataclasses.Source(url=s)
                if isinstance(s, str)
                else s.to_dataclass()
                for s in sources
            ],
            tags=tags,
            notes=self.notes,
            hint=self.hint,
        )


class MultipleChoiceQuestion(BaseModel):
    question: str | Question
    choices: list[str | Answer]
    source: Optional[str | Source] = None
    sources: Optional[list[str | Source]] = None
    tag: Optional[str] = None
    tags: Optional[list[str]] = None
    notes: str | None = None
    hint: str | None = None

    def to_dataclass(self) -> quiz_dataclasses.MultipleChoiceQuestion:
        sources: list[str | Source] = [] if self.sources is None else self.sources
        if self.source:
            sources.append(self.source)
        tags = self.tags if self.tags is not None else []
        if self.tag:
            tags.append(self.tag)
        answers = [
            (i, a) for (i, a) in enumerate(self.choices) if isinstance(a, Answer)
        ]
        assert len(answers) == 1
        i, answer = answers[0]
        letter = string.ascii_lowercase[i]
        answer = answer.to_dataclass()
        answer.answer = f"{letter}. {answer.answer}"
        return quiz_dataclasses.MultipleChoiceQuestion(
            question=quiz_dataclasses.Question(question=self.question)
            if isinstance(self.question, str)
            else self.question.to_dataclass(),
            sources=[
                quiz_dataclasses.Source(url=s)
                if isinstance(s, str)
                else s.to_dataclass()
                for s in sources
            ],
            choices=[
                quiz_dataclasses.Choice(choice=a if isinstance(a, str) else a.answer)
                for a in self.choices
            ],
            answer=answer,
            tags=tags,
            notes=self.notes,
            hint=self.hint,
        )


class Round(BaseModel):
    title: str
    sub_title: Optional[str] = None
    questions: list[MultipleChoiceQuestion | SingleChoiceQuestion]

    def to_dataclass(self) -> quiz_dataclasses.Round:
        return quiz_dataclasses.Round(
            title=self.title,
            sub_title=self.sub_title,
            questions=[q.to_dataclass() for q in self.questions],
        )


class Quiz(BaseModel):
    title: str
    sub_title: Optional[str] = None
    rounds: list[Round]
    slideshow: Optional[str] = None

    def to_dataclass(self) -> quiz_dataclasses.Quiz:
        return quiz_dataclasses.Quiz(
            title=self.title,
            sub_title=self.sub_title,
            rounds=[r.to_dataclass() for r in self.rounds],
            slideshow=self.slideshow,
        )


def parse_file(filename: Path) -> quiz_dataclasses.Quiz:
    with filename.open("r") as fp:
        raw = yaml.safe_load(fp)
    quiz = Quiz.model_validate(raw)

    return quiz.to_dataclass()
