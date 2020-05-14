#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from werkzeug import serving, wrappers
from flask import Flask, request, make_response, redirect
from flask_cors import CORS, cross_origin
from datetime import date, datetime
from classes.jwtAuth import JWTAuth
from classes.database import Database
from classes.utils import Utils
from classes.procedure import Procedure
from classes.error import Error
from classes.userOptions import get_ordered_options
from classes.userChannels import get_user_channels
from collections import OrderedDict
import ssl
import importlib
import sys
import copy
import hashlib
import simplejson as json

__sslCert = "/etc/ssl/certs/labs357.com.ar.crt"
__sslKey = "/etc/ssl/private/labs357.key"
__jwtPrivateKey = r"D:\eniac\LABS357 Dashboard\API Labs\API\v1\keys\private.key"
__jwtPublicKey = r"D:\eniac\LABS357 Dashboard\API Labs\API\v1\keys\public.key"
__appPort = 5006
__appHostname = "0.0.0.0"
__dbName = "dev_plataforma"
__dbHost = "127.0.0.1"
__dbUser = "root"
__dbPswd = ""

app = Flask(__name__)
CORS(app)

@app.route('/auth', methods=['POST'])
def auth():
	error = None
	response = None
	try:
		#Revisa que el body de la petición sea un json válido
		validJsonData = Utils.validateRequestJsonData(request)
		if validJsonData == True:
			jsonData = request.get_json()

			#Revisa que en el json esten los argumentos necesarios. En este caso, user y password
			validateArguments = Utils.allPostArgumentsExists(jsonData, ["username", "password"])
			if validateArguments[0] == True:
				#Crea instancia de DB, arma tupla de argumentos y llama al SP correspondiente
				DATABASE = Database.getInstance(__dbHost,__dbUser,__dbPswd,__dbName)
				username = jsonData["username"]
				password = jsonData["password"]
				args = (username, password, 0,)
				res = DATABASE.callProc(Procedure.GET_USER_API, args, False)

				#Si res es NONE, no trajo resultados el SP	
				if res is None:
					error = Error.INVALID_USER
				else:
					#Si el usuario existe, genera el token
					auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)

					#1: Cantidad de días de vigencia del token
					#user-api-: SUBJECT del token, meramente informativo. Podemos usar el id del usuario y que es de la api
					userId = res["id"]
					token = auth.encodeToken(1, 'user-api-' + str(userId))
					if token is not None:
						response = OrderedDict([
							("token", token["token"]),
							("expires", token["expires"].isoformat())
						])
					else:
						error = Error.TOKEN_GENERATION_ERROR
			else:
				#Si hay que modificar algo del mensaje, se hace un deepcopy, no modificamos directamente la variable porque es estatica
				error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
				error["errmsg"] = error["errmsg"].format(validateArguments[1])
		else:
			error = Error.INVALID_REQUEST_BODY
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR
	
	return wrappers.Response(
		json.dumps(response if error is None else error), 200, mimetype='application/json'
	)

@app.route('/auth2', methods=['GET'])
def auth2():
	error = None
	response = None
	try:
		#Revisa que esten los argumentos necesarios en la peticion. En este caso, user y password
		validateArguments = Utils.allGetArgumentsExists(request, ["username", "password"])
		if validateArguments[0] == True:
			#Crea instancia de DB, arma tupla de argumentos y llama al SP correspondiente
			DATABASE = Database.getInstance(__dbHost,__dbUser,__dbPswd,__dbName)
			username = request.args.get("username")
			password = request.args.get("password")
			args = (username, password, 0,)
			res = DATABASE.callProc(Procedure.GET_USER_API, args, False)

			#Si res es NONE, no trajo resultados el SP	
			if res is None:
				error = Error.INVALID_USER
			else:
				#Si el usuario existe, genera el token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)

				#1: Cantidad de días de vigencia del token
				#user-api-: SUBJECT del token, meramente informativo. Podemos usar el id del usuario y que es de la api
				userId = res["id"]
				token = auth.encodeToken(1, 'user-api-' + str(userId))
				if token is not None:
					response = OrderedDict([
						("token", token["token"]),
						("expires", token["expires"].isoformat())
					])
				else:
					error = Error.TOKEN_GENERATION_ERROR
		else:
			error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
			error["errmsg"] = error["errmsg"].format(validateArguments[1])
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR
	
	return wrappers.Response(
		json.dumps(response if error is None else error), 200, mimetype='application/json'
	)

