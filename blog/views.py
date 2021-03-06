from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core.mail import send_mail
# from django.http import HttpResponseRedirect

from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm

POSTS_PER_PAGE = 5


def post_list(request):
	posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	paginator = Paginator(posts_list, POSTS_PER_PAGE)

	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			form.save_m2m()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()

	indexes = Post.objects.all()

	context = {'form': form,
			   'indexes': indexes
			   }

	return render(request, 'blog/post_edit.html', context)


@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			form.save_m2m()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)

	indexes = Post.objects.all()

	context = {'form': form,
			   'indexes': indexes
			   }

	return render(request, 'blog/post_edit.html', context)


@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')


def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)


# def contact_me(request):
# 	if request.method == "POST":
# 		form = ContactForm(request.POST)
# 		if form.is_valid():
# 			subject = form.cleaned_data['subject']
# 			sender = form.cleaned_data['contact_email']
# 			message = form.cleaned_data['subject']
# 			send_mail(subject, message, sender, ['rchang21@gmail.com'])
# 			return HttpResponseRedirect('/contact/thanks/')
# 	else:
# 		form = ContactForm()
# 	return render(request, 'blog/contact_form.html', {'form': form})
#
#
# def contact_thanks(request):
# 	return render(request, 'blog/contact_thanks.html')


def resume(request):
	return render(request, 'blog/resume.html')


def get_posts_with_tag(request, tag):
	posts_list = Post.objects.filter(published_date__lte=timezone.now())\
		.filter(tags__name__in=[tag])\
		.order_by('-published_date')
	paginator = Paginator(posts_list, POSTS_PER_PAGE)

	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post_list.html', {'posts': posts})


def about(request):
	return render(request, 'blog/about.html')