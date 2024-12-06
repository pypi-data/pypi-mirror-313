# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2023 51 Degrees Mobile Experts Limited, Davidson House,
# Forbury Square, Reading, Berkshire, United Kingdom RG1 3EU.
#
# This Original Work is licensed under the European Union Public Licence
# (EUPL) v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
#
# If using the Work as, or as part of, a network application, by
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading,
# such notice(s) shall fulfill the requirements of that article.
# *********************************************************************


import base64
import os
import array

class KeyUtils():

	# Obtain a key either from environment variable or from a property.
	# Try resource key as env var, then as upper case env var, the system property
	@staticmethod
	def get_named_key(key_name):
		value = KeyUtils.__get_env_variable(key_name)
		if (value == None):
			value = KeyUtils.__get_env_variable(key_name.upper())
		return value

	# Evaluate whether a key might be valid
	@staticmethod
	def is_invalid_key(key_value):
		try:
			value_bytes = str.encode(key_value + "=" * (-len(key_value) % 4), "utf8")
			decoded_bytes = bytearray(base64.urlsafe_b64decode(value_bytes))
			decoded = decoded_bytes.decode('ascii', 'replace')
			return key_value == None or \
				len(key_value.strip()) < 19 or \
				len(decoded) < 14
		except:
			return True

	@staticmethod
	def __get_env_variable(name):
		if name in os.environ:
			return os.environ[name]
		else:
			return ""
