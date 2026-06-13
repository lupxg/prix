from flask_restx import Namespace, Resource, fields
from flask import request
from sqlalchemy import select
from .model import Post
from http import HTTPStatus
from app.posts.postDTO import PostDTO
from ..extensions import db
from app.utils import token_required

api = Namespace('posts', description='Post related operations')

post_model = api.model("Post", {
    "id": fields.Integer,
    "title": fields.String,
    "body": fields.String,
    "created_at": fields.DateTime,
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
    @api.expect(post_model)
    @token_required
    @api.doc(security='Bearer')
    def post(self, current_user):
        """ Creates a post
        """

        user_post = request.get_json()
        postDTO = PostDTO(**user_post)
        post = Post(**vars(postDTO))
        db.session.add(post)
        db.session.commit()

        return request.json, HTTPStatus.CREATED
