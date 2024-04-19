from django.db import connection
from django.shortcuts import render
from .models import User


def fetch_student(request):
    alias_field = {
        "first_name": "fname",
        "email": "mail",
        "pk": "id",
    }
    # res = User.objects.all()
    res = User.objects.raw("SELECT * FROM user_user", translations=alias_field)
    return render(request, "index.html", {"res": res})


# sql fetch all rows
def fetch_all(request):
    with connection.cursor() as sql:
        res = sql.execute("SELECT * FROM user_user").fetchall()
    return render(request, "index.html", {"res": res})


# sql fetch one row
def find_one(request):
    with connection.cursor() as sql:
        sql.execute("SELECT * FROM user_user")
        res = sql.fetchone()
    return render(request, "index.html", {"res": res})


def create_customer(request):
    info = User(
        first_name=request.POST.get("first_name"),
        last_name=request.POST.get("last_name"),
        gender=request.POST.get("gender"),
    )
    info.save()