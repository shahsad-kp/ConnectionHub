from django.test import TestCase
from django.urls import reverse

from MainUsers.models import User


class LoginedTest(TestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
        )
        self.client.login(
            username=self.username,
            password=self.password,
        )
        self.post = self.user.posts.create(
            image='test.jpg',
            caption='test',
        )


class AdminPostPageTest(LoginedTest):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            viewname='admin-posts-page',
            args=[
                self.post.id,
            ]
        )

    def test_get_post_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_post_page.html')

    def test_invalid_post_id(self):
        url = reverse(
            viewname='admin-posts-page',
            args=[
                999,
            ]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AdminPostDeleteTest(LoginedTest):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            viewname='admin-posts-delete',
            args=[
                self.post.id,
            ]
        )

    def test_delete_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.user.posts.count(), 0)

    def test_invalid_post_id(self):
        url = reverse(
            viewname='admin-posts-delete',
            args=[
                999,
            ]
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class AdminCommentDeleteTest(LoginedTest):
    def setUp(self):
        super().setUp()
        self.comment = self.post.comments.create(
            user=self.user,
            content='test',
        )
        self.url = reverse(
            viewname='admin-comments-delete',
            args=[
                self.comment.id,
            ]
        )

    def test_delete_comment(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(self.post.comments.count(), 0)

    def test_invalid_comment_id(self):
        url = reverse(
            viewname='admin-comments-delete',
            args=[
                999,
            ]
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
