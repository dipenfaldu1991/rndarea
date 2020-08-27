from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from chat import utility_functions as chat_utility_functions
from django.contrib.auth.models import User
from chat.models import Chat,  PrivateChat, Message
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.db.models import Max
from contacts import utility_functions as contacts_utility_functions
from accounts.models import profile


def u_profileimg(request):
    user_img=''
    if request.user.is_authenticated:
        u = profile.objects.get(user_id=request.user)
        user_img=u.image
        print('user image====================',user_img)
    return user_img



# restituisce la lista di chat private dell'utente corrente
@login_required()
def chat_list(request):
    chat_list = chat_utility_functions.get_user_private_chats(request)
    return render(request, 'private-chat-list.html',
                  {'private_chats': chat_list, 'len_chats': len(chat_list),'user_img':u_profileimg(request)})


#ci porta alla pagina per creare (o continuare) una chat privata, genera la lista di utenti con cui posso chattare
@login_required()
def new_chat(request):
    addable = chat_utility_functions.get_addable_users_private_chat(request)
    return render(request, 'new-chat.html', {'users': addable, 'len_addable': len(addable),'user_img':u_profileimg(request)})


# Genera una chat privata tra luser corrente e un altro dato partecipante, ci reindirizza direttamente alla pagina della chat.
@login_required
def create_chat(request):
    other_username = request.POST.get("other_username")
    other_user = User.objects.get(username=other_username)
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages,'user_img':u_profileimg(request)})

@login_required
def createnew_chat(request):
    other_user = User.objects.get(username=request.session["username"])
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages,'user_img':u_profileimg(request)})



#ci riporta alla pagina della chat privata dopo aver recuperato i messaggi
@login_required
def private_chat(request):
    chat_id = request.POST.get("id_chat")
    chat = PrivateChat.objects.get(id_chat=chat_id)
    messages = Message.objects.all().filter(chat=chat)
    if chat.participant1 == request.user:
        participant = chat.participant2
    else:
        participant = chat.participant1
    return render(request, 'chat.html', {'user2': participant, 'id_chat': chat_id, 'messages': messages,'user_img':u_profileimg(request)})



# presa una chat di gruppo, recupera i messaggi e i partecipanti e ci reindirizza alla sua pagina

# invia un messaggio dati in input i suoi campi. Funziona sia per chat privata che di gruppo visto che e' il messaggio
# che ricorda la chat alla quale appartiene.
@login_required
def send_message(request):
    chat_id = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=chat_id)
    text_message = request.POST.get("text-message-input")
    if len(text_message) > 0:
        messaggio=Message.add_this(Message(), chat, request.user, text_message)
    response = HttpResponse("200")
    return response

# recupera un messaggio dato il suo id
@login_required
def get_message_by_id(id):
    return Message.objects.all().get(id=id)




#restituisce i messaggi di una chat (singola o privata), in json, serve per il refresh ajax
def get_json_chat_messages(request):
    id_chat = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=id_chat)
    messaggi_query = Message.objects.all().filter(chat=chat)
    messaggi_json_array = []
    for messaggio in messaggi_query:
        msg = {'username': messaggio.sender.username, 'text': messaggio.text,
               'timestamp': messaggio.timestamp.strftime('%Y-%m-%d %H:%M')}
        messaggi_json_array.append(msg)
    return JsonResponse(messaggi_json_array, safe=False)