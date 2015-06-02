# C3data version 1.0.0
#
# Abstract data class for CEOS tableau calculations
# Contains measurement data in a dictionary and the associated date in a string
# 
# Initializes with a string or list
# Exposes: getData() and getDate()

class C3data:

	__paramsList = ('Date', 'C1', 'A1', 'A2', 'B2', 'C3', 'A3', 'S3', 'A4', 'D4', 'B4', 'C5', 'A5') # Params to search for

	def __init__(self, measurements = ''):
		self.__data = {}
		self.__date = ''
		if measurements:
			if isinstance(measurements, str):
				self.__loadData(measurements.split('\n'))
			elif isinstance(measurements, list):
				self.__loadData(measurements)
			else:
				raise TypeError('A string or a list of strings is required')
			

	# __loadData(data)
	#
	# @api: private
	# @params: data{list}
	# 
	# load data into the __data dictionary and __date str
	def __loadData(self, data):
		lineBuffer = []
		

		for item in data:
			for val in self.__paramsList:

				# if the __paramsList item exists (followed by a ':'') and is not preceded by a '#''
				# parse out the pieces we want
				if item.find(val + ":") != -1 and item.find("#") == -1:
					item = item[item.find(val):]
					lineBuffer = item.split(":")

					# Different handling if the param is a date vs. a abberation value
					if lineBuffer[0] == "Date":

						# If the first value for the line list is 'Date', build a proper date for the second value
						self.__date = str(lineBuffer[1] + ':' + lineBuffer[2] + ':' + lineBuffer[3]).strip()
					else:
						measurements = []
						values = {}
						# All non date items should be of the following structure:
						# ['C1', ' -6.835nm             (95%: 1.61nm)']
						# ['A1', '  12.26nm /  +21.2deg (95%', '  4.3nm)']
						# Strip any whitespace on the second item, split it on spaces, and take
						# the first element (ex. -6.835nm)
						measurements = lineBuffer[1].split("/")
						if len(measurements) > 1:
							values['angle'] = measurements[1].strip().split(" ")[0]

						values['measurement'] = self.__normalize(measurements[0].strip())
						
						#lineBuffer[1] = self.__normalize(lineBuffer[1].strip().split(" ")[0])
						self.__data[val] = values

	# __normalize
	#
	# @api: private
	# @params: value{str}
	#
	# normalize data to mm
	def __normalize(self, value):
		factors = {'mm': 1, 'um': 0.001, 'nm': 0.000001, 'pm': 0.000000001}

		# check for one of the keys in the data
		for key in factors.keys():
			if key in value:
				value = value.split(key)[0]
				return str(float(value) * factors[key])



	# getData
	#
	# @api: public
	# 
	# getter for the __data dictionary
	def getData(self):
		return self.__data

	# getDate
	#
	# @api: public
	# 
	# getter for the __date str
	def getDate(self):
		return self.__date

	# def toString(self, delimitor = ' '):
	# 	#print some string representation of the data object using the specified delimitor
	# 	return ''