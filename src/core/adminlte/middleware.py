from django.utils import timezone
from src.main.models import DailyStats
from ..utils import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2


class TrafficCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.path.startswith('/admin') and not request.path.startswith('/static'):
            today = timezone.now().date()
            stats, created = DailyStats.objects.get_or_create(date=today)
            stats.sessions += 1
            stats.save()

            if request.user.is_authenticated and request.user.country == 'UA':
                ip = get_client_ip(request)

                if ip != '127.0.0.1':
                    try:
                        g = GeoIP2()
                        country_code = g.country_code(ip)

                        if country_code and country_code != request.user.country:
                            request.user.country = country_code
                            request.user.save()
                    except Exception as e:
                        pass

        response = self.get_response(request)
        return response