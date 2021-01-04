from django.urls import path
from . import views

app_name = 'myBlog'
urlpatterns = [
	path('', views.index, name='index'),
	path('threads/', views.threads, name='threads'),
	path('threads/<int:id>/', views.thread, name='thread'),
	path('thread/edit/<int:id>/',views.edit, name ='edit'),
	path('thread/new/',views.new, name ='new'),
	path('accounts/sign_up/',views.sign_up, name="sign_up"),
	path('threads/comment/<int:id>/', views.postComment, name ='postComment')
]