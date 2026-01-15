from django.core.management.base import BaseCommand

from src.cms.models import Contacts
from src.main.models import Page, MainPage
from datetime import timedelta



class Command(BaseCommand):

    def handle(self, *args, **options):

        main_page = MainPage.load()
        contacts = Contacts.load()

        mandatory_pages = [
            "Про кінотеатр",
            "Кафе - Бар",
            "Vip - зал",
            "Реклама",
            "Дитяча кімната",
        ]

        for title in mandatory_pages:
            page, created = Page.objects.get_or_create(
                title=title,
                defaults={
                    'description': 'Текст за замовчуванням...',
                    'is_active': True,
                    'is_removable': False
                }
            )

            if not created and page.is_removable:
                page.is_removable = False
                page.save()

