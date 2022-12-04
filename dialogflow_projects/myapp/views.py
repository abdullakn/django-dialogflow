
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .country import country_info

# Create your views here.


def sample_view(request):
    return HttpResponse("success")

def new_sample(request):
    return HttpResponse("done")



@csrf_exempt
def dialogflow_webhook(request):
    if request.method=='GET':
        print("get method")
        return render(request,'chatbotpage.html')
    if (request.method == 'POST'):
        

        print('Received a post request')

        body_unicode = request.body.decode('utf-8')
        req = json.loads(body_unicode)

        action = req.get('queryResult').get('action')

        print(action)
        if action=='search_world':
            
            apiCall = requests.get('https://covid19.mathdro.id/api').json()

            data = {
                'confirmed': apiCall['confirmed']['value'],
                'deaths': apiCall['deaths']['value'],
                
            }
            

            message = "Total number of people in the world affected with COVID19 is {}. There have been {} deaths".format(format(data['confirmed']), format(data['deaths']))

            

            responseObj = {
                "fulfillmentText":  message,
               
            }
            print("world response",responseObj)


        else:
            country = req.get('queryResult').get('parameters').get('geo-country')

            for countryData in country_info:
                if country==countryData['name']:
                    code=countryData['code']

            apiCall = requests.get("https://covid19.mathdro.id/api/countries/"+ code).json()

            data = {
                'confirmed': apiCall['confirmed']['value'],
                'deaths': apiCall['deaths']['value'],
                
            }
            print(data)

            message = "Total number of people in {} affected with COVID19 is {}. There have been {} deaths".format(country, format(data['confirmed']), format(data['deaths']))
            

            responseObj = {
                "fulfillmentText":  message,
                
                
            }

            
        print("final")

        return JsonResponse(responseObj)

    