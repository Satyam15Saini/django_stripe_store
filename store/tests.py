from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Order
from unittest.mock import patch
import json

class WebhookTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', price_cents=1000)
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            total_price_cents=1000,
            status='PENDING'
        )

    @patch('stripe.Webhook.construct_event')
    def test_stripe_webhook_checkout_session_completed(self, mock_construct_event):
        # Mock the event returned by stripe.Webhook.construct_event
        class MockEvent:
            type = 'checkout.session.completed'
            class Data:
                class Object:
                    client_reference_id = str(self.order.id)
                object = Object()
            data = Data()

        mock_construct_event.return_value = MockEvent()

        # Call the webhook
        response = self.client.post(
            reverse('stripe_webhook'),
            data='{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )

        self.assertEqual(response.status_code, 200)
        
        # Verify order status changed to PAID
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'PAID')

    @patch('stripe.Webhook.construct_event')
    def test_stripe_webhook_invalid_signature(self, mock_construct_event):
        import stripe
        mock_construct_event.side_effect = stripe.error.SignatureVerificationError('Invalid sig', 'sig')

        response = self.client.post(
            reverse('stripe_webhook'),
            data='{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='invalid_signature'
        )

        self.assertEqual(response.status_code, 400)
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'PENDING')
