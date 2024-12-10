from django.db import models

class Booking(models.Model):
    room_id = models.IntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"Booking for Room {self.room_id}"
