from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse
from os import listdir
from datetime import datetime


def home_view(request: HttpRequest) -> HttpResponse:
    template_name = "app/home.html"
    pages = {
        "Главная страница": reverse("home"),
        "Показать текущее время": reverse("time"),
        "Показать содержимое рабочей директории": reverse("workdir"),
    }

    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {"pages": pages}
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет,
    # возвращается просто текст
    current_time = None
    msg = f'Текущее время: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей
    # директории
    return HttpResponse(", ".join(listdir(path=".")))
