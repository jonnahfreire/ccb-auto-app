from os import environ, path, sys

# --------------------------------------------------------------------
sysname: str = "ccb-autom"

syslocal_path: str = path.join("/home", environ["USER"])\
    if not sys.platform == "win32" else path.join(environ['USERPROFILE'])

syspath: str = path.join(syslocal_path, sysname)

config:            str = ".config" if not sys.platform == "win32" else "config"
dbpath:            str = path.join(syspath, config, "user.db")
logpath:           str = path.join(syspath, config, "logs.db")
notification_path: str = path.join(syspath, config, "notifications.db")
settings_path:     str = path.join(syspath, config, "settings.db")
