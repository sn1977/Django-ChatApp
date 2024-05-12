from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers


@login_required(login_url="/login/")
def index(request):
    """
    This is a view to render the chat html (ist ein Beispiel).
    """
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )
        serialized_obj = serializers.serialize('json', [new_message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages})


def login_view(request):
    redirect = request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get("redirect"))
        else:
            return render(
                request,
                "auth/login.html",
                {"wrongPassword": True, "redirect": redirect},
            )
    return render(request, "auth/login.html", {"redirect": redirect})


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Hier kannst du weitere Felder aus dem Formular abrufen und dem Benutzer zuweisen

        # Benutzer erstellen und in die Datenbank speichern
        user = User.objects.create_user(username, password=password)
        # Weitere Benutzerattribute setzen, falls erforderlich
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Optional: Weiterleitung nach erfolgreicher Registrierung
        return redirect('login/')  # Zum Beispiel zur Login-Seite

    # GET-Anfrage: Das Registrierungsformular anzeigen
    return render(request, "auth/register.html")

