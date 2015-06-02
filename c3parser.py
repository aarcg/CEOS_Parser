# C3parser version 1.0.0
#
# Static class to parse CEOS log files into sections, get c3data from each section,
# manage the data, and build representations of the data
# 
# Initializes with a required filename and an optional split delimitor
# Exposes: getTotalItems() and toString()

from c3data import C3data

class C3parser:

	# Private class variables
	__params = ['Date', 'C1', 'A1', 'A2', 'B2', 'C3', 'A3', 'S3', 'A4', 'D4', 'B4', 'C5', 'A5']
	__factors = {'mm': 1, 'um': 0.001, 'nm': 0.000001, 'pm': 0.000000001}
	__defaultPostfix = {
		'C1': 'nm',
		'A1': 'nm',
		'A2': 'nm',
		'B2': 'nm',
		'C3': 'nm',
		'A3': 'nm',
		'S3': 'nm',
		'A4': 'um',
		'D4': 'um',
		'B4': 'um',
		'C5': 'mm',
		'A5': 'um'
	}

	def __init__(self, fileString, splitOn='Accept Aberr'):

		self.__logfile = fileString
		self.__data = []
		self.__splitOn = splitOn

		self.__parse(self.__logfile)

	def __parse(self, logString):
		# split on the desired delimitor
		logList = logString.split(self.__splitOn)

		# print loglist

		# for each item in the new list, split again on 'Tab pressed'
		# Don't use the last item since it is after the deliminated split
		# and won't contain any usable data
		for i in range(0, len(logList) - 1):
			temp = logList[i].split('Tab pressed')
			# take the last item in the list
			# print 'appending: ' + str(temp[-1])
			self.__data.append(C3data(temp[-1]))

	# __scaleParam
	#
	# @api private
	# @params param{'str'}, value{'str'}
	#
	# Scale measurements from mm to the default value for the parameter
	def __scaleParam(self, param, value):
		defaultPostfix = self.__defaultPostfix[param]
		scaleFactor = self.__factors[defaultPostfix]
		return float(value) / scaleFactor

	def getTotalItems(self):
		return len(self.__data)

	def toString(self, delimitor='\t'):
		# Construct the header string
		header = list(self.__params)
		for i in range(0, len(header)):
			if header[i] in self.__defaultPostfix.keys():
				header[i] += '(' + self.__defaultPostfix[header[i]] + ')'
		outStr = delimitor.join(header) + '\n'

		# Construct the data string
		for item in self.__data:
			data = item.getData()
			outStr += item.getDate() + delimitor
			for i in range(1, len(self.__params)):
				param = self.__params[i]

				if param in data:
					measurement = data[self.__params[i]]['measurement']
					outStr += str(self.__scaleParam(param, measurement))
				else:
					outStr += '0'

				# Only add delimitor if not the last item
				if i < len(self.__params) - 1:
						outStr += delimitor

			outStr += '\n'

		return outStr

