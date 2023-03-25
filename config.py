import configparser
import os, sys, codecs

if getattr(sys, 'frozen', False):
	application_path = os.path.dirname(sys.executable)
elif __file__:
	application_path = os.path.dirname(__file__)

config = configparser.ConfigParser()

config.read_file(codecs.open(str(application_path) + '/config.ini', "r", "utf8"))

discordtoken = os.environ.get("BOT_TOKEN") or config['SETTINGS']['discordtoken'].strip()
channel_id = os.environ.get("CHANNEL_ID") or config['SETTINGS']['channel_id'].strip()

