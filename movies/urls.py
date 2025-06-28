from django.urls import path
from . import views

# Register the app namespace for URL reversing
app_name = 'movies'

urlpatterns=[
    path('',views.movie_list,name='movie_list'),
    path('<int:movie_id>/theaters',views.theater_list,name='theater_list'),
    path('theater/<int:theater_id>/seats/book/',views.book_Seats,name='book_seats'),
]