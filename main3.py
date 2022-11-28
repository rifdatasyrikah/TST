import uvicorn
from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserLoginSchema, UserSchema
from jwt_handler import signJWT
from jwt_bearer import jwtBearer

posts = [
    {
        "id" : 1,
        "title" : "penguins",
        "text" : "weeee"
    }
]

users = []

app = FastAPI()

# 1 get for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"world"}

# 2 get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data" : posts}

# 3 get single post {id}
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {
            "error" : "Post with this ID does not exist!"
        }
    else:
        for post in posts:
            if post["id"] == id:
                return {"data" : post}

# 4
@app.post("/posts", dependencies =[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info":"Post Added!"
    }

# 5
@app.post("/user/signup", tags=["user"])
def signup(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            False

# 6
@app.post("/user/login", tags=["user"])
def login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid"
        }

if __name__ == '__main__':
    uvicorn.run("main3:app", host="0.0.0.0", port=8000, reload=True)