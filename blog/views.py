from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from django.core.paginator import Paginator
from .forms import BlogPost

def home(request):
    blogs = Blog.objects #쿼리셋 #메소드  #모델로부터 전달받은 객체목록
    blog_list = Blog.objects.all().order_by('-id')
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs': blogs,'posts':posts})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk = blog_id)

    return render(request, 'detail.html', {'blog':blog_detail})

def new(request):   #new.html을 띄워주는 함수
    return render(request, 'new.html')

def create(request): #입력받는 내용을 데이터베이스에 넣어주는 함수
    blog = Blog(image = request.FILES['image'])
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now() #작성 시점의 시간
    blog.save() #데이터베이스에 저장 -> 지우기는 delete
    return redirect('home')
    #쿼리셋과 메소드의 형식
    #모델.쿼리셋(objects).메소드

def blogpost(request):
    #입력된 내용을 처리하는 기능 -> post
    #빈 페이지를 띄워주는 기능 -> get
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})