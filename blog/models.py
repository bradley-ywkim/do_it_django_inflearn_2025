from django.db import models

#라이브러리 > 패키지 > 모듈 > 클래스 > 매서드

#Post 테이블 만들기
class Post(models.Model):
    title = models.CharField(max_length=50)  #문자 50자까지 받을 수 있음
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True) #admin페이지에서 조회 불가
    updated_at = models.DateTimeField(auto_now=True) #admin페이지에서 조회 불가
    #author
    #만들었으면 cmder에서 makemigrations

    def __str__(self):
        return f'[{self.pk}] {self.title}'





