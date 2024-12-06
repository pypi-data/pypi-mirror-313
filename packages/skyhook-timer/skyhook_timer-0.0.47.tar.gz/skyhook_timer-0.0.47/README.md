# skyhook-app
Alliance Auth (https://allianceauth.readthedocs.io/en/v4.4.2/index.html) plugin for tracking Skyhook timers

https://pypi.org/project/skyhook-timer/


## Installation

### 1 - Install app

Install into your Alliance Auth virtual environment from PyPI:

```bash
pip install skyhook-timer
```

### 2 - Configure AA settings

Add `'skyhook_timer'` to `INSTALLED_APPS`

### 3 - Finalize installation into AA

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for AA

### 4 - Setup permissions

Now you can access Alliance Auth and setup permissions for your users. See below

## Permissions

This is an overview of all permissions used by this app:

Name | Purpose | Code
-- | -- | --
Can add skyhook timer | Can create a unique skyhook timer with system/planet and time. If the system/planet timer exists already it overwrites | add_skyhooktimer
Can change skyhook timer | Edit existing skyhook timers | change_skyhooktimer
Can delete skyhook timer | Removes a skyhook timer from the list | delete_skyhooktimer
Can view skyhook timer | Allows viewing of the nav menu link, and rendering of the skyhook timer page. This should be added to all users/members/states/groups that should be able to view skyhook timers | view_skyhooktimer

# CHANGELOG

### 0.0.43
- Limited stable release
