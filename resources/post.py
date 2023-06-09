from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from cloudinary.uploader import upload
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

@blp.route('/create_post', methods=['POST'])
class PostCreation(MethodView):
    @jwt_required()
    @blp.arguments(PostSchema)  # Validation of data
    @blp.response(200, PostSchema, description="Success. Returns a message confirming the post has been created.")
    def post(self, post_data):
        """ Rota para criar um post.

        Retorna uma mensagem confirmando que o post foi criado.

        """
        # pega o usuário atual
        current_user_id = get_jwt_identity()

        # Extrai dados do post_data
        title = post_data['title']
        abstract = post_data['abstract']
        text = post_data['text']

        image_one_url = None
        image_two_url = None

        # Check da image_one
        if 'image_one' in request.files and request.files['image_one'].filename != '':
            image_one = request.files['image_one']
            res_one = upload(image_one)
            image_one_url = res_one['secure_url']

        # Check da image_two
        if 'image_two' in request.files and request.files['image_two'].filename != '':
            image_two = request.files['image_two']
            res_two = upload(image_two)
            image_two_url = res_two['secure_url']

        try:
            # Cria um novo post com as imagens
            new_post = PostModel(
                user_id=current_user_id,
                title=title,
                abstract=abstract,
                text=text,
                image_one=image_one_url,
                image_two=image_two_url
            )

            db.session.add(new_post)
            db.session.commit()  # commit mudanças no database

            return {"message": "Post created successfully."}

        except Exception as e:
            abort(500, message=str(e))


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
