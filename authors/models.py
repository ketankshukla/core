from django.db import models
import uuid


# Create your models here.
class Author(models.Model):
    '''
    Book author class
    Managed only in django admin
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
