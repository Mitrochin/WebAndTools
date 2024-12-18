from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Author, Quote, Tag
from datetime import datetime


def home(request):
    return render(request, 'quotes/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('quotes_app:login')
    else:
        form = UserRegisterForm()
    return render(request, 'quotes_app/register.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        born_date_str = request.POST['born_date']
        born_date = datetime.strptime(born_date_str, "%d.%m.%Y").date()
        born_location = request.POST['born_location']
        description = request.POST['description']
        Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()
        return redirect('quotes_app:authors')
    return render(request, 'quotes_app/add_author.html')


@login_required
def add_quote(request):
    if request.method == 'POST':
        quote_text = request.POST['quote']
        author_id = request.POST['author']
        author = Author.objects.filter(id=author_id).first()
        tags = request.POST['tags']
        user = request.user
        Quote(quote=quote_text, author=author, tags=tags, user=user).save()
        return redirect('quotes_app:quotes')
    authors = Author.objects.all()
    return render(request, 'quotes_app/add_quote.html', {'authors': authors})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes_app/authors.html', {'authors': authors})


def quote_list(request):
    quotes = Quote.objects.all()
    top_tags = Tag.objects.all()[:10]
    return render(request, 'quotes_app/quotes.html', {'quotes': quotes, 'top_tags': top_tags})


def author_detail(request, pk):
    try:
        author = get_object_or_404(Author, pk=pk)
        quotes = Quote.objects.filter(author=author)
        return render(request, 'quotes_app/author_detail.html', {'author': author, 'quotes': quotes})
    except Http404:
        return redirect('quotes_app:authors')


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    return render(request, 'quotes_app/tag_detail.html', {'tag': tag, 'quotes': quotes})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes_app/authors.html', {'authors': authors})




