from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Room(models.Model):
    categories = (('standard', 'Standard'),
                  ('vip', 'VIP'),
                  ('presi', 'Presidentiel'))

    type = models.CharField(choices=categories, max_length=20)
    beds = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return f'Room: {self.type}'

class Reservation(models.Model):
    entry_date = models.DateField()
    exit_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reservation of {self.user} for {self.room}'
