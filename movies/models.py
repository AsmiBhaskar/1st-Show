from django.db import models
from django.contrib.auth.models import User 


class Movie(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/", blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)  # optional
    trailer_url = models.URLField(blank=True, null=True, help_text="YouTube trailer URL")

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=6, decimal_places=2, default=200.00)

    def dynamic_price(self):
        from django.utils import timezone
        import math
        total_seats = self.seats.count()
        booked_seats = self.seats.filter(is_booked=True).count()
        remaining_seats = total_seats - booked_seats
        # Price increases as seats fill up (up to 50% more)
        if total_seats > 0:
            seat_factor = 1 + 0.5 * (1 - remaining_seats / total_seats)
        else:
            seat_factor = 1
        # Price increases as showtime approaches (up to 30% more if <2h left)
        hours_to_show = (self.time - timezone.now()).total_seconds() / 3600
        if hours_to_show < 2:
            time_factor = 1.3
        elif hours_to_show < 6:
            time_factor = 1.15
        else:
            time_factor = 1
        price = float(self.base_price) * seat_factor * time_factor
        return round(price, 2)

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Booking by{self.user.username} for {self.seat.seat_number} at {self.theater.name}'