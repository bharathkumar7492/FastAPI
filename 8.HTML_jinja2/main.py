from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()


templates = Jinja2Templates(directory="templates")



posts: list[dict] = [
    {
    "id": 1, 
    "movie": "Avengers End Game",
    "hero": "Iron Man", 
    "power": "Super Suit",
    "date_posted": "Nov 05, 2026"
    },
    {
    "id": 1, 
    "movie": "Avengers: Civil War",
    "hero": "Captain America", 
    "power": "Super Serum",
    "date_posted": "Nov 06, 2026"
    }
]




@app.get("/", include_in_schema=False)
@app.get("/posts",include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"})
    

@app.get("/api/posts")
def get_posts():
    return posts