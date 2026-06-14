from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from .model import Post
from http import HTTPStatus
from app.posts.postDTO import PostDTO
from ..extensions import db

api = Namespace('posts', description='Post related operations')

post_model = api.model("Post", {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "title": fields.String(),
    "body": fields.String(),
    "created_at": fields.DateTime(),
})

create_post_model = api.model("CreatePost", {
    "title": fields.String(required=True),
    "body": fields.String(required=True),
})

@api.route("/")
class PostsList(Resource):
    @api.doc('get_posts')
    @api.marshal_with(post_model, as_list=True)
    def get(self):
        """ Get a list of posts
        """

        stmt = select(Post)
        posts = db.session.execute(stmt).scalars().all()

        return posts, HTTPStatus.OK


    @api.response(HTTPStatus.CREATED, 'Created post')
    @api.expect(create_post_model)
    @jwt_required()
    @api.doc(security='Bearer')
    def post(self):
        """ Creates a post
        """
        
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        postDTO = PostDTO(**data)
        post = Post(**vars(postDTO))
        post.user_id = current_user_id
        db.session.add(post)
        db.session.commit()

        return {"msg" : "Post created"}, HTTPStatus.CREATED
