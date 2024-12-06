from django.contrib.auth.models import User
from django.test import TestCase

from secretsanta.models import Application, SantaPair, Year
from secretsanta.tasks import (
    generate_pairs, notify_outstanding_santees, notify_santas,
)


class TestTasks(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        self.user4 = User.objects.create_user(username='user4', password='password')
        self.user5 = User.objects.create_user(username='user5', password='password')
        self.user6 = User.objects.create_user(username='user6', password='password')
        self.user7 = User.objects.create_user(username='user7', password='password')
        self.user8 = User.objects.create_user(username='user8', password='password')
        self.user9 = User.objects.create_user(username='user9', password='password')
        self.user10 = User.objects.create_user(username='user10', password='password')

        self.year1 = Year.objects.create(year=2023, open=True)

    def test_generate_pairs(self):
        year = self.year1
        Application.objects.create(year=year, user=self.user1)
        Application.objects.create(year=year, user=self.user2)
        Application.objects.create(year=year, user=self.user3)
        Application.objects.create(year=year, user=self.user4)
        Application.objects.create(year=year, user=self.user5)
        Application.objects.create(year=year, user=self.user6)
        Application.objects.create(year=year, user=self.user7)
        Application.objects.create(year=year, user=self.user8)
        Application.objects.create(year=year, user=self.user9)
        Application.objects.create(year=year, user=self.user10)
        generate_pairs(year.year)
        self.assertEqual(SantaPair.objects.count(), 10)

    def test_notify_santas(self):
        year = self.year1
        SantaPair.objects.create(year=year, santa=self.user1, santee=self.user2)
        notify_santas(year.year)
        # Here you can check if the message was sent correctly

    def test_notify_outstanding_santees(self):
        year = self.year1
        SantaPair.objects.create(year=year, santa=self.user1, santee=self.user2, delivered=False)
        notify_outstanding_santees(year.year)
        # Here you can check if the message was sent correctly
