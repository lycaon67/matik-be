from django.db import models
from homes.models import Homes
from homes.models import Rooms
import uuid
from django.utils.translation import gettext_lazy as _
from core.util.model_to_dict import ModelToDictionary
# Create your models here.

class Devices(models.Model, ModelToDictionary):
    
    id = models.AutoField(primary_key=True, editable=False)
    key = models.CharField(max_length=100, null=False, unique=True)
    type = models.CharField(max_length=100, null=True)
    home = models.ForeignKey(Homes, models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'devices'
            

    def __str__(self):
        return self.id
    
class Channels(models.Model, ModelToDictionary):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100, null=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING)
    type = models.IntegerField(default=0)
    room = models.ForeignKey(Rooms, models.DO_NOTHING, null=True)
    status = models.CharField(max_length=1024, null=True)

    class Meta:
        managed = True
        db_table = 'channels'
            

    def __str__(self):
        return self.id