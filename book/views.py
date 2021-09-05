from django.shortcuts import render
from book.forms import PostSearchForm
from book.models import Book

def post_search(request):

    form = PostSearchForm

    results = []


    # take the information from HTML, which is 'q' from form.
    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            print(q)

            results = Book.objects.filter(title__icontains=q)

    return render(request, 'index.html', {'form':form, 'results':results})
