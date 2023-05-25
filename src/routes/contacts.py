from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/all", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Specify how many records to skip
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository
    :param current_contacts: User: Get the current contacts
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts


@router.get("/find/{some_info}", response_model=List[ContactResponse])
async def find_contact_by_some_info(some_info: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contact_by_some_info function is used to find contacts by some info.

    :param some_info: str: Pass the search string to the function
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_some_info(some_info, db, current_user)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ContactResponse])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_birthday_per_week function returns a list of contacts that have their birthday in the next 7 days.
    The function takes an integer as input, which is the number of days to look ahead for birthdays.
    It then queries the database and returns a list of contacts with their birthday in that time frame.

    :param days: int: Specify the amount of days that we want to search for birthdays
    :param db: Session: Inject the database session into the function
    :param current_user: User: Get the current user
    :return: A list of contacts with a birthday in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday_per_week(days, db, current_user)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact function is a GET endpoint that returns the contact with the given ID.
    If no such contact exists, it raises an HTTP 404 error.

    :param contact_id: int: Specify the type of the parameter
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 1 requests per 1 minute',
             dependencies=[Depends(RateLimiter(times=15, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
    It takes a СontactModel object as input, and returns an HTTP response with the newly created contacts information.


    :param body: СontactModel: Specify the type of data that will be passed to the function
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db, current_user)


@router.put("/put/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
    It takes an id, and a body containing the fields to update.
    The function returns the updated contact.

    :param body: СontactModel: Specify the data that will be passed to the function
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id of the logged in user
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
