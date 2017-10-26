"""
Read LICENSE file
"""

from .storage import JSONDriver
import os

DEFAULTS = {
	"token": "Insert Token Here",
	"command_prefix": "!",
	"questions": [
		{
			"question": "What is your server ID?",
			"embed_title": "Server ID"
		},{
			"question": "What is your server name?",
			"embed_title": "Server Name"
		}
	],
	"output": 0
}

def initConfig():
	dirs = [ "data" ]
	for dirr in dirs:
		if not os.path.exists(dirr):
			print("DIRECTORY '{}' DOESN'T EXIST. CREATING...".format(dirr))
			os.mkdir(dirr)
	storage = JSONDriver("data/config.json")
	for key, value in DEFAULTS.items():
		if not storage.get(key):
			print("ADDING DEFAULT KEY `{}` TO THE CONFIG.JSON FILE".format(key))
			storage.set(key, value)

	storage.save()
	return storage