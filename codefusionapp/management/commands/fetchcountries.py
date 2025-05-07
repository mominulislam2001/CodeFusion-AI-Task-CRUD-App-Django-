from django.core.management.base import BaseCommand
import requests
from codefusionapp.models import Country

URL = "https://restcountries.com/v3.1/all"

class Command(BaseCommand):
    help = "Fetches country data from restcountries.com and stores/updates DB."

    def handle(self, *args, **options):
        resp = requests.get(URL, timeout=60)
        resp.raise_for_status()
        created = updated = 0

        for item in resp.json():
            obj, is_created = Country.objects.update_or_create(
                cca2=item.get('cca2', ''),
                defaults={
                    'name': item['name']['common'],
                    'capital': item.get('capital', [''])[0] if item.get('capital') else '',
                    'population': item.get('population', 0),
                    'region': item.get('region', ''),
                    'timezones': item.get('timezones', []),
                    'flag': item.get('flags', {}).get('png', ''),
                    'languages': item.get('languages', {}),
                }
            )
            created += is_created
            if not is_created:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Created: {created}, Updated: {updated}'))
