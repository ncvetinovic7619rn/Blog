from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from django.contrib import messages
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm

# Create your views here.

def index(request):
	if not request.user.is_authenticated:
		return render(request, 'index.html', {'page_title': 'LOL'})
	else:
		return redirect('myBlog:threads')

@login_required
def thread(request, id):
	tmp = get_object_or_404(Thread, id=id)
	return render(request, 'thread.html', {'thread': tmp, 'page_title' : tmp.title})

@login_required
def threads(request):
	tmp = Thread.objects.all()
	return render(request, 'threads.html',{'threads': tmp})

@permission_required('myBlog.add_thread')
def new(request):
	if request.method =='POST':
		form = ThreadForm(request.POST)
		if form.is_valid():
			t = Thread(title=form.cleaned_data['title'], content=form.cleaned_data['content'], owner=request.user)
			t.save()
			return redirect('myBlog:threads')
		else:
			return render(request, 'new.html', {'form':form})
	else:
		form = ThreadForm()
		return render(request, 'new.html',{'form':form})

@permission_required('myBlog.change_thread')
def edit(request, id):
	if request.method == 'POST':
		form = ThreadForm(request.POST)
		if form.is_valid():
			t = Thread.objects.get(id=id)
			t.title = form.cleaned_data['title']
			t.content = form.cleaned_data['content']
			t.save()
			return redirect('myBlog:threads')
		else:
			return redirect(request, 'edit.html', {'form': form , 'id' : id})
	else:
		t = Thread.objects.get(id=id)
		form = ThreadForm(instance=t)
		return render(request, 'edit.html', {'form': form, 'id': id})

def sign_up(request):
	context = {}
	form = UserCreationForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			group =Group.objects.get_or_create(name = 'Regular')
			user = form.save()
			user.groups.add(1)
			return redirect('myBlog:threads')
	context['form'] = form
	return render(request,'registration/sign_up.html', context)

@login_required
def postComment(request, id):
	form = CommentForm(request.POST.get('comment'))
	tmp = get_object_or_404(Thread, id=id)
	if request.method =='POST':
		if request.POST.get('comment'):
			user = request.user
			comm = request.POST.get('comment')
			t = Thread.objects.get(id=id)
			comment = Comment(comment = comm,thread = t,user=user)
			comment.save()
			messages.success(request,"Your comment has been posted successfully")
		else:
			return render(request,'thread.html', {'id':id})
	return render(request, 'thread.html', {'thread': tmp, 'page_title' : tmp.title})
		

