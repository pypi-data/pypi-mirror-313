import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from allianceauth.eveonline.models import EveCharacter

from alumni.models import AlumniSetup
from alumni.tasks import alumni_check_character, run_alumni_check_all

from .app_settings import ALUMNI_TASK_PRIORITY

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AlumniSetup)
def alumni_was_updated(sender, instance: AlumniSetup, *args, **kwargs):
    run_alumni_check_all.apply_async(priority=ALUMNI_TASK_PRIORITY)


@receiver(post_save, sender=EveCharacter)
def character_added(sender, instance: EveCharacter, created, *args, **kwargs):
    if created is True:
        alumni_check_character.apply_async(args=[instance.character_id], priority=ALUMNI_TASK_PRIORITY - 1)
