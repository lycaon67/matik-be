from django.db import models
from user.models import User
import uuid
from core.util.model_to_dict import ModelToDictionary

# Create your models here.

class Homes(models.Model, ModelToDictionary):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, default="")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'homes'
            

    def __str__(self):
        return self.id
    
class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    home = models.ForeignKey(Homes, models.DO_NOTHING)
    type = models.IntegerField() ## 0 - Kitchen, 1 - Living Room, 2 - Garage, 3 - Bed Room, 5 - Office

    class Meta:
        managed = True
        db_table = 'rooms'
            

    def __str__(self):
        return self.id

# Create your models here.

class HomeUserAccess(models.Model, ModelToDictionary):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, models.DO_NOTHING)
    home = models.ForeignKey(Homes, models.DO_NOTHING)
    role = models.BooleanField(default=0)
    status = models.BooleanField(default=0)


    class Meta:
        managed = True
        db_table = 'home_user_access'

    def __str__(self):
        return self.id