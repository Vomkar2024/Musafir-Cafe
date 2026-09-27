from django.test import TestCase, Client
from django.urls import reverse
from main.models import Order, MenuItem, Contact


class MusafirCafeAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.item = MenuItem.objects.create(
            name="Cold Coffee",
            price=120.00,
            category="drink",
            is_available=True
        )
        self.order = Order.objects.create(
            customer_name="Test Customer",
            customer_phone="9876543210",
            status="placed",
            estimated_wait_minutes=15
        )

    def test_pages_render_status_200(self):
        """Test home, menu, about, services, contact, place_order render fine"""
        for url_name in ['main', 'menu', 'about', 'services', 'contact', 'place_order', 'order_tracking_home']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_menu_category_filter(self):
        """Test menu page category filter query parameter"""
        response = self.client.get(reverse('menu') + '?category=drink')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cold Coffee")

    def test_contact_form_submission(self):
        """Test POST request to contact page creates Contact record"""
        response = self.client.post(reverse('contact'), {
            'name': 'Aarav Patel',
            'email': 'aarav@example.com',
            'phone': '9876543210',
            'message': 'Great cafe experience!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(email='aarav@example.com').exists())

    def test_token_generation(self):
        """Test that every order gets a unique token like A101, A102"""
        self.assertTrue(self.order.token_number.startswith('A'))
        expected_token = f"A{100 + self.order.id}"
        self.assertEqual(self.order.token_number, expected_token)

    def test_status_workflow(self):
        """Test staff status transitions PLACED -> CONFIRMED -> PREPARING -> READY -> COMPLETED"""
        order = self.order
        self.assertEqual(order.status, 'placed')

        # Placed -> Confirmed
        self.client.post(reverse('update_order_status', kwargs={'token': order.token_number}), {
            'status': 'confirmed',
            'estimated_wait_minutes': '15'
        })
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

        # Confirmed -> Preparing
        self.client.post(reverse('update_order_status', kwargs={'token': order.token_number}), {
            'status': 'preparing',
            'estimated_wait_minutes': '10'
        })
        order.refresh_from_db()
        self.assertEqual(order.status, 'preparing')
        self.assertEqual(order.estimated_wait_display, '10 minutes')

        # Preparing -> Ready
        self.client.post(reverse('update_order_status', kwargs={'token': order.token_number}), {
            'status': 'ready',
            'estimated_wait_minutes': '0'
        })
        order.refresh_from_db()
        self.assertEqual(order.status, 'ready')
        self.assertEqual(order.estimated_wait_display, 'Ready Now!')

        # Ready -> Completed
        self.client.post(reverse('update_order_status', kwargs={'token': order.token_number}), {
            'status': 'completed'
        })
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')

    def test_customer_order_tracking_html(self):
        """Test customer tracking ticket page (/order/<token>/)"""
        url = reverse('order_tracking', kwargs={'token': self.order.token_number})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.token_number)
        self.assertContains(response, "MUSAFIR CAFE")

    def test_customer_order_tracking_json_api(self):
        """Test AJAX auto-polling JSON response"""
        url = reverse('order_tracking', kwargs={'token': self.order.token_number}) + "?format=json"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['token_number'], self.order.token_number)
        self.assertEqual(data['status'], 'placed')

    def test_kitchen_dashboard_view(self):
        """Test kitchen dashboard renders queue"""
        url = reverse('kitchen_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.token_number)
