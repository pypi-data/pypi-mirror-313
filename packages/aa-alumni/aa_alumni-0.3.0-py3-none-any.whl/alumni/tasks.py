import datetime
from random import randint

from bravado.exception import HTTPClientError, HTTPInternalServerError
from celery import shared_task

from django.db import IntegrityError

from allianceauth.authentication.models import State
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

from .app_settings import (
    ALUMNI_CHARACTERCORPORATION_RATELIMIT, ALUMNI_STATE_NAME,
    ALUMNI_TASK_JITTER, ALUMNI_TASK_PRIORITY,
)
from .models import (
    AlumniSetup, CharacterCorporationHistory, CorporationAllianceHistory,
)
from .providers import (
    get_characters_character_id_corporationhistory,
    get_corporations_corporation_id_alliancehistory,
)

logger = get_extension_logger(__name__)


@shared_task
def run_alumni_check_all():
    for character in EveCharacter.objects.all().values('character_id'):
        alumni_check_character.apply_async(
            args=[character['character_id']],
            priority=ALUMNI_TASK_PRIORITY
        )


@shared_task
def alumni_check_character(character_id: int) -> bool:
    """Check/Update a characters alumni status using the historical models

    Parameters
    ----------
    character_id: int
        Should match an existing EveCharacter model

    Returns
    -------
    bool
        Whether the user is an alumni or not **it is updated in this function as well**"""

    alumni_setup = AlumniSetup.objects.first()
    alumni_state = State.objects.get(name=ALUMNI_STATE_NAME)
    character = EveCharacter.objects.get(character_id=character_id)
    if character.corporation_id in alumni_setup.alumni_corporations.values_list('corporation_id', flat=True):
        # Cheapo cop-out to end early
        alumni_state.member_characters.add(character)
        return True

    if character.alliance_id in alumni_setup.alumni_alliances.values_list('alliance_id', flat=True):
        # Cheapo cop-out to end early
        alumni_state.member_characters.add(character)
        return True

    char_corp_history = CharacterCorporationHistory.objects.filter(
        character=character)

    for char_corp in char_corp_history:
        # print(alumni_setup.alumni_corporations.values_list('corporation_id', flat=True))
        if char_corp.corporation_id in alumni_setup.alumni_corporations.values_list('corporation_id', flat=True):
            # Cheapo cop-out to end early
            alumni_state.member_characters.add(character)
            return True

    for alliance in alumni_setup.alumni_alliances.all():
        if char_alliance_datecompare(alliance_id=alliance.alliance_id, character_id=character_id):
            alumni_state.member_characters.add(character)
            return True

    # If we reach this point, we aren't an alumni
    alumni_state.member_characters.remove(character)
    return False


def char_alliance_datecompare(alliance_id: int, character_id: int) -> bool:
    """Voodoo relating to checking start dates and _next_ start dates

    Necessary to determine if a character was a member of a corp
    WHILE it was in an alliance

    Parameters
    ----------
    alliance_id: int
        Should match an existing EveAllianceInfo model

    character_id: int
        Should match an existing EveCharacter model

    Returns
    -------
    bool
        Whether True"""

    character = EveCharacter.objects.get(character_id=character_id)
    char_corp_history = CharacterCorporationHistory.objects.filter(
        character=character).order_by('record_id')

    for index, char_corp_record in enumerate(char_corp_history):
        # Corp Joins Alliance, Between Char Join/Leave Corp
        try:
            filter_end_date = char_corp_history[index + 1].start_date
        except IndexError:
            filter_end_date = datetime.datetime.now()

        if CorporationAllianceHistory.objects.filter(
            corporation_id=char_corp_record.corporation_id,
            alliance_id=alliance_id,
            start_date__range=(
                char_corp_record.start_date,
                filter_end_date)).exists() is True:
            return True

        corp_alliance_history = CorporationAllianceHistory.objects.filter(
            corporation_id=char_corp_record.corporation_id).order_by('record_id')

        for index_2, corp_alliance_record in enumerate(corp_alliance_history):
            # Needs to be unfiltered alliance id because we need _next_ start date
            # but check if the alliance id matches before we run any logic
            try:
                if corp_alliance_record.alliance_id == alliance_id:
                    # Char Joins Corp, Between Corp Join/Leave
                    if corp_alliance_record.start_date < char_corp_record.start_date < corp_alliance_history[index_2 + 1].start_date:
                        return True
                    # Char Leaves Corp, Between Corp Join/Leave
                    elif corp_alliance_record.start_date < char_corp_history[index + 1].start_date < corp_alliance_history[index_2 + 1].start_date:
                        return True
                    # Corp Leaves Alliance in between Char Join/Leave Corp
                    elif char_corp_record.start_date < corp_alliance_history[index_2 + 1].start_date < char_corp_history[index + 1].start_date:
                        return True
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                # Need to actually add some IndexError handling to above tasks, but lets log this gracefully so as not to cactus up the whole thing.
                logger.exception(e)
    return False


