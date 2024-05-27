import re
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from accounts.models import Profile
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreatePostForm, UpdatePostForm, ContactForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# Create your views here.
@login_required
def home(request):  # sourcery skip: use-named-expression
    last_post =Blog.objects.last()
    c_count = Comment.objects.all().count()
    r_count = Reply.objects.all().count()
    total = c_count + r_count
    search = request.GET.get('search')
    if search:
        all_posts = Blog.objects.filter(Q(title__icontains= search) | Q(description__icontains= search)).order_by('-id')
    else:
        all_posts = Blog.objects.all().order_by('-id')
    paginator = Paginator(all_posts, 4)
    page= request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    
    context = {
        'posts':posts,
        'last_post':last_post,
        'total':total
    }
    return render(request, 'blog/home.html', context)
@login_required
def detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=post, active=True)
    replies = Reply.objects.filter(active=True)
    context = {
        'post':post,
        'comments':comments,
        'replies':replies,
    }
    return render(request, 'blog/detail.html', context)
@login_required
def mcategory(request, mcat_slug):
    all_posts= Blog.objects.all().order_by('-id')
    if mcat_slug:
        mcategories = get_object_or_404(MainCategory, slug=mcat_slug)
        posts = all_posts.filter(main_category__in=[mcategories])
    context = {
        'posts':posts,
    }
    return render(request,'blog/mcategory.html', context)
@login_required
def category(request, cat_slug):
    all_posts= Blog.objects.all().order_by('-id')
    if cat_slug:
        categories = get_object_or_404(Category, slug=cat_slug)
        posts = all_posts.filter(category__in=[categories])
    context = {
        'posts':posts,
    }
    return render(request,'blog/category.html', context)
@login_required
def scategory(request, scat_slug):
    all_posts= Blog.objects.all().order_by('-id')
    if scat_slug:
        scategories = get_object_or_404(SubCategory, slug=scat_slug)
        posts = all_posts.filter(sub_category__in=[scategories])
    context = {
        'posts':posts,
    }
    return render(request,'blog/scategory.html', context)


def comment(request):
    if request.POST:
        slug = request.POST['slug']
        comment = request.POST['comment']
        blog = Blog.objects.get(slug=slug)
        user = request.user
        new_comment = Comment.objects.create(name=user, content=comment,blog=blog,active=True)
        new_comment.save()
    
    return redirect('detail', slug)

def reply(request):
    if request.POST:
        slug = request.POST['slug']
        c = request.POST['c']
        reply = request.POST['reply']
        comment = Comment.objects.get(id=c)
        user = request.user
        new_reply = Reply.objects.create(name=user, reply=reply,comment=comment,active=True)  
    
    return redirect('detail',slug)


def comment_update(request):
    slug = request.POST['slug']
    comment_id = request.POST['c_id']
    comment = Comment.objects.get(id=comment_id)
    if request.POST:
        update = request.POST['update']
        comment.content = update
        comment.save()
    return redirect('detail', slug)

def reply_update(request):
    slug = request.POST['slug']
    reply_id = request.POST['r_id']
    reply = Reply.objects.get(id=reply_id)
    if request.POST:
        update = request.POST['updatereply']
        reply.reply = update
        reply.save()
    return redirect('detail', slug)

def comment_delete(request):
    if request.POST:
        slug = request.POST['slug']
        comment_id = request.POST['c_id']
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
    return redirect('detail', slug)

def reply_delete(request):
    if request.POST:
        slug = request.POST['slug']
        reply_id = request.POST['r_id']
        reply = Reply.objects.get(id=reply_id)
        reply.delete()
    return redirect('detail', slug)

@login_required
def add_post(request):
    if request.POST:
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post Created Successfully')
            return redirect('home')
        else:
            messages.warning(request, 'Error Check Your Data')
            return redirect('add_post')
    else:
        form = CreatePostForm()
    return render(request, 'blog/addpost.html', {'form':form})
@login_required
def update_post(request, slug):
    post = Blog.objects.get(slug=slug)
    if request.POST:
        form = UpdatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated Successfully')
            return redirect('detail', slug)
        else:
            messages.warning(request, 'Error Check Your Data')
            return redirect('update_post')
    else:
        form = UpdatePostForm(instance=post)
    return render(request, 'blog/updatepost.html', {'form':form})
@login_required
def delete_post(request, slug):
    post = Blog.objects.get(slug=slug).delete()
    messages.success(request, 'Post Has Been Deleted')
    return redirect('home')


def about(request):
    about= About.objects.all().first()
    profile = Profile.objects.all()
    return render(request, 'blog/about.html',{'about':about,'profile':profile})

@login_required
def contact(request):
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            subject = cd['subject']
            e_from = cd['e_from']
            message = f"{name} Send: {cd['message']}"
            send_mail(subject,message, e_from, ['django5448@gmail.com'])
            messages.success(request, 'Email Has Been Sent')
            return redirect('home')
        else:
            messages.warning(request, 'There Is Error')
    else:
        form = ContactForm()
        
    return render(request, 'blog/contact.html', {'form':form})