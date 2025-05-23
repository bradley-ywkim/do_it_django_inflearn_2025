from django.shortcuts import render
from .models import Post


#views.py 관리방안
#FBV: Function Based -> 단순 get, post
#CBV: Class Based -> 이게 유지보수 get, post관리상좋다.

#views.py <-> models.py 커뮤니케이션

def index(request):
    #posts = Post.objects.all().order_by('-pk') #내림차순
    posts = Post.objects.all().order_by('pk') #오름차순 


    return render(
        request,
       'blog/index.html',
        {
            'posts': posts,
        }
    )