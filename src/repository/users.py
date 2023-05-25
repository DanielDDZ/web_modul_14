from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

from libgravatar import Gravatar


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the User object associated with that email. If no such user exists,
    it returns None.

    :param email: str: Filter the database for a user with that email
    :param db: Session: Pass the database session to the function
    :return: An user object
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
    It takes an UserModel object and a Session object as arguments, and returns an User object.
    The function first tries to get the Gravatar image for the email address provided in the body of
    the request, but if it fails it will just set avatar to None. It then uses **body.dict() to unpack
    the dictionary returned by body's dict method into keyword arguments that are passed into creating
    a new instance of User (which is what we want). The function then adds this new user instance
    to our database session, commits

    :param body: UserModel: Pass the data from the request body to the function
    :param db: Session: Access the database
    :return: A new user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_contact = User(**body.dict(), avatar=avatar)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_token(contact: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Specify the type of token
    :param db: Session: Commit the changes to the database
    :return: None
    :doc-author: Trelent
    """
    contact.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes an email and a database session as arguments.
    It then gets the user from the database using their email address, sets their confirmed field to True,
    and commits that change to the database.

    :param email: str: Get the email of the user
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function takes an email and a url as arguments.
    It then uses the get_user_by_email function to retrieve the user from the database.
    The avatar property of that user is set to be equal to the url argument, and then
    the db session is committed.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is going to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: The updated user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
