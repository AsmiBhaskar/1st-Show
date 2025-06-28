from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movie=Movie.objects.filter(name__icontains=search_query)
    else:
        movie=Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movie})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'theaters': theaters, 'movie': movie})

@login_required(login_url='/login/')
def book_Seats(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theaters)
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        error_seats = []
        if not selected_Seats:
            return render(request, "movies/seat_selection.html", {'theater': theaters, 'seats': seats, 'error': 'Please select at least one seat.', 'current_price': theaters.dynamic_price()})
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat, id=seat_id, theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                    )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats: 
            error_message = f"The following seats are already booked:{', '.join(error_seats)}"
            return render(request, "movies/seat_selection.html", {'theater': theaters, 'seats': seats, 'error': "no seat selected", 'current_price': theaters.dynamic_price()})
        return redirect('users:profile')
    return render(request, 'movies/seat_selection.html',{'theater': theaters, 'seats': seats, 'current_price': theaters.dynamic_price()})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def show_timetable(request):
    from .models import Theater
    shows = Theater.objects.select_related('movie').all().order_by('time')
    # Precompute available and total seats for template
    for show in shows:
        show.available_seats = show.seats.filter(is_booked=False).count()
        show.total_seats = show.seats.count()
    return render(request, 'movies/show_timetable.html', {'shows': shows})