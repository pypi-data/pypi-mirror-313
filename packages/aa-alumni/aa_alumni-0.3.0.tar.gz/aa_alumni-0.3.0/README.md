# Alliance Auth - Alumni

## Features

- Integration with Alliance Auth's State System, creates and maintains an Alumni State for past members of an Alliance and/or Corporation.

## Installation

### Step 1 - Prepare Auth

Remove/Promote any state with a priority of `1`, Alumni is considered slightly better than the built in Guest State.

### Step 2 - Install from pip

```shell
pip install aa-alumni
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'alumni'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-Alumni
# Tasks
CELERYBEAT_SCHEDULE['alumni_run_alumni_check_all'] = {
    'task': 'alumni.tasks.run_alumni_check_all',
    'schedule': crontab(minute=37, hour=3, day_of_week=4),
}
CELERYBEAT_SCHEDULE['alumni_run_update_all_models'] = {
    'task': 'alumni.tasks.update_all_models',
    'schedule': crontab(minute=37, hour=3, day_of_week=3),
}
```

### Step 4 - Update AA's State system

```shell
python myauth/manage.py alumni_state
```

### Step 5 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 6 - Configure Further

In the Admin interface, visit `alumni > config > add` or `<AUTH-URL>/admin/alumni/config/add/`
Select the Alliances and/or Corporations for which characters with historical membership are Alumni

## Settings

| Name | Description | Default |
| --- | --- | --- |
|`ALUMNI_CHARACTERCORPORATION_RATELIMIT`| Celery Rate Limit _per worker_, 10 tasks * 10 Workers = 100 tasks/min | '10/m' |

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
