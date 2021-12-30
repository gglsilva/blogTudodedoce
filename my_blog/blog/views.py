from django.core import paginator
from django.core.checks import messages
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .forms import EmailPostForm
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


def post_share(request, post_id):
    # recupera o post pelo id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # formulário enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # campos do formulário estão validados
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}  recomenda ler {post.title}"
            message = f"Você deve ler {post.title} em {post_url} \n\n \
                        {cd['name']}  \n {cd['email']}"
            send_mail(subject, message, 'gb.pydeveloper@gmail.com', [cd['to']])
            sent = True
            # envia um email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,'form':form, 'sent':sent})
