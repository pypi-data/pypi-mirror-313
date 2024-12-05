from contextlib import ContextDecorator
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from chef.settings import settings

engine = create_engine(settings.database_uri, echo=True)


class MyContext(ContextDecorator):

    session: Union[Session, None]

    def __init__(self) -> None:
        self.session = None

    def __enter__(self):
        print('in enter')
        self.session = Session(engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('in exit')
        self.session.close()


def get_session():
    return MyContext()
