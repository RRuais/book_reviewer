from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/register$', views.register, name='register'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/home$', views.users_home, name='users_home'),
    url(r'^users/(?P<id>\w+)$', views.show_user, name='show_user'),
    url(r'^books$', views.books, name='books'),
    url(r'^books/add$', views.add_book, name='add_book'),
    url(r'^books/(?P<id>\w+)$', views.books_home, name="books_home"),
    url(r'^books/review/(?P<id>\w+)$', views.review, name='review'),
    url(r'^logout', views.logout, name='logout')

]
