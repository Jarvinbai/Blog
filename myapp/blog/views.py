from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,AboutUs,Category
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ContactForm, RegisterForm,LoginForm,ForgotPasswordForm,ResetPasswordForm,PostForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.

# posts = [
#     {'id':1, 'title': 'Post1','content': 'Content of Post1'},
#     {'id':2, 'title': 'Post2','content': 'Content of Post2'},
#     {'id':3, 'title': 'Post3','content': 'Content of Post3'},
#     {'id':4, 'title': 'Post4','content': 'Content of Post4'}
# ]

def index(request):
    blog_title = "Meet Our Community"
    # posts = Post.objects.all()
    all_posts = Post.objects.all()

    # Get search term if it exists
    search_term = request.GET.get('search', '')
    
    # If search term exists, filter the posts
    if search_term:
        all_posts = all_posts.filter(
            # Search in title OR content OR category name
            Q(title__icontains=search_term) | 
            Q(content__icontains=search_term) | 
            Q(category__name__icontains=search_term)
        )

    paginator = Paginator(all_posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # return render(request,"blog/index.html",{'blog_title':blog_title , 'posts':posts})
    return render(request,"blog/index.html",{'blog_title':blog_title , 'page_obj':page_obj,'search_term': search_term})

# def detail(request, post_id):
#     # post = next((item for item in posts if item['id'] == int(post_id)), None)
#     # logger = logging.getLogger("TESTING")
#     # logger.debug(f'post variable is {post}')

#     # getting data from model by post id

#     post = Post.objects.get(pk=post_id)
#     return render(request,"blog/detail.html",{'post':post})

def detail(request, slug):
    # post = next((item for item in posts if item['id'] == int(post_id)), None)
    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')

    # getting data from model by post id

    post = Post.objects.get(slug=slug)
    related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
    return render(request,"blog/detail.html",{'post':post, 'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("this is the new url")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,"blog/contact.html",{'form':form, 'name': name, 'email':email, 'message': message})
    return render(request,"blog/contact.html")

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here..."
    else:
        about_content = about_content.content
    return render(request,"blog/about.html",{'about_content':about_content})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False) # user data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            # print('register success')
            messages.success(request,'Registration Successfull. You can log in')
            return redirect('blog:login')
    else:
        form = RegisterForm()
        
    return render(request, 'blog/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('blog:dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form': form})


def dashboard(request):
    blog_title = "My Posts"
    #getting user posts
    all_posts = Post.objects.filter(user=request.user)

    # paginate
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/dashboard.html', {'blog_title': blog_title, 'page_obj': page_obj})


def logout(request):
    auth_logout(request) 
    return redirect('blog:index')  # Redirect to the Home page 


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        #form
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('blog/reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@bhai.com', [email])
            messages.success(request, 'Email has been sent')


    return render(request,'blog/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('blog:login')
            else :
                messages.error(request,'The password reset link is invalid')

    return render(request,'blog/reset_password.html', {'form': form})


def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        #form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')
    return render(request,'blog/new_post.html', {'categories': categories, 'form': form})