from . import api
from ..models import db, Post, User
from flask import request
from .apiauthhelper import basic_auth_required, token_auth_required, basic_auth, token_auth

@api.get('/posts')
def all_posts_api():
    posts = Post.query.order_by(Post.date_created.desc()).all() # list of Post Objects
    posts = [p.to_dict() for p in posts] # list of Post Dictionaries
    return {
        'status':'ok',
        'total_results': len(posts),
        'posts': posts
    }

@api.get('/posts/<post_id>')
def single_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'total_results': 1,
            'post': post.to_dict()
        }
    return {
        'status': 'not ok',
        'message': 'A post with that ID does not exist.'
    }, 404



# Everything below this in the create_post_api function is used for checking wether the post was successfully created
@api.post('/posts/create')
@token_auth_required
def create_post_api(user):
    data = request.json
    title = data['title']
    caption = data['caption']
    img_url = data['img_url']

    post = Post(title, img_url, caption, user.id)

    db.session.add(post)
    db.session.commit()

    return {
        'status': 'ok',
        'message': "Successfully created the post."
    }, 201




# Everything made below the creat_user function is meant to confirm whether the username
# an email in place is allowed and does error handling.
@api.post('/user/create')
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That username is already taken'
        };400
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email is already in use'
        };400

    user = User(username, email, password)
    
    db.session.add(user)
    db.session.commit()

    return{
        'status': 'ok',
        'message': 'Successfully created your account!'
    }; 201


@api.post('/user/login')
@basic_auth_required
def login_user(user):
    return {
        'status': 'ok',
        'user': user.to_dict(),
        'message': "Successfully logged in."
    }, 200