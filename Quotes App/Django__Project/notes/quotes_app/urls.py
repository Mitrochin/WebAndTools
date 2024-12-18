from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='quotes_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='quotes_app:login'), name='logout'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/', views.author_list, name='authors'),
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),
]































