import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


posts = {
        0 : {
            "id": 0,
            "upvotes": 1,
            "title": "My cat is the cutest",
            "link": "https://facebook.com",
            "username": "jnt1"
        },
        1 : {
            "id": 1,
            "upvotes": 3,
            "title": "Cat loaf",
            "link": "https://amazon.com",
            "username": "jnt2"
        }
}
posts_id_counter = 2


comments = {
        0 :  
        { 
            0: {
            "id": 0,
            "upvotes": 1,
            "text": "Nice cat",
            "username": "jnt1"
             }
        },
        1 : {

        }
}
comment_id_counter = 1

#Get all posts
@app.route("/")
@app.route("/api/posts/")
def get_posts():
    result = {
        "success": True,
        "data": list(posts.values())
    }
    return json.dumps(result), 200


#Create post
@app.route("/api/posts/", methods = ["POST"])
def create_post():
    global posts_id_counter #lets you change global variable directly
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if not (title and link and username):
        return json.dumps({"success": False, "error": "Cannot create post"}), 404
    post = {
        "id": posts_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username
    }
    posts[posts_id_counter] = post
    result = {
        "success": True,
        "data": post
    }
    comments[posts_id_counter] = {}
    posts_id_counter += 1
    return json.dumps(result), 201


#Get a post
@app.route("/api/posts/<int:post_id>/")
def get_specific_post(post_id):
    post = posts.get(post_id)
    if post:
        return json.dumps({"success": True, "data": post}), 200
    return json.dumps({"success": False, "error": "That post does not exist"}), 404


#Delete a post
@app.route("/api/posts/<int:post_id>/", methods = ["DELETE"])
def delete_post(post_id):
    post = posts.get(post_id)
    if post:
        del posts[post_id]
        del comments[post_id]
        return json.dumps({"success": True, "data": post})
    return json.dumps({"success": False, "error": "That post does not exist"}), 404
 

#Get comments for a specific post
@app.route("/api/posts/<int:post_id>/comments/")
def get_comments(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"success": False, "error": "That post does not exist"}), 404
    data = comments.get(post_id)
    if not data:
        return json.dumps({"success": False, "error": "That comment does not exist"}), 404
    return json.dumps({"success": True, "data": list(data.values())}), 200


#Post a comment for a specific post
@app.route("/api/posts/<int:post_id>/comments/", methods = ["POST"])
def post_comment(post_id):
    global comment_id_counter
    post = posts.get(post_id)
    if not post:
        return json.dumps({"success": False, "error": "That post does not exist"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")
    if not (text and username):
        return json.dumps({"success": False, "error": "Cannot post comment"}), 404
    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username
    }
    comments[post_id][comment_id_counter] = comment
    comment_id_counter += 1
    return json.dumps({"success": True, "data": comment}), 200


#Edit a comment comment for a specific post
@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods = ["POST"])
def edit_comment(post_id, comment_id):
    if not posts.get(post_id):
        return json.dumps({"success": False, "error": "That post does not exist"}), 404
    comment = comments[post_id].get(comment_id)
    if not comment:
        return json.dumps({"success": False, "error": "That comment does not exist"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    if not text:
        return json.dumps({"success": False, "error": "Cannot update comment"}), 404
    comment["text"] = text
    return json.dumps({"success": True, "data": comment}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
