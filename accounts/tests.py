from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, override_settings
from axes.models import AccessFailureLog

class AuthFlowTests(TestCase):
    def test_register_login_me_logout(self):
        # Register
        r = self.client.post(reverse("register"), {
            "username": "alice",
            "email": "alice@example.com",
            "password": "s3cretpass!",
            "password_confirm": "s3cretpass!",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("login"))

        # Login
        r = self.client.post(reverse("login"), {
            "username": "alice",
            "password": "s3cretpass!",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("me"))

        # Access protected view
        r = self.client.get(reverse("me"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "alice")

        # Logout
        r = self.client.post(reverse("logout"))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], reverse("login"))

        # After logout, protected view redirects
        r = self.client.get(reverse("me"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("login"), r["Location"])

    def test_register_mismatched_passwords(self):
        r = self.client.post(reverse("register"), {
            "username": "bob",
            "email": "bob@example.com",
            "password": "one",
            "password_confirm": "two",
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Passwords do not match")
        self.assertFalse(User.objects.filter(username="bob").exists())

    @override_settings(AXES_FAILURE_LIMIT=2, AXES_COOLOFF_TIME=1)
    def test_login_blocked_after_failures(self):
        User.objects.create_user(username="carl", email="carl@example.com", password="rightpass")

        # First bad attempt: re-render login form
        r = self.client.post(reverse("login"), {"username": "carl", "password": "wrong"})
        self.assertEqual(r.status_code, 200)

        # Second attempt hits the limit -> blocked
        r = self.client.post(reverse("login"), {"username": "carl", "password": "wrong"})
        self.assertEqual(r.status_code, 429)  # or 403 if you keep Axes default

        # Even with correct creds, still blocked
        r = self.client.post(reverse("login"), {"username": "carl", "password": "rightpass"})
        self.assertEqual(r.status_code, 429)


