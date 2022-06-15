from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from posts.models import Comment, Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.user_not_author = User.objects.create_user(username='test_user2')
        cls.group = Group.objects.create(
            title='test_group',
            slug='test_group',
            description='testtext'
        )

        cls.post = Post.objects.create(
            pk=1,
            text='Текстовый текст',
            author=cls.user,
            group=cls.group
        )
        cls.comment = Comment.objects.create(
            text='Текст комментария',
            post=cls.post,
            author=cls.user,
        )
        cls.post_url = f'/{cls.user.username}/{cls.post.id}/'

        cls.public_urls = (
            ('/', 'posts/index.html'),
            (f'/group/{cls.group.slug}/', 'posts/group_list.html'),
            (f'/profile/{cls.user.username}/', 'posts/profile.html'),
            (f'/posts/{cls.post.id}/', 'posts/post_detail.html'),
        )
        cls.auth_user_urls_only = (
            ('/create/', 'posts/create_post.html'),
            ('/follow/', 'posts/follow.html'),
        )
        cls.auth_author_urls_only = (
            (f'/posts/{cls.post.id}/edit/', 'posts/create_post.html'),
        )
        cls.redirect_url = (
            (f'/posts/{cls.post.id}/edit/',
                f'/auth/login/?next=/posts/{cls.post.id}/edit/'),
            ('/create/', '/auth/login/?next=/create/')
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)
        self.authorized_not_author_client = Client()
        self.authorized_not_author_client.force_login(
            PostURLTests.user_not_author
        )

    def test_url_exists_at_desired_location(self):
        """Страницы / доступ любому пользователю."""
        urls_for_test = PostURLTests.public_urls
        for url in urls_for_test:
            with self.subTest(url=url[0]):
                response = self.guest_client.get(url[0])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_return_404(self):
        """Страница не существует и вернет 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_only_author_permission_page(self):
        """Проверка страница, доступной только автору."""
        urls_for_test = PostURLTests.auth_author_urls_only
        for url in urls_for_test:
            with self.subTest(url=url[0]):
                response = self.authorized_client.get(url[0])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_only_auth_user_page(self):
        """Проверка страницы, доступной только авторизованному юзеру."""
        urls_for_test = PostURLTests.auth_user_urls_only
        for url in urls_for_test:
            with self.subTest(url=url):
                response = self.authorized_not_author_client.get(url[0])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        url3 = PostURLTests.auth_user_urls_only
        url2 = PostURLTests.auth_author_urls_only
        url1 = PostURLTests.public_urls
        url = url1 + url2 + url3

        for address, template in url:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_post_edit_accsess_denied_for_non_author(self):
        """Проверка невозможности для редактирования поста для неавтора."""
        url_user_non_author = (
            (f'/posts/{self.post.id}/edit/'),
        )
        for address in url_user_non_author:
            with self.subTest(address=address):
                response = self.authorized_not_author_client.get(
                    address
                )
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_posts_urls_redirect_anon_to_login(self):
        """Проверка переадресации неавторизованного пользователя """
        """на главную страницу."""
        urls_for_guest_to_redirect = PostURLTests.redirect_url
        for address, expected in urls_for_guest_to_redirect:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertRedirects(response, expected)
