from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('posts/new', views.new),
    path('posts/add', views.create),
    path('posts/edit/<int:id>', views.edit),
    path('posts/update/<int:id>', views.update),
    path('posts/delete/<int:id>', views.delete),
    path('posts/<int:id>', views.show_post),
    path('my-posts', views.show_logged_user_posts),
    path('collection', views.show_collection),
    path('posts/save/<int:id>', views.save),
    path('posts/unsave/<int:id>', views.unsave),
    # path('', views.index),
    # path('', views.index),
]