@shared_task
def update_all_models():
    """Update All CharacterCorporation history models from ESI"""

    for character in EveCharacter.objects.all().values('character_id'):
        update_charactercorporationhistory.apply_async(
            args=[character['character_id']],
            priority=ALUMNI_TASK_PRIORITY,
            countdown=randint(1, ALUMNI_TASK_JITTER)
        )

    # Once all charactercorporations are updated/exist.
    # then initiate the corporationalliance updates
    update_all_models_followup.apply_async(priority=ALUMNI_TASK_PRIORITY)


@shared_task
def update_all_models_followup():
    """Update All CorporationAlliance history models from ESI"""

    for char_corp_record in CharacterCorporationHistory.objects.values('corporation_id').distinct():
        update_corporationalliancehistory.apply_async(
            args=[char_corp_record['corporation_id']],
            priority=ALUMNI_TASK_PRIORITY,
            countdown=randint(1, ALUMNI_TASK_JITTER)
        )


@shared_task(bind=True, rate_limit=ALUMNI_CHARACTERCORPORATION_RATELIMIT)
def update_corporationalliancehistory(self, corporation_id: int):
    """Update CorporationAllianceHistory models from ESI

    Parameters
    ----------
    corporation_id: int """

    for dat in get_corporations_corporation_id_alliancehistory(corporation_id):
        try:
            if dat['is_deleted'] == 'true':
                deleted = True
            else:
                deleted = False
            CorporationAllianceHistory.objects.create(
                corporation_id=corporation_id,
                alliance_id=dat['alliance_id'],
                is_deleted=deleted,
                record_id=dat['record_id'],
                start_date=dat['start_date'],
            )
        except IntegrityError:
            # This already exists, move on
            pass
        except HTTPClientError as e:  # 429?
            raise self.retry(exc=e, countdown=61)
        except HTTPInternalServerError as e:  # Custom timeouts are defined as a 500 on this endpoint
            raise self.retry(exc=e, countdown=61)
        except Exception as e:
            logger.exception(e)


@shared_task(bind=True, rate_limit=ALUMNI_CHARACTERCORPORATION_RATELIMIT)
def update_charactercorporationhistory(self, character_id: int) -> None:
    """Update CharacterCorporationHistory models from ESI

    Parameters
    ----------
    character_id: int
        Should match an existing EveCharacter model"""

    try:
        character = EveCharacter.objects.get(character_id=character_id)
    except Exception as e:
        logger.exception(e)
        return

    for dat in get_characters_character_id_corporationhistory(character_id):
        try:
            if dat['is_deleted'] == 'true':
                deleted = True
            else:
                deleted = False
            CharacterCorporationHistory.objects.create(
                character=character,
                corporation_id=dat['corporation_id'],
                is_deleted=deleted,
                record_id=dat['record_id'],
                start_date=dat['start_date'],
            )
        except IntegrityError:
            # This already exists, move on
            pass
        except HTTPClientError as e:  # 429?
            raise self.retry(exc=e, countdown=61)
        except HTTPInternalServerError as e:  # Custom timeouts are defined as a 500 on this endpoint
            raise self.retry(exc=e, countdown=61)
        except Exception as e:
            logger.exception(e)
