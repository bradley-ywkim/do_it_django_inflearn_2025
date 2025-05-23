from django.db import models

#라이브러리 > 패키지 > 모듈 > 클래스 > 매서드

#Post 테이블 만들기
class Post(models.Model):
    title = models.CharField(max_length=50)  #문자 50자까지 받을 수 있음
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/image/%Y/%m/%d/', blank=True) #어디에 저장되게 할 건지 정의: 이 폴더에 저장해라.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #admin페이지에서 조회 불가
    updated_at = models.DateTimeField(auto_now=True) #admin페이지에서 조회 불가

    #author
    #만들었으면 cmder에서 makemigrations

    def __str__(self):
        return f'[{self.pk}] {self.title}'


    def get_absolute_url(self):
        return f'/blog/{self.pk}/'



