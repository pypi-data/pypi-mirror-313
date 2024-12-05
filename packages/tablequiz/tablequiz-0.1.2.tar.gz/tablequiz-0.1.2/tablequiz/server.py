import importlib.resources

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from tablequiz.quiz import Quiz

with importlib.resources.path("tablequiz", "templates") as templates_path:
    templates = Jinja2Templates(directory=templates_path)


async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        request, "index.html", context={"quiz": request.app.state.quiz}
    )


async def slideshow(request: Request) -> Response:
    return templates.TemplateResponse(
        request, "slideshow.html", context={"quiz": request.app.state.quiz}
    )


async def quiz_round(request: Request) -> Response:
    round_number = request.path_params["round"]
    quiz = request.app.state.quiz
    quiz_round = quiz.rounds[round_number - 1]
    return templates.TemplateResponse(
        request,
        "quiz_round.html",
        context={"quiz": quiz, "round": quiz_round},
    )


async def quiz_round_answers(request: Request) -> Response:
    round_number = request.path_params["round"]
    quiz = request.app.state.quiz
    quiz_round = quiz.rounds[round_number - 1]
    return templates.TemplateResponse(
        request,
        "quiz_answers.html",
        context={"quiz": quiz, "round": quiz_round},
    )


routes: list[Route | Mount] = [
    Route("/", endpoint=index, name="index"),
    Route("/slideshow", endpoint=slideshow, name="slideshow"),
    Route(
        "/rounds/{round:int}/answers", endpoint=quiz_round_answers, name="round_answers"
    ),
    Route("/rounds/{round:int}", endpoint=quiz_round, name="round"),
    Mount("/static", StaticFiles(packages=["tablequiz"]), name="static"),
    Mount("/images", StaticFiles(directory="images", check_dir=False), name="images"),
]


def create_server(quiz: Quiz, host: str, port: int) -> uvicorn.Server:
    app = Starlette(debug=True, routes=routes)
    app.state.quiz = quiz
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="info",
    )
    return uvicorn.Server(config)
