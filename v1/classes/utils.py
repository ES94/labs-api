#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import sys
import traceback
import inspect
from datetime import date, datetime
import simplejson as json

class Utils:
	__errorLogPath = r"D:\eniac\LABS357 Dashboard\API Labs\API\v1\logs\error.log"

	@staticmethod
	def setLog():
		try:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]
			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(Utils.__errorLogPath, "a") as logFile:
				logFile.write(stringError)
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]  
			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(Utils.__errorLogPath, "a") as logFile:
				logFile.write(stringError)

	@staticmethod
	def validateRequestJsonData(request):
		"""
		Validate if the request body has a valid json
		Param: request -> HTTP request
		Return <True|False>
		"""
		if request.data:
			if request.is_json:
				try:
					jsonData = json.loads(request.data)
					return True
				except:
					return False
			else:
				return False
		else:
			return False

	@staticmethod
	def allPostArgumentsExists(dict, args):
		"""
		Check if arguments are in dict
		Param: dict -> Object where args must be present
		Param: args -> Args to find in the dict object
		Return: [<True|False>, <Error message>]
		"""
		invalidArgs = []
		for a in args:
			if a not in dict:
				invalidArgs.append(a)

		if (len(invalidArgs) > 0):
			return [
				False,
				", ".join(invalidArgs)
			]
		else:
			return [True]

	@staticmethod
	def allGetArgumentsExists(request, args):
		"""
		Check if arguments are in dict
		Param: request -> HTTP request
		Param: args -> Args to find in the dict object
		Return: [<True|False>, <Error message>]
		"""
		invalidArgs = []
		for a in args:
			if request.args.get(a) is None:
				invalidArgs.append(a)

		if (len(invalidArgs) > 0):
			return [
				False,
				", ".join(invalidArgs)
			]
		else:
			return [True]

	@staticmethod
	def getTokenFromHeader(request):
		"""
		Get token from the request header
		Param: request -> HTTP request
		Return: <token>
		"""		
		if "Authorization" in request.headers:
			authHeader = request.headers.get("Authorization")
			if authHeader:
				token = authHeader.split(" ")[1]
				return token
		
		return None
