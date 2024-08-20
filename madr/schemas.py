from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list


class LivroSchema(BaseModel):
    ano: int
    titulo: str
    romancista_id: int


class LivroPublic(LivroSchema):
    id: int


class LivroUpdate(BaseModel):
    ano: int | None = None
    titulo: str | None = None
    romancista_id: int | None = None


class LivroList(BaseModel):
    livros: list
