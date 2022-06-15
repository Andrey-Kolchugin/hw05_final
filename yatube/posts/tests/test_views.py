import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post
from posts.tests.fixtures.fixture_data import test_picture

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.picture = test_picture
        cls.user = User.objects.create_user(username='test_user2')
        cls.user_two = User.objects.create_user(username='test_user_two')
        cls.group = Group.objects.create(
            title='test_group2',
            slug='test_group2',
            description='testtext'
        )
        cls.group2 = Group.objects.create(
            title='test_group3',
            slug='test_group3',
            description='testtest2',
        )
        cls.post = Post.objects.create(
            pk=1,
            text='Текстовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.picture,
        )
        cls.comment = Comment.objects.create(
            text='Текст комментария',
            post=cls.post,
            author=cls.user,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_two,
            author=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)
        self.authorized_client_two = Client()
        self.authorized_client_two.force_login(PostPagesTests.user_two)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует верный шаблон."""
        cache.clear()
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':
                    self.user.username}): 'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_detail', kwargs={'post_id':
                    self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id':
                    self.post.id}): 'posts/create_post.html',
            reverse('posts:follow_index'): 'posts/follow.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        """Созданный пост появился на стартовой странице."""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        index_text_0 = first_object.text
        index_author_0 = first_object.author.username
        index_group_0 = first_object.group.title
        index_group_slug_0 = first_object.group.slug
        index_image_0 = first_object.image.name
        self.assertEqual(index_text_0, PostPagesTests.post.text)
        self.assertEqual(index_author_0, PostPagesTests.post.author.username)
        self.assertEqual(index_group_0, PostPagesTests.group.title)
        self.assertEqual(index_group_slug_0, PostPagesTests.group.slug)
        self.assertEqual(index_image_0, PostPagesTests.post.image.name)

    def test_follow_index_page_show_correct_context(self):
        """Шаблон follow_index сформирован с правильным контекстом."""
        response = self.authorized_client_two.get(
            reverse('posts:follow_index')
        )
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        index_text_0 = first_object.text
        index_author_0 = first_object.author.username
        index_group_0 = first_object.group.title
        index_group_slug_0 = first_object.group.slug
        index_image_0 = first_object.image.name
        self.assertEqual(index_text_0, PostPagesTests.post.text)
        self.assertEqual(index_author_0, PostPagesTests.post.author.username)
        self.assertEqual(index_group_0, PostPagesTests.group.title)
        self.assertEqual(index_group_slug_0, PostPagesTests.group.slug)
        self.assertEqual(index_image_0, PostPagesTests.post.image.name)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        """Созданный пост появился на странице группы"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        index_text_0 = first_object.text
        index_author_0 = first_object.author.username
        index_group_0 = first_object.group.title
        index_group_slug_0 = first_object.group.slug
        index_image_0 = first_object.image.name
        self.assertEqual(index_text_0, PostPagesTests.post.text)
        self.assertEqual(index_author_0, PostPagesTests.post.author.username)
        self.assertEqual(index_group_0, PostPagesTests.group.title)
        self.assertEqual(index_group_slug_0, PostPagesTests.group.slug)
        self.assertEqual(index_image_0, PostPagesTests.post.image.name)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username':
                    self.user.username})
        )
        self.assertIn('page_obj', response.context)
        first_object = response.context['page_obj'][0]
        crnt_page_text_0 = first_object.text
        crnt_page_author_0 = first_object.author.username
        crnt_page_group_0 = first_object.group.title
        crnt_page_group_slug_0 = first_object.group.slug
        crnt_page_image_0 = first_object.image.name
        self.assertEqual(crnt_page_text_0, PostPagesTests.post.text)
        self.assertEqual(
            crnt_page_author_0,
            PostPagesTests.post.author.username
        )
        self.assertEqual(crnt_page_group_0, PostPagesTests.group.title)
        self.assertEqual(crnt_page_group_slug_0, PostPagesTests.group.slug)
        self.assertEqual(crnt_page_image_0, PostPagesTests.post.image.name)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id':
                    self.post.id})
        )
        self.assertIn('post', response.context)
        self.assertIn('comments', response.context)
        page_object = response.context['post']
        comment_obj = response.context['comments'][0]
        comment = comment_obj.text
        crnt_page_text_0 = page_object.text
        crnt_page_author_0 = page_object.author.username
        crnt_page_group_0 = page_object.group.title
        crnt_page_group_slug_0 = page_object.group.slug
        crnt_page_post_id = page_object.pk
        crnt_page_image_0 = page_object.image.name
        self.assertEqual(crnt_page_text_0, PostPagesTests.post.text)
        self.assertEqual(
            crnt_page_author_0,
            PostPagesTests.post.author.username
        )
        self.assertEqual(crnt_page_group_0, PostPagesTests.group.title)
        self.assertEqual(crnt_page_group_slug_0, PostPagesTests.group.slug)
        self.assertEqual(crnt_page_post_id, PostPagesTests.post.pk)
        self.assertEqual(crnt_page_image_0, PostPagesTests.post.image.name)
        self.assertEqual(comment, PostPagesTests.comment.text)

    def test_post_edit_page_show_correct_context(self):
        """Форма create_post в post_edit работает корректно."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id':
                    self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_page_show_correct_context(self):
        """Форма create_post в post_create работает корректно."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_is_not_other_group(self):
        """проверка того, что новый пост попадает только в свою группу"""
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group2.slug})
        )
        self.assertEqual(len(response.context['page_obj']), 0)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.user_two = User.objects.create_user(username='test_user_two')
        cls.group = Group.objects.create(
            title='test_group',
            slug='test_group',
            description='testtest',
        )
        cls.follow = Follow.objects.create(
            user=cls.user_two,
            author=cls.user,
        )
        post_list = [Post(
            author=PaginatorViewsTest.user,
            text=f'Тестовый текст {i}',
            group=PaginatorViewsTest.group,) for i in range(0, 13)]
        Post.objects.bulk_create(post_list)
        cls.paginator_test_page_urls = (
            (reverse('posts:index')),
            (reverse('posts:follow_index')),
            (reverse('posts:group_list', kwargs={'slug': cls.group.slug})),
            (reverse('posts:profile', kwargs={'username': cls.user.username})),
        )

    def setUp(self):
        self.authorized_client_two = Client()
        self.authorized_client_two.force_login(PaginatorViewsTest.user_two)

    def test_index_first_page_contains_ten_records(self):
        """проверка пангинатора на первой стр. """
        cache.clear()
        ursl_for_test = PaginatorViewsTest.paginator_test_page_urls
        for address in ursl_for_test:
            with self.subTest(address=address):
                response = self.authorized_client_two.get(address)
                self.assertIn('page_obj', response.context)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        """проверка пангинатора на последней стр. index"""
        ursl_for_test = PaginatorViewsTest.paginator_test_page_urls
        for address in ursl_for_test:
            with self.subTest(address=address):
                response = self.authorized_client_two.get(
                    address, {'page': '2'}
                )
                self.assertIn('page_obj', response.context)
                self.assertEqual(len(response.context['page_obj']), 3)


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()

    def test_cache_works_index_page(self):
        """Проверка кэширования страницы index."""
        response = self.guest_client.get(reverse('posts:index'))
        Post.objects.create(
            text='Cache test',
            author=CacheTests.user,
        )
        cache.clear()
        new_response = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(response.context, new_response.context)

    def test_cache_works_index_page_after_post_delete(self):
        """Кэширование страницы index после удаления поста."""
        response = self.guest_client.get(reverse('posts:index'))
        Post.objects.filter(pk=CacheTests.post.pk).delete()
        new_response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.content, new_response.content)


