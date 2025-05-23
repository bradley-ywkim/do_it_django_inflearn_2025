from django.shortcuts import render
from .models import Post


#views.py 관리방안
#FBV: Function Based -> 단순 get, post
#CBV: Class Based -> 이게 유지보수 get, post관리상좋다.

#views.py <-> models.py 커뮤니케이션

from django.views.generic import ListView

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/post_list.html' -> 지워도 됨





# def index(request):
#     #posts = Post.objects.all().order_by('-pk') #내림차순
#     posts = Post.objects.all().order_by('pk') #오름차순
#
#
#     return render(
#         request,
#        'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_page.html',
        {
            'post': post,
        }
      )

