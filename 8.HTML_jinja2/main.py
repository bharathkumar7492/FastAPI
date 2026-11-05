from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


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

# response_class=HTMLResponse - html response
# include_in_schema=False - router works in web browser but not appear in api doc


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    # return {"message": "hello world"}
    return f"<h1>{posts[0]["movie"]}</h1>"

@app.get("/api/posts")
def get_posts():
    return posts