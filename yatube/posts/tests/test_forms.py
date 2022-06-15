
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Comment, Group, Post
from posts.tests.fixtures.fixture_data import SMALL_GIF

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.small_gif = SMALL_GIF
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='testtext',
        )
        cls.post = Post.objects.create(
            text='Текстовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded
        )
        cls.form = PostForm()
        cls.form_data = {
            'text': 'Тестовый пробного комметария'
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_create_post(self):
        """Форма создает запись в Post."""
        """Проверяем редирект и создание новой записи"""
        post_count = Post.objects.count()
        testimage = SimpleUploadedFile(
            name='small.gif',
            content=PostCreateFormTests.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст',
            'group': PostCreateFormTests.group.id,
            'image': testimage
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': PostCreateFormTests.user.username}
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_post_edit_change_post_in_db(self):
        """Проверка редактирования поста в базе данных."""

        testimage = SimpleUploadedFile(
            name='small_new.gif',
            content=PostCreateFormTests.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Редактированный текст',
            'group': PostCreateFormTests.group.id,
            'image': testimage,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostCreateFormTests.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail',
                kwargs={'post_id': PostCreateFormTests.post.pk}
            )
        )
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
                image='posts/small_new.gif',
            ).exists()
        )

    def test_add_comments_form_correct_working(self):
        """Проверка создания записи Comments в БД"""
        form_data = {
            'text': 'Тестовый пробного комметария',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostCreateFormTests.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail',
                kwargs={'post_id': PostCreateFormTests.post.pk}
            )
        )
        self.assertTrue(
            Comment.objects.filter(
                text=form_data['text'],
                post=PostCreateFormTests.post.pk,
            ).exists()
        )

    def test_add_comments_guest_redirect_login(self):
        """Проверка редиректа неавторизованного юзера при
        попытке отправить форму Comments"""
        form_data = {
            'text': 'Тестовый пробного комметария',
        }
        response = self.guest_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostCreateFormTests.post.pk}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, (
                reverse('users:login') + '?next=' + reverse(
                    'posts:post_detail',
                    kwargs={'post_id': PostCreateFormTests.post.pk}
                ) + 'comment/'
            )
        )