@app.route('/test')
def test():
	error = None
	response = None
	
	try:
		#Revisamos si el token viene en el header de la peticion
		token = Utils.getTokenFromHeader(request)
		if token is not None:
			#Si esta, lo decodificamos
			auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
			decodedToken = auth.decodeToken(token)
			
			if "errno" not in decodedToken:
				response = decodedToken
			else:
				error = decodedToken
		else:
			error = Error.TOKEN_NOT_FOUND	
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR

	return wrappers.Response(
		json.dumps(response if error is None else error), 200, mimetype='application/json'
	)

@app.route('/login', methods=['POST'])
def login():
	# Variables locales
	error = None
	response = None
	email = None
	password = None

	try:
		# Revisar formato JSON válido
		valid_json_data = Utils.validateRequestJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.allPostArgumentsExists(
						json_data, 
						['email', 'password']
					)
					if validate_arguments[0]:
						# Crear db, tupla de args y llamada a SP
						db = Database.getInstance(
							__dbHost, 
							__dbUser, 
							__dbPswd, 
							__dbName
						)
						email = json_data['email']
						password = json_data['password']
						args = (email, password)
						user_results = db.callProc(
							Procedure.GET_USER_PLATFORM, 
							args, 
							True
						)  # Obtención de usuario
						print(user_results)
						# Revisar que el usuario existe
						if user_results is not None:
							response = OrderedDict([
								('id', user_results[0]['id']),
								('id_cliente', user_results[0]['id_cliente']),
								('nombre', user_results[0]['nombre']),
								('email', user_results[0]['email']),
								('canales', get_user_channels(user_results))
							])
						else:
							# Usuario inválido
							error = Error.INVALID_USER
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = error['errmsg'].format(
							validate_arguments[1]
						)
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
		else:
			# Formato JSON inválido
			error = Error.INVALID_REQUEST_BODY
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR
	
	return wrappers.Response(
		json.dumps(response if error is None else error), 
		200, 
		mimetype='application/json'
	)

@app.route('/profile', methods=['POST'])
def profile():
	# Variables locales
	error = None
	response = None
	id_client = None
	id_user = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.validateRequestJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.allPostArgumentsExists(
						json_data,
						['id_user', 'id_client']
					)
					if validate_arguments[0]:
						# Crear db, tupla de args y llamada a SP
						db = Database.getInstance(
							__dbHost, 
							__dbUser, 
							__dbPswd, 
							__dbName
						)
						id_user = json_data['id_user']
						id_client = json_data['id_client']
						args = (id_user, id_client)
						user_opt = db.callProc(
							Procedure.GET_USER_MENU_OPTIONS,
							args,
							True
						)  # Obtención de opciones

						# Revisar que el usuario existe
						if user_opt is not None:
							response = get_ordered_options(user_opt)
						else:
							# Usuario inválido
							error = Error.INVALID_USER
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = error['errmsg'].format(
							validate_arguments[1]
						)					
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
		else:
			# Formato JSON inválido
			error = Error.INVALID_REQUEST_BODY
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR

	return wrappers.Response(
		json.dumps(response if error is None else error),
		200,
		mimetype='application/json'
	)

if __name__ == '__main__':
	try:
		importlib.reload(sys)

		#"""
		#EN PRODUCCION, CON LOS CERTIFICADOS CORRESPONDIENTES
		#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		#context.load_cert_chain(__sslCert, __sslKey)
		#serving.run_simple(__appHostname, __appPort, app, threaded=True, ssl_context=context)
		#"""

		#DESARROLLO
		serving.run_simple(__appHostname, __appPort, app)
	except:
		Utils.setLog()
