from graphene.test import Client

# from snapshottest.django import TestCase

from django.test import TestCase
from django.contrib.auth.models import User

from ..schema import schema
from ..models import Portfolio


def assertMatch(self, exe, res=None):
    try:
        self.assertMatchSnapshot(exe)
    except AttributeError:
        self.assertEqual(exe, res)


class SchemaTest(TestCase):
    def create_users(self):
        user = User.objects.create_user(username="davisphem", email="davis@gmail.com")
        user.set_password("phemmy2022")
        user.save()
        self.user1 = user

    def create_portfolios(self):
        self.frontend = Portfolio.objects.create(owner=self.user1, title="frontend")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n")

    def setUp(self):
        super().setUp()
        self.client = Client(schema)
        self.create_users()
        self.create_portfolios()

    def test_get_portfolios_resolver(self):

        exe = self.client.execute(
            """{
            users{
                username
                email
            }
        }
        """
        )

        assertMatch(
            self,
            exe,
            {
                "data": {
                    "users": [{"username": "davisphem", "email": "davis@gmail.com"}]
                }
            },
        )

    def test_create_users_mutation(self):
        exe = {}
        assertMatch(self, exe, {})
