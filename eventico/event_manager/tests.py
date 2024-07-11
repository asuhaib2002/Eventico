# from datetime import datetime
from django.utils.timezone import now
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from event_manager.models import Event
from django.contrib.auth import get_user_model
from django.urls import get_resolver
from rest_framework.authtoken.models import Token

User = get_user_model()

class EventTests(APITestCase):
    def setUp(self):
        owner = User.objects.create_user(username='owner_account', email='suhaib@owner.com',password='testpass')
        self.user = owner
        self.client.login(username='owner_account', password='testpass')
        self.attendee1 = User.objects.create_user(username='atendee1', password='testpass')
        self.attendee2 = User.objects.create_user(username='atendee2', password='testpass')
        self.event_url = reverse('api:event-list')

    def test_create_event(self):
        url = reverse('api:event-list')
        data = {'title': 'New Event', 'description': 'This is a new event', 'date': '2024-07-09T00:00:00Z', 'location': 'New Location'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_events(self):
        url = reverse('api:event-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Rewriting was required
    def test_update_event(self):
        url = reverse('api:event-list')
        data = {'title': 'New Event', 'description': 'This is a new event', 'date': '2024-07-09T00:00:00Z', 'location': 'New Location'}
        response = self.client.post(url, data, format='json')
        event = Event.objects.first()
        url = reverse('api:event-detail', kwargs={'pk': event.id})
        data = {'title': 'Updated Event', 'description': 'This is an updated event', 'date': '2024-07-10T00:00:00Z', 'location': 'Updated Location'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Event')

    def test_delete_event(self):
        url = reverse('api:event-list')
        data = {'title': 'New Event', 'description': 'This is a new event', 'date': '2024-07-09T00:00:00Z', 'location': 'New Location'}
        response = self.client.post(url, data, format='json')
        event = Event.objects.first()
        url = reverse('api:event-detail', kwargs={'pk': event.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    def test_attend_event(self):
        url = reverse('api:event-list')
        data = {'title': 'New Event', 'description': 'This is a new event', 'date': '2024-07-09T00:00:00Z', 'location': 'New Location'}
        response = self.client.post(url, data, format='json')
        event = Event.objects.first()
        attend_url = reverse('api:event-attend', args=[event.id])
        response = self.client.post(attend_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, event.attendees.all())

    def test_already_attending_event(self):
        url = reverse('api:event-list')
        data = {'title': 'New Event', 'description': 'This is a new event', 'date': '2024-07-09T00:00:00Z', 'location': 'New Location'}
        response = self.client.post(url, data, format='json')
        event = Event.objects.first()
        event.attendees.add(self.user)
        attend_url = reverse('api:event-attend', args=[event.id])
        response = self.client.post(attend_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You are already attending this event.')
