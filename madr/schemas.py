from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr

sanitized = Annotated[
    str, AfterValidator(lambda x: ' '.join(str(x).split()).lower())
]


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: sanitized
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: sanitized
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RomancistaSchema(BaseModel):
    nome: sanitized


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list


class LivroSchema(BaseModel):
    ano: int
    titulo: sanitized
    romancista_id: int


class LivroPublic(LivroSchema):
    id: int


class LivroUpdate(BaseModel):
    ano: int | None = None
    titulo: str | None = None
    romancista_id: int | None = None


class LivroList(BaseModel):
    livros: list
