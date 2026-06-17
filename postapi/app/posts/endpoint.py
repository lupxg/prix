from flask_restx import Namespace, Resource, fields
from flask import request, g
from sqlalchemy import select
from .model import Post
from http import HTTPStatus
from app.posts.postDTO import PostDTO
from ..extensions import db
from app.api.auth.utils import login_required

api = Namespace('posts', description='Post related operations')

post_model = api.model("Post", {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "title": fields.String(required=True),
    "body": fields.String(required=True),
    "created_at": fields.DateTime(),
})

trasient_post_model = api.model("Post", {
    "title": fields.String(required=True),
    "body": fields.String(required=True),
})

@api.route("/")
class Posts(Resource):
    @api.doc('get_posts')
    @api.marshal_with(post_model, as_list=True)
    def get(self):
        """ Get a list of posts
        """

        stmt = select(Post)
        posts = db.session.execute(stmt).scalars().all()

        return posts, HTTPStatus.OK
    

    @api.response(HTTPStatus.CREATED, 'Created post')
    @api.expect(trasient_post_model)
    @api.marshal_with(post_model)
    @login_required
    def post(self):
        """ Creates a posts
        """
        data = request.get_json()
        postDTO = PostDTO(**data)
        post = Post(**vars(postDTO))
        post.user_id = g.user.id
        db.session.add(post)
        db.session.commit()

        return data, HTTPStatus.CREATED
    

    @api.response(HTTPStatus.OK, 'Update post')
    @api.expect(trasient_post_model)
    @login_required
    def update(self):
        """ Update a post
        """
        pass