class Follow_system_Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Подписчик
        cls.user_one = User.objects.create_user(username='Follower')
        # Юзер, на которого тестируется функция подписки
        cls.user_two = User.objects.create_user(username='Followme')
        # Юзер, на которого есть действующая подписка
        cls.user_three = User.objects.create_user(username='Followmeto')
        cls.post_two = Post.objects.create(
            author=cls.user_two,
            text='Пост для подписки',
        )
        cls.post_three = Post.objects.create(
            author=cls.user_three,
            text='Пост для подписки',
        )
        cls.follow = Follow.objects.create(
            user=cls.user_one,
            author=cls.user_three,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(Follow_system_Tests.user_one)
        self.authorized_client_two = Client()
        self.authorized_client_two.force_login(Follow_system_Tests.user_two)

    def test_auth_user_following_other_user(self):
        """Авторизованный юзер может подписываться на других юзеров"""
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user_two.username}
            )
        )
        self.assertTrue(
            Follow.objects.filter(
                user=Follow_system_Tests.user_one,
                author=Follow_system_Tests.user_two,
            ).exists()
        )

    def test_auth_user_can_unfollowing_user(self):
        """Авторизованный юзер может удалять подписку"""
        follow_count = Follow.objects.count()
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user_three.username}
            )
        )
        self.assertEqual(follow_count, Follow.objects.count() + 1)

    def test_new_post_add_to_newsline_follower_user(self):
        """Новая запись пользователя появляется в ленте подписчика"""
        response = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        self.assertIn('page_obj', response.context)
        page_obj = response.context['page_obj'][0]
        self.assertEqual(page_obj.text, Follow_system_Tests.post_three.text)

    def test_new_no_exist_in_unfollowet_newsline_page(self):
        """Новая запись не появляется в ленте тех,кто не подписан"""
        response = self.authorized_client_two.get(
            reverse('posts:follow_index')
        )
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 0)
