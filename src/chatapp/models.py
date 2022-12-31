from django.db import models


class Room(models.Model):
    """  """
    
    name = models.CharField(max_length=255, null=False, blank=False)
    

class Message(models.Model):
    """  """
    
    author = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)
    is_changed = models.BooleanField(default=False)
