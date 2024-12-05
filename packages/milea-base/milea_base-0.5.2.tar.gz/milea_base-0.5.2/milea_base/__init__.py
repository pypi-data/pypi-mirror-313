from django.conf import settings as core

MILEA_VARS = {}

for app in core.MILEA_APPS:
    try:
        settings_module = __import__(f"{app}.settings", fromlist=["*"])
    except ImportError:
        raise Exception(f"Error while importing configuration for app {app}: settings.py not found.")
    else:
        vars = {key: getattr(settings_module, key) for key in dir(settings_module) if not key.startswith('__')}
        MILEA_VARS[app] = vars

for app, value in MILEA_VARS.items():
    try:
        vars = core.MILEA_VARS[app]
        for key, val in vars.items():
            if key in MILEA_VARS[app]:
                MILEA_VARS[app][key] = val
    except Exception:
        pass
