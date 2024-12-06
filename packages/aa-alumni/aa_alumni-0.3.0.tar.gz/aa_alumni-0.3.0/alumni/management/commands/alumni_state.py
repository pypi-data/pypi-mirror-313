from django.core.management.base import BaseCommand

from allianceauth.authentication.models import State

from alumni import app_settings


class Command(BaseCommand):
    help = 'Setup/Reset/Fix the Alumni State for the Alumni Module'

    def handle(self, *args, **options):
        self.stdout.write("Creating/Reseting/Fixing the Alumni State for the Alumni Module")
        alumni_name = app_settings.ALUMNI_STATE_NAME
        priority = 1

        created = State.objects.update_or_create(
            name=alumni_name,
            defaults={
                "priority": priority, }
        )
        if created:
            self.stdout.write("Success! Created Alumni State")
        else:
            self.stdout.write("Success! Updated Alumni State")
