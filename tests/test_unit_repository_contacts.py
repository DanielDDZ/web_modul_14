import unittest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    get_contact_by_some_info,
    get_birthday_per_week,
)

contacts = [
    Contact(
        first_name="User", second_name="Example", email="example@gmail.com",
        phone="0635624678", birthday=date.today() + timedelta(days=8), description="Some info for testing",
        user_id=1),
    Contact(
        first_name="User1", second_name="Example1", email="example1@gmail.com",
        phone="0985578900", birthday=date.today() + timedelta(days=3), description="Some info for testing",
        user_id=1),
    Contact(first_name="User2", second_name="Example2", email="example2@gmail.com",
         phone="0941251588", birthday=date.today() + timedelta(days=1), description="Some info for testing",
         user_id=1)
]


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = ContactModel(
            first_name="User",
            second_name="Example",
            email="example@gmail.com",
            phone="0987654321",
            birthday=date(year=1988, month=3, day=25),
            description="Some info for testing",
            user_id=1
        )

    async def test_get_contacts(self):
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=3, db=self.session, user=self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_contact(user_id=self.user.id, db=self.session, user=self.user)
        self.assertEqual(result, self.user)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(user_id=1, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_create_contact(self):
        result = await create_contact(body=self.body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, self.body.first_name)
        self.assertEqual(result.second_name, self.body.second_name)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.phone, self.body.phone)
        self.assertEqual(result.birthday, self.body.birthday)
        self.assertEqual(result.description, self.body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_found(self):
        body = ContactModel(
            first_name="User4",
            second_name="Example",
            email="example@gmail.com",
            phone="0671122456",
            birthday=date(year=1995, month=8, day=19),
            description="Some info for testing",
            user_id=1
        )
        self.session.query().filter().first.return_value = self.user
        result = await update_contact(user_id=self.user.id, body=body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await update_contact(user_id=self.user.id, body=self.body, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_remove_contact_found(self):
        self.session.query().filter().first.return_value = self.user
        result = await remove_contact(user_id=self.user.id, db=self.session, user=self.user)
        self.assertEqual(result, self.user)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(user_id=self.user.id, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_get_contact_by_some_info(self):
        self.session.query().filter().all.return_value = contacts
        result = await get_contact_by_some_info(some_info="example1@gmail.com", db=self.session, user=self.user)
        self.assertEqual(result, [contacts[1]])

    async def test_get_birthday_per_week(self):
        self.session.query().filter().all.return_value = contacts
        result = await get_birthday_per_week(days=5, db=self.session, user=self.user)
        self.assertEqual(result, [contacts[1], contacts[2]])


if __name__ == '__main__':
    unittest.main()
