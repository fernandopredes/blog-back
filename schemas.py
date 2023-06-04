from marshmallow import Schema, fields

class UserSchema(Schema):
    """
    Define como deve ser a estrutura do dado após criação de um novo usuário.
    """
    id = fields.Int(dump_only=True, description="id do usuário")
    name = fields.Str(required=True, description="nome do usuário")
    password = fields.Str(required=True, load_only=True, description="password do usuário")
    email = fields.Email(required=True, description="e-mail do usuário")
    ship_name = fields.Str(required=True, description="nome da embarcação do usuário")
    

    class Meta:
        description = "Define como um novo usuário a ser inserido deve ser representado"

class UserLoginSchema(Schema):
    """
    Define como deve ser a estrutura para realizar o login de um usuário.
    """
    email = fields.Email(required=True, description="e-mail do usuário")
    password = fields.Str(required=True, load_only=True, description="password do usuário")

    class Meta:
        description = "Define como um login de usuário deve ser representado"

class CreateUserSchema(Schema):
    """
    Define como deve ser a estrutura do dado após criação de usuário.
    """
    message = fields.String(description="Mensagem de usuário criado")

    class Meta:
        description = "Esquema de mensagem após a criação de usuário."

class UserTokenSchema(Schema):
    """
    Define como deve ser a estrutura do dado após um login.
    """
    access_token = fields.String(description="Token de acesso")
    user_id = fields.Int(description="Id do usuário")

    class Meta:
        description = "Esquema para resposta da rota de login do usuário"
