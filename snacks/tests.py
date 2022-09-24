from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Snack
from django.urls import reverse

# Create your tests here.
class SnacksTests(TestCase):
    # Create test user
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@email.com",
            password="password1"
        )
    
        self.snack = Snack.objects.create(
            title = "Chips",
            purchaser = self.user,
            description = "Nacho cheese inspired tortilla chips."
        )

    def test_model_string_representation(self):
        self.assertEqual(str(self.snack), "Chips")

    def test_model_content(self):
        self.assertEqual(self.snack.title, "Chips")
        self.assertEqual(str(self.snack.purchaser), "test")
        self.assertEqual(self.snack.description, "Nacho cheese inspired tortilla chips.")

    def test_snack_list_view(self):
        response = self.client.get(reverse('snack_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chips")
        self.assertTemplateUsed(response, "snack_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse('snack_detail', args='1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nacho cheese inspired tortilla chips.")
        self.assertTemplateUsed(response, "snack_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse('snack_create'),
            {
                "title": "Soylent",
                "purchaser": self.user.id,
                "description": "Apparently its a book reference."
            },
            follow=True
        )
    
        self.assertRedirects(response, reverse('snack_detail', args='2'))
        self.assertContains(response, "Apparently its a book reference.")
        self.assertTemplateUsed(response, "snack_detail.html")
    
    def test_snack_update_view(self):
        response = self.client.post(
            reverse("snack_update", args='1'),
            {
                "title": "Chips Updated",
                "purchaser": self.user.id,
                "description": "I like Chips."
            },
            follow=True
        )

        self.assertRedirects(response, reverse('snack_detail', args='1'))

    def test_snack_delete_view(self):
        response = self.client.get(reverse('snack_delete', args='1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack_delete.html')

        response = self.client.post(reverse('snack_delete', args='1'), follow=True)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertNotContains(response, 'Chips')