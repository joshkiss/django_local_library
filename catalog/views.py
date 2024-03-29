from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic 
from .models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # the .all() is implied by default
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors, 
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 2
    
    # template_name = 
    # queryset = Book.objects.filter(genre__icontains='language')[:5]
    # template_name = 'books/my_arbitrary_template_name_list.html'
    
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'this is just some data'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=Author)
        return context
    

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()