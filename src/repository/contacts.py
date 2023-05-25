from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts.
    
    :param skip: int: Skip a certain number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user's id from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    """
    The get_contact function takes in a contact_id and returns the Contact object with that id.
    It also checks to make sure that the user is authorized to access this information.
    
    :param contact_id: int: Specify the contact id of the contact we want to get
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is logged in
    :return: A contact object
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Connect to the database
    :param user: User: Get the user id from the user object
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(first_name=body.first_name,
                      second_name=body.second_name,
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      description=body.description,
                      user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User) -> Contact | None:
    """
    The update_contact function updates a contact in the database.

    :param contact_id: int: Get the contact with that id
    :param body: ContactModel: Pass the contact model to the function
    :param db: Session: Access the database
    :param user: User: Get the user id from the token
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        contact.user_id = contact.id
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is authorized to delete a contact
    :return: The contact that was deleted or none if the contact didn't exist
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_some_info(some_info: str, db: Session, user: User) -> List[Contact]:
    """
    The get_contact_by_some_info function takes a string and returns a list of contacts that have the string in their first name, second name or email.

    :param some_info: str: Pass the information that we want to search for
    :param db: Session: Create a connection to the database
    :param user: User: Get the user id from the database
    :return: A list of contacts with the specified information
    :doc-author: Trelent
    """
    response = []
    info_by_first_name = db.query(Contact).filter(
        and_(Contact.first_name.like(f'%{some_info}%'), Contact.user_id == user.id)).all()
    if info_by_first_name:
        for n in info_by_first_name:
            response.append(n)
    info_by_second_name = db.query(Contact).filter(
        and_(Contact.second_name.like(f'%{some_info}%'), Contact.user_id == user.id)).all()
    if info_by_second_name:
        for n in info_by_second_name:
            response.append(n)
    info_by_email = db.query(Contact).filter(
        and_(Contact.email.like(f'%{some_info}%'), Contact.user_id == user.id)).all()
    if info_by_email:
        for n in info_by_email:
            response.append(n)
    return response


async def get_birthday_per_week(days: int, db: Session, user: User) -> Contact:
    """
    The get_birthday_per_week function returns a list of contacts whose birthday is within the next 7 days.

    :param days: int: Specify the number of days in which we want to get the birthdays
    :param db: Session: Access the database
    :param user: User: Get the user id of the current logged in user
    :return: A list of contacts whose birthdays are in the next 7 days
    :doc-author: Trelent
    """
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for cont in all_contacts:
        if timedelta(0) <= ((cont.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(cont)
    return response
