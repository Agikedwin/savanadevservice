from http.client import responses
from os import access

from django.shortcuts import render
from django.http import  HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

auth_url_discord ='https://discord.com/oauth2/authorize?client_id=1376833469547679835&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&scope=identify'
def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'msg': 'Hello login agik'})

@login_required(login_url='/oauth2/login')
def get_authenticated_user(request: HttpRequest):
    return JsonResponse({'msg':'Authenticated'})

def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)

def discord_login_redirect(request: HttpRequest):
    #Get the code
    code = request.GET.get('code')
    print(code)


    user = exchange_code(code)
    savana_discord_user = authenticate(request, user=user)
    print(savana_discord_user)
    if savana_discord_user is None:
        return JsonResponse({'error': 'Authentication failed'}, status=401)
    print(f'the savana auth user {savana_discord_user}')
    login(request,savana_discord_user)
    #return JsonResponse({"user": user})
    #check if user is authenticated
    #return redirect('/oauth2/user')
    #take me to graphql end points
    return redirect('/graphql')


def exchange_code(code: str):
    try:
        data = {
            'client_id':'1376833469547679835',
            'client_secret':'6sa0vJrlaR9rem8Y1_8qYG4w74EC5zWa',
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri':'http://localhost:8000/oauth2/login/redirect',
            #'redirect_uri': 'http://localhost:8000/api/oauth2/code/ql',
            'scope':'identify'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
        credentials = response.json()
        print(response.status_code)
        print(response.json())

        access_token = credentials['access_token']
        response = requests.get('https://discord.com/api/v6/users/@me', headers={
            'Authorization': 'Bearer %s' %access_token
        })
        print(response)
        user =response.json()
        print(user)
        return user

    except  Exception as e:
        print(e)

