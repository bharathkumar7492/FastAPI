from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
# StaticFiles – Helps FastAPI serve files such as CSS, JavaScript, images, etc


app = FastAPI()

# app.mount()=Connects a folder to your FastAPI application, "/static"= URL path used to access static files
# StaticFiles()=	Serves static files, (directory="static")= Folder containing CSS, JS and images
# name="static"= Name given to this mounted application
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]



# name="" - These names are mainly useful for URL generation using 'request.url_for()'.
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts",include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"})
    

@app.get("/api/posts")
def get_posts():
    return posts