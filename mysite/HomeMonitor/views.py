from django.http import HttpResponse
from django.shortcuts import render
import requests
import getpass
import json



def checkStatusCode(status_code, Url):
	if status_code == 200 or status_code == 201:
		return
	else:
		print("Call to URL {0} failed with status code {1}".format(Url,status_code))
		print("Exiting")
		exit(1)


def getDeviceHeader():

	global deviceHeader
	
	authHeaders = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

	userName = input("Concert username[iotpadminuser] ") or "iotpadminuser"
	password = "P@55w0rd"

	authUrl = 'https://sso.pool4.iotpdev.com/auth/realms/authenticate/protocol/openid-connect/token'

	try:
		print("authURL: {0}".format(authUrl))
	
		response = requests.post(authUrl,
	                             headers = authHeaders, 
	                             data = {"client_id" : "postman", 
	                                     "username" : userName, 
	                                     "password" : password, 
	                                     "grant_type" : "password"
								        }
	                        )
		checkStatusCode(response.status_code,authUrl)         
		print (response)
	
	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)
	except requests.exceptions.RequestException as e:
		print("Response Exception Raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)

	deviceHeader = {"Authorization" : "Bearer " + response.json()['access_token'], 
					"Content-Type" : "application/json"}



def tempRequest():
	req = requests.get('https://api.pool4.iotpdev.com/api/1/devices/69dc93d6-7f9d-4926-a27c-7ce6b6e73923/snapshot?withValues=true', headers = deviceHeader)
	req_json = json.loads(req.text)
	
	text_value = req_json['sensors'][1]['value']
	return text_value
	
	
def humRequest(): 
	req = requests.get('https://api.pool4.iotpdev.com/api/1/devices/69dc93d6-7f9d-4926-a27c-7ce6b6e73923/snapshot?withValues=true', headers = deviceHeader)
	req_json = json.loads(req.text)
	
	text_value = req_json['sensors'][0]['value']
	return text_value


def lightRequest(): 
	req = requests.get('https://api.pool4.iotpdev.com/api/1/devices/69dc93d6-7f9d-4926-a27c-7ce6b6e73923/snapshot?withValues=true', headers = deviceHeader)
	req_json = json.loads(req.text)
	
	text_value = req_json['sensors'][0]['value']
	return text_value

def main():

	getDeviceHeader()
	
	# Request goes here!
	tempRequest()
	humRequest()
	lightRequest()
	
	
main()

def index(request):	
		return HttpResponse(render(request, 'index.html', {'temp_reading': tempRequest, 'light_reading': lightRequest, 'hum_reading': humRequest }))
 

	
    
