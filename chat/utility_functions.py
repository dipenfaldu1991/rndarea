
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import User
from chat.models import Chat, PrivateChat, Message,Warning
from django.contrib.auth.models import User

# controlla fra tutte le chat private nel sistema e restituisce quelle in cui l'user corrente
# è presente come primo o secondo partecipante
def get_user_private_chats(request):
    user_in_p1 = PrivateChat.objects.all().filter(participant1=request.user)
    user_in_p2 = PrivateChat.objects.all().filter(participant2=request.user)
    userp = PrivateChat.objects.filter(participant1=request.user)
    user=User.objects.get(username=request.user)
    warning=Warning.objects.filter(sender_id=request.user).values_list('chat_id', flat=True)
    ussss =Warning.objects.values('chat_id').annotate(warning_count=Count('chat_id')).filter(warning_count__gt=0)
    return user_in_p1 | user_in_p2 ,warning,userp,ussss



# restituisce gli utenti con cui posso avere una chat privata.
def get_addable_users_private_chat(request):
    contacts = [user for user in contacts_utility_function.get_contacts(request)]
    return contacts


#restituisce gli utenti presenti nei contatti che ancora non ho aggiunto a un dato gruppo
#viene usata per aggiungere utenti a un gruppo già esistente

# restituisce la lista di partecipanti di un dato gruppo
