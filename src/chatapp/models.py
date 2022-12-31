from django.db import models


class Room(models.Model):
    """  """
    
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.name
    

class Message(models.Model):
    """  """
    
    author = models.CharField(max_length=255, null=False, blank=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)
    is_changed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'[{self.room}] ({self.author}) {self.text}'
