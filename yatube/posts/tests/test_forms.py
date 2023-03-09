import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Post, Group, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestForm(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.author_user = User.objects.create_user(username='leo')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.author_client = Client()
        self.author_client.force_login(TestForm.author_user)

        self.group = Group.objects.create(
            title='Group1',
            slug='group1',
            description='Group1'
        )
    
    def create_image(self) -> SimpleUploadedFile:
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        return SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    def test_create_post(self):
        """Проверка корректности создания поста."""
        count_post = Post.objects.count()
        upload_image = self.create_image()

        form_data = {
            'text': 'Новый пост',
            'group': self.group.pk,
            'image': upload_image
        }
        response = self.author_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), count_post + 1)
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': TestForm.author_user.username})
        )
        post: Post = Post.objects.all()[0]
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, Group.objects.get(pk=form_data['group']))
        self.assertEqual(post.image, f'posts/{upload_image.name}')

    def test_edit_post(self):
        """Проверка корректной работы измененеия поста."""
        post = Post.objects.create(
            text='Просто пост',
            author=self.author_user,
        )

        count_post = Post.objects.count()
        upload_image = self.create_image()
 
        form_data = {
            'text': 'Изменененый текст',
            'group': self.group.pk,
            'image': upload_image
        }
        response = self.author_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.pk}),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(pk=post.pk)

        self.assertEqual(Post.objects.count(), count_post)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, Group.objects.get(pk=form_data['group']))
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': post.pk})
        )
        self.assertEqual(post.image, f'posts/{upload_image.name}')

    def test_create_form_comment(self):
        """Проверка создания комментария.

        проверим что комментарий сохраняется и появляется на странице поста
        """
        count = Comment.objects.count()
        form_data = {
            'text': 'Это пробный комментарий'
        }

        post = Post.objects.create(
            text='Пост 1',
            author=TestForm.author_user,
            group=self.group,
        )

        response = self.author_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )

        comment = response.context.get('comments')[0]
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(Comment.objects.count(), count + 1)

    def test_unauthorized_user_cannot_create_comment(self):
        count_comment = Comment.objects.count()

        post = Post.objects.create(
            text='Просто пост',
            author=self.author_user,
        )

        form_data = {
            'text': 'Новый комментарий',
        }    

        url = reverse('posts:add_comment', kwargs={'post_id': post.id})       
        response = self.client.post(
            url,
            data=form_data,
            follow=True
        )

        self.assertEqual(Comment.objects.count(), count_comment)
        self.assertRedirects(response, '/auth/login/?next=' + url)            
