"""
Read LICENSE file
"""

import json
import os

class StorageDriver:

	def __init__(self):
		pass

	def get(self, key, keyspaces=None):
		raise NotImplementedError("You have to use an actual storage driver")

	def set(self, key, value, keyspaces=None):
		raise NotImplementedError("You have to use an actual storage driver")

	def save(self):
		raise NotImplementedError("You have to use an actual storage driver")

class JSONDriver(StorageDriver):
	def __init__(self, file):
		if not os.path.exists(file):
			print("The file '{}' does not exist, creating...".format(file))
			with open(file, 'w') as outfile:
				json.dump({}, outfile)

		if os.path.isdir(file):
			raise IsADirectoryError("The path '{}' is a directory, must be file".format(file))

		c = open(file).read()

		self.file = file
		self.values = json.loads(c)

	def set(self, key, value, keyspaces=[]):
		keyspaces = keyspaces[:]
		self.values = self._set(key, value, self.values, keyspaces)
	
	def _set(self, key, value, values, keyspaces=[]):
		if len(keyspaces) == 0:
			values[key] = value
			return values
		space = keyspaces.pop(0)
		if values:
			values[space] = self._set(key, value, values.get(space, None), keyspaces)
			return values
		else:
			return {space: self._set(key, value, None, keyspaces)}


	def get(self, key, keyspaces=[]):
		values = self.values
		if keyspaces == [] or keyspaces == None:
			if key in values:
				return values[key]
			return None
		for keyspace in keyspaces:
			if not keyspace in values:
				return
			values = values[keyspace]
		if key in values:
			return values[key]
		return None

	def save(self):
		with open(self.file, 'w') as f:
			json.dump(self.values, f, indent=4)