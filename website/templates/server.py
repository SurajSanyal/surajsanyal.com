from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from datetime import datetime

from website import config
from website.content.content import MarkdownPage, MarkdownCatalog

# FastAPI boilerplate setup which includes:
# - Creating the "app".
# - Pointing the app to the static files location for serving static content like images, fonts, JavaScript, etc.
# - Initializing the Jinja templating engine and pointing to the directory with the HTML templates.
app = FastAPI()
app.mount("/static", StaticFiles(directory="website/static"), name="static")
templates = Jinja2Templates(directory="website/templates")

# Get the current year and expose it to the Jinja templating engine.
# ALL templates will have access to this variable by using {{ year }}.
# You can even expose functions this way {{ and_use_like_this(with_parameter) }}.
templates.env.globals.update(
    year=datetime.now().year,
)


# This "@app.get" decorator tells FastAPI that:
# - This route responds to GET requests. Can be substituted for other requests like POST.
# - The response this gives is an HTML page. You can do things like JSONResponse if you were building an API endpoint.
# All routes consume a Request; this should always be the first argument to any route function.
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # This is the boilerplate way of displaying a templated webpage.
    # The HTML response takes the HTML request and the template. It can also accept a "context", more on that down below.

    response = templates.TemplateResponse(request=request, name="home.html")
    return response


@app.get("/markdown-example", response_class=HTMLResponse)
def markdown_example(request: Request):
    md = MarkdownPage("example.md")  # We use the MarkdownPage module to pull and render a Markdown file.

    # The "context" variable is a dictionary that exposes variables and
    # objects to this specific templating call. This works differently than
    # exposing variables with the Jinja global environment, which makes it available
    # to all templates everywhere.
    #
    # Here we use it to pass our Markdown content to the webpage.
    response = templates.TemplateResponse(
        request=request,
        name="markdown_example.html",
        context={
            "md": md
        }
    )
    return response


@app.get("/pages")
def markdown_catalog(request: Request):
    catalog = MarkdownCatalog()

    response = templates.TemplateResponse(
        request=request,
        name="markdown_example.html",
        context={
            "catalog": catalog
        }
    )
    return response