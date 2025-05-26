from django.shortcuts import render
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# views.py 관리방안
# FBV: Function Based -> 단순 get, post
# CBV: Class Based -> 이게 유지보수 get, post관리상좋다.

# views.py <-> models.py 커뮤니케이션


class PostList(ListView):
    model = Post
    ordering = '-pk'  # 생성일 내림차순 정렬 (최신 글 위로)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostCreate(CreateView):
    model = Post #레코드를 만들 수 있게 하는 기능
    #post의 어떤것들을 쓸것인지 정의
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']



class PostDetail(DetailView):
    model = Post

    # 기본으로 제공되는 Post 객체외 다른 데이터를 추가로 넘기는 것.
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None).order_by('-pk')  # 최신순 정렬
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category).order_by('-pk')  # 최신순 정렬

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )




def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'tag': tag,
    })
