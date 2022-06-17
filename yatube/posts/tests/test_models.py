
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Group, Post, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='tetetete',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )
        cls.comments = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='test text',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

        comment = PostModelTest.comments
        expected_object_text = comment.text
        self.assertEqual(expected_object_text, str(comment))


class VerbosenameModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_two = User.objects.create_user(username='auth_two')
        cls.group = Group.objects.create(
            title='Группа',
            slug='testslug',
            description='группа любителей тестов',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий',
        )
        cls.follow = Follow.objects.create(
            user=cls.user_two,
            author=cls.user,
        )

    def test_comment_verbose_name(self):
        comment = VerbosenameModelTest.comment
        field_verboses = {
            'text': 'Текст комметария',
            'author': 'Автор',
            'post': 'Пост',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)

    def test_post_verbose_name(self):
        comment = VerbosenameModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Сообщество',
            'pub_date': 'Дата публикации',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)

    def test_group_verbose_name(self):
        comment = VerbosenameModelTest.group
        field_verboses = {
            'title': 'Название сообщества',
            'slug': 'Слаг ссылки',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)

    def test_follow_verbose_name(self):
        comment = VerbosenameModelTest.follow
        field_verboses = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)
