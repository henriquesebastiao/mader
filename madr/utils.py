from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.security import get_current_user

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


def sanitize(text: str) -> str:
    text = text.lower().strip().split()
    return ' '.join(text)
