from django.shortcuts import render
from books.models import Book
from django.core.paginator import Paginator
from datetime import datetime


def get_all_books():
    books = Book.objects.order_by("pub_date")
    books_list = []
    for book in books:
        books_list.append(
            {
                "name": book.name,
                "author": book.author,
                "pub_date": book.pub_date,
            }
        )
    return books_list


def books_view(request):
    template = "books/books_list.html"
    books_list = get_all_books()
    context = {"books": books_list}
    return render(request, template, context)


def books_info(request, pub_date):
    template = "books/books_single.html"
    pubdate = datetime.strptime(pub_date, "%Y-%m-%d").date()
    books_list = get_all_books()
    paginator = Paginator(books_list, 1)
    page_number = 1
    for book in paginator.object_list:
        book_info = book.get("pub_date", False)
        if book_info == pubdate:
            page_number = paginator.object_list.index(book) + 1
    context = {}
    if page_number >= 0:
        next_page = page_number + 1
        next_page_url = ""
        prev_page = page_number - 1
        prev_page_url = ""
        if next_page <= len(books_list):
            next_page_url = (
                books_list[next_page - 1].get("pub_date").strftime("%Y-%m-%d")
            )
        if prev_page > 0:
            prev_page_url = (
                books_list[prev_page - 1].get("pub_date").strftime("%Y-%m-%d")
            )
        page_content = paginator.get_page(page_number)
        context = {
            "books": page_content,
            "page": page_content,
            "next_page_url": next_page_url,
            "prev_page_url": prev_page_url,
        }
    return render(request, template, context)
