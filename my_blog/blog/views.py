from django.core import paginator
from django.http import request
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    """
    Recupera todos os posts do blog e define 3 posts por página
    se for inteiro recuperar a ultima página, se não recupera a 
    primeira pagina, por fim retorna as paginas e os posts
    """
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page,
                                                'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Tenta recuperar o post pelo slug, caso não encontre retorna 404
    retorna o template e o post selecionado
    """
    post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request, 'blog/post/detail.html', {'post':post})
