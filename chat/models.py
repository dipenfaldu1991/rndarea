from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from rndarea import settings
from json import JSONEncoder
from django.db.models import Max

# Create your models here.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Chat, contiene id e id_ultimo messaggio
class Chat(models.Model):
    id_chat = models.SmallIntegerField('id_chat', default=-1, primary_key=True)

    # assegna come id_chat il valore successivo all'id maggiore
    def counter(self):
        if Chat.objects.count() > 0:
            last_chat = Chat.objects.all().order_by('-id_chat')[0]
            no = last_chat.id_chat
        else:
            no = 0
        return no + 1

# Chat privata, ricorda i 2 partecipanti
class PrivateChat(Chat):
    participant1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant1',
                                     default='admin')
    participant2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant2',
                                     default='admin')
    unique_together = (('participant1', 'participant2'),)

    #aggiunge una chat privata
    def add_this(self, user1, user2):
        #controlla se esiste, se non esiste la crea
        if not self.check_if_exist(user1, user2):
            self.id_chat = self.counter()
            self.participant1 = user1
            self.participant2 = user2
            self.save()
            return self
        #se esiste restituisce l'istanza esistente, fa un controllo sulla posizione in cui si trova il nostro user
        else:
            is_user_part1 = len(PrivateChat.objects.all().filter(participant1=user1, participant2=user2))
            if is_user_part1 > 0:
                return PrivateChat.objects.all().get(participant1=user1, participant2=user2)
            else:
                return PrivateChat.objects.all().get(participant1=user2, participant2=user1)

    #controlla se esite una chat privata
    def check_if_exist(self, user1, user2):
        if (PrivateChat.objects.filter(participant1=user1, participant2=user2).count() == 0) and (
                PrivateChat.objects.filter(participant1=user2, participant2=user1).count() == 0):
            return False
        else:
            return True


class Message(models.Model):
    id = models.SmallIntegerField('ID', primary_key=True, default=-1)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField('text', max_length=255, default="text")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    status=models.CharField(max_length=300,default='unread')

    #restituisce come id da usare per un nuovo messaggio, il numero successivo a quello dell'id piu' grande presente
    def counter(self):
        if Message.objects.count() > 0:
            # -id vuol dire che ordina per id in maniera decrescente
            last_message = Message.objects.all().order_by('-id')[0]
            no = last_message.id
        else:
            no = 0
        return no + 1

    #aggiunge un messaggio data chat, mittente e testo.
    def add_this(self, chat, sender, text):
        self.id = self.counter()
        self.sender = sender
        self.text = text
        self.chat = chat
        self.save()
        return self

    def add_notification(self, Message):
        notification = Message(user=self.user, Message=Message)
        notification.save

class Warning(models.Model):
    id = models.SmallIntegerField('ID', primary_key=True, default=-1)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='senders')
    timestamp = models.DateTimeField(auto_now_add=True)
    warning = models.CharField('warning', max_length=255, default="text")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    status=models.CharField(max_length=300,default='unread')

    #restituisce come id da usare per un nuovo messaggio, il numero successivo a quello dell'id piu' grande presente
    def counter(self):
        if Message.objects.count() > 0:
            # -id vuol dire che ordina per id in maniera decrescente
            last_message = Message.objects.all().order_by('-id')[0]
            no = last_message.id
        else:
            no = 0
        return no + 1

    #aggiunge un messaggio data chat, mittente e testo.
    def add_this(self, chat, sender, warning):
        self.id = self.counter()
        self.sender = sender
        self.warning = warning
        self.chat = chat
        self.save()
        return self

    def add_notification(self, Message):
        notification = Message(user=self.user, Message=Message)
        notification.save        