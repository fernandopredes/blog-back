from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import PostModel
from schemas import PostSchema, UpdatePostSchema, DeletePostSchema

blp = Blueprint("Posts", __name__, description="Operations with Posts")

@blp.route('/posts')
class PostList(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema(many=True), description="Success. Returns the list of all posts.")
    def get(self):
        """Pega todos os posts"""
        posts = PostModel.query.all()
        post_schema = PostSchema(many=True)
        return post_schema.dump(posts)

    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema, description="Success. Returns the created post.")
    def post(self, post_data):
        """Cria um novo post"""
        user_id = get_jwt_identity()
        post_data['user_id'] = user_id

        post = PostModel(**post_data)
        try:
            db.session.add(post)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            abort(500, message="An error occurred while trying to create a Post.")

        return post

@blp.route('/posts/<int:post_id>')
class Post(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema, description="Success. Returns the post with the given id.")
    def get(self, post_id):
        """Pega um único post"""
        post = PostModel.query.get_or_404(post_id)
        return post

    @jwt_required()
    @blp.arguments(UpdatePostSchema)
    @blp.response(200, PostSchema, description="Success. Returns the updated post.")
    def put(self, post_data, post_id):
        """Update de um post"""
        post = PostModel.query.get(post_id)
        if post:
            for key, value in post_data.items():
                setattr(post, key, value)
        else:
            post = PostModel(id=post_id, **post_data)

        db.session.add(post)
        db.session.commit()

        return post

    @jwt_required()
    @blp.response(200, DeletePostSchema, description="Success. Returns a success message and the deleted post.")
    @blp.response(404, description="The id was not found.")
    def delete(self, post_id):
        """Deleta um post"""
        post = PostModel.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message":"Post deleted"}, 200
