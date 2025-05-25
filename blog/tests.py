from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.contrib.auth.models import User

class TestView(TestCase):
    def setUp(self):
        self.client = Client() #Client: 방문자의 브라우저를 의미
        self.user_trump = User.objects.create_user(
            username='trump',
            password='somepassword'
        )
        self.user_obama = User.objects.create_user(
            username='obama',
            password='somepassword'
        )

        self.category_programming = Category.objects.create(
            name = 'programming', slug='programming'
        )

        self.category_music = Category.objects.create(
            name='music', slug='music'
        )



        # Tag 태그
        self.tag_python_kor = Tag.objects.create(
            name="파이썬 공부", slug="파이썬-공부"
        )
        self.tag_python = Tag.objects.create(
            name="python", slug="python"
        )
        self.tag_hello = Tag.objects.create(
            name="hello", slug="hello"
        )


        self.post_001 = Post.objects.create( #쿼리
            title = '첫번째 포스트 입니다.',
            content = 'Hello, World. We are the World.',
            category = self.category_programming,
            author=self.user_trump,
        )

        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content = '저는 쌀국수를 좋아합니다.',
            category = self.category_music,
            author=self.user_obama,
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='카테고리가 없을 수 있죠.',
            author=self.user_obama,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)


    def navbar_test(self, soup):
        # 네브바
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')



    #list, detail다있으므로 별도 함수로 작성
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories_card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류({Post.objects.filter(category=None).count()})', categories_card.text)

    def test_post_list_with_posts(self):
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/') #서버에 blog로 요청하는 행위 코드
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser') #내용을 가져오고 이건 html이다라고 인지시켜주는 코드
        self.assertIn('Blog', soup.title.text)

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

    def test_post_list_without_posts(self):
        Post.objects.all().delete()
        self.assertEqual(0, Post.objects.count())

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.assertIn('Blog', soup.title.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)






    def test_post_detail(self):

        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)
        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.category.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)


    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200) #정상 응답 수신

        soup = BeautifulSoup(response.content, 'html.parser') #파싱 내용 출력
        self.navbar_test(soup) #내비게이션 바 정상 출력 확인
        self.category_card_test(soup) #카테고리 목록 ui 정상 출력 확인

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.h1.text)
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
