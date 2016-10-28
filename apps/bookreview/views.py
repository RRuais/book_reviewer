from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Book, Review

def index(request):
    return render(request, 'bookreview/index.html')


def register(request):
    if request.method == "POST":
        result = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], c_password=request.POST['c_password'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['email'] = result[1].email
            request.session['id'] = result[1].id
            return redirect(reverse('users_home'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect('/')

def login(request):
    if request.method == "POST":
        result = User.objects.login(email=request.POST['email'], password=request.POST['password'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['email'] = result[1].email
            request.session['id'] = result[1].id
            return redirect(reverse('users_home'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect(reverse('index'))

def users_home(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'users' : User.objects.all(),
        'latest_books' : Book.objects.all().order_by('-created_at')[:3],
        'all_books' : Book.objects.all()
    }
    return render(request, 'bookreview/home.html', context)

def show_user(request, id):
    user = User.objects.get(id=id)
    total_reviews = Review.objects.filter(users=user)
    count = len(total_reviews)

    context = {
        'user' : User.objects.get(id=id),
        'count' : count,
        'total_reviews' : total_reviews
    }

    return render(request, 'bookreview/show_user.html', context)

def logout(request):
    request.session.clear()
    return redirect(reverse('index'))

def books(request):
    return render(request, 'bookreview/add_book.html')

def add_book(request):
    if request.method == 'POST':
        user_id = User.objects.get(id=request.session['id'])
        rating = request.POST['rating']
        result = Book.objects.create(title=request.POST['title'], author=request.POST['author'], users=user_id)
        book = Book.objects.get(id=result.id)
        review = Review.objects.create(review=request.POST['review'], rating=rating, users=user_id, book=book)
        return redirect(reverse('users_home'))

def books_home(request, id):
    book = Book.objects.get(id=id)
    review = Review.objects.filter(book=book)

    context = {
        'book' : Book.objects.get(id=id),
        'reviews' : review
    }
    return render(request, 'bookreview/books_home.html', context)

def review(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.get(id=id)
        result = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], users=user, book=book)
        return redirect('books_home', id=book.id)
