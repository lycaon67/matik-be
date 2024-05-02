from django.db import models
import uuid

from core.util.model_to_dict import ModelToDictionary
# Create your models here.

class User(models.Model, ModelToDictionary):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    user_id = models.IntegerField(null=True, blank=True, unique=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=200, null=True)
    role = models.IntegerField()
   
    class Meta:
        managed = True
        db_table = 'user'
            

    def __str__(self):
        return self.id
    
