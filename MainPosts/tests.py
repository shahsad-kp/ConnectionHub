from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from MainPosts.models import Post, Reaction, SavedPost
from MainUsers.models import User


class DetailPageTest(TestCase):
    def setUp(self) -> None:
        self.post_id = 1
        self.url = reverse(
            viewname='post-detail',
            args=[self.post_id]
        )
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_valid_post(self):
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post-detail.html')

    def test_invalid_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class PostLikeTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.url = reverse(
            viewname='like-post',
            args=[self.post_one.id]
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_invalid_post(self):
        response = self.client.get(
            reverse(
                viewname='like-post',
                args=[999]
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 1)
        self.assertEqual(response.json()['dislikes'], 0)
        self.assertEqual(response.json()['liked'], True)

    def test_already_liked_post(self):
        Reaction.objects.create(
            user=self.user,
            post=self.post_one,
            reaction='like'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 0)
        self.assertEqual(response.json()['liked'], False)

    def test_already_disliked_post(self):
        Reaction.objects.create(
            user=self.user,
            post=self.post_one,
            reaction='dislike'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 1)
        self.assertEqual(response.json()['dislikes'], 0)
        self.assertEqual(response.json()['liked'], True)


class PostDislikeTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.url = reverse(
            viewname='dislike-post',
            args=[self.post_one.id]
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_invalid_post(self):
        response = self.client.get(
            reverse(
                viewname='dislike-post',
                args=[999]
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 1)
        self.assertEqual(response.json()['liked'], False)
        self.assertEqual(response.json()['disliked'], True)

    def test_already_liked_post(self):
        Reaction.objects.create(
            user=self.user,
            post=self.post_one,
            reaction='like'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 1)
        self.assertEqual(response.json()['liked'], False)
        self.assertEqual(response.json()['disliked'], True)

    def test_already_disliked_post(self):
        Reaction.objects.create(
            user=self.user,
            post=self.post_one,
            reaction='dislike'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 0)
        self.assertEqual(response.json()['liked'], False)
        self.assertEqual(response.json()['disliked'], False)


class SavePostTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.url = reverse(
            viewname='save-post',
            args=[self.post_one.id]
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_invalid_post(self):
        response = self.client.get(
            reverse(
                viewname='save-post',
                args=[999]
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['saved'], True)

    def test_already_saved_post(self):
        SavedPost.objects.create(
            user=self.user,
            post=self.post_one
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['saved'], False)


class ViewCommentsTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.url = reverse(
            viewname='view-comment',
            args=[self.post_one.id]
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_invalid_post(self):
        response = self.client.get(
            reverse(
                viewname='view-comment',
                args=[999]
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = {
            'success': True,
            'comments': [],
        }
        data = response.json()
        self.assertDictEqual(data, expected)


class AddCommentTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.url = reverse(
            viewname='add-comment',
            args=[self.post_one.id]
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_invalid_post(self):
        response = self.client.post(
            reverse(
                viewname='add-comment',
                args=[999]
            ),
            data={
                'comment': 'test comment'
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_post(self):
        response = self.client.post(
            self.url,
            data={
                'comment': 'test comment'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['comments'][0]['user']['username'], 'testuser')

    def test_empty_comment(self):
        response = self.client.post(
            self.url,
            data={
                'comment': ''
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        expected_data = {
            'success': False,
            'error': 'Comment is required'
        }
        self.assertDictEqual(data, expected_data)


class SavedPostsTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.post_one = Post.objects.create(
            user=self.user,
            image='test_files/post_one.jpg',
        )
        self.post_two = Post.objects.create(
            user=self.user,
            image='test_files/post_two.jpg',
        )
        self.url = reverse(
            viewname='saved-posts-dashboards'
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-posts-dashboard.html')


class NewPostTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.url = reverse(
            viewname='new-post'
        )
        self.client = Client()
        self.client.login(
            username='testuser',
            password='testpassword'
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new-post.html')

    def test_post(self):
        response = self.client.post(
            self.url,
            data={
                'image': SimpleUploadedFile(
                    name='test_image.jpg',
                    content=open('test_files/profile_image_one.jpg', 'rb').read(),
                    content_type='image/jpeg'
                ),
                'tags': 'tag1, tag2, tag3',
                'caption': 'test caption'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().tags.count(), 3)
        self.assertEqual(Post.objects.first().tags.first().name, 'tag1')
