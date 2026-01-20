from django.core.management.base import BaseCommand
from src.main.models import Movie, Hall, Schedule
from datetime import timedelta, time, datetime
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):

        halls = Hall.objects.all()
        movies = Movie.objects.all()

        for hall in halls:
            for movie in movies:

                start_date = movie.date_of_show
                end_date = movie.date_of_end_show

                if not start_date or not end_date:
                    continue

                delta = end_date - start_date

                for i in range(delta.days + 1):
                    day = start_date + timedelta(days=i)

                    schedule_datetime = timezone.make_aware(datetime.combine(day, time(10,0)))

                    schedule, created = Schedule.objects.get_or_create(
                        id_hall=hall,
                        id_movie=movie,
                        id_cinema=hall.id_cinema,
                        date=schedule_datetime,
                        defaults={'price': 50}
                    )






