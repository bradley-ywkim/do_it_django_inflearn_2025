from django.db import models
import os
#라이브러리 > 패키지 > 모듈 > 클래스 > 매서드
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, null=True)    #카테고리를 이해할 수 있도록 글로 구분=그래서 유니크 되어야 한다.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'


    class Meta:
        verbose_name_plural = 'Categories'



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, null=True)    #카테고리를 이해할 수 있도록 글로 구분=그래서 유니크 되어야 한다.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'





#Post 테이블 만들기
class Post(models.Model):
    title = models.CharField(max_length=50)  #문자 50자까지 받을 수 있음
    hook_text = models.CharField(max_length=100, blank=True) #blank = 폼에 입력값 필수 채움 여부, null=db에 빈 값 여부 판단
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/image/%Y/%m/%d/', blank=True) #어디에 저장되게 할 건지 정의: 이 폴더에 저장해라.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #admin페이지에서 조회 불가
    updated_at = models.DateTimeField(auto_now=True) #admin페이지에서 조회 불가

    # author = models.ForeignKey(User, on_delete=models.CASCADE) #
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #계정 삭제해도 글 유지
    category = models.ForeignKey(Category, null=True, blank = True, on_delete=models.SET_NULL) #카테고리가 지워지더라도 포스트 안지워짐
    tags = models.ManyToManyField(Tag, blank=True)

    #만들었으면 cmder에서 makemigrations

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'


    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]


