from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import requests
import json
import os

def home(request):
    return render(request, "front.html")

def download(request):
    newfac = []
    # get of open facilities
    url = "https://api.kmhfltest.health.go.ke/api/facilities/material/?format=json&access_token=hgGAMT3poDU4o4qRxhY3QWEYGDYiaH&fields=id,code,name,official_name,regulatory_status_name,updated,facility_type_name,owner_name,county,sub_county_name,rejected,ward_name,keph_level,keph_level_name,constituency_name,is_complete,in_complete_details,approved,is_approved,approved_national_level&page_size=1000"
    API_KEY = "" #generate API key
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response =  requests.get(url, headers=headers)
    if(response):
        Data = response.json()
        page_size = 1000
        for i in range(page_size-1):
            if Data["results"][i]["closed"] == 0: # 0=false
                newfac.append(Data["results"][i])
    else:
        print("Error receiving facilities")    
    with open('openfacilities.json', 'w') as outfile:   #write filtered data to json
            json.dump(newfac[0:-1], outfile, indent=4)
    outfile.close()
            
    with open('openfacilities.json', 'r') as f:         # Replace boolean values
        data = json.load(f)
        for i in range(961):                # pgsize 1000 = 960 facilities
            if data[i]["closed"] == 0:
                data[i]["closed"] = "No"
            elif data[i]["closed"] == 1:
                data[i]["closed"] = "Yes"
            if data[i]["open_public_holidays"] == 0:
                data[i]["open_public_holidays"] = "No"
            elif data[i]["open_public_holidays"] == 1:
                data[i]["open_public_holidays"] = "Yes"
            if data[i]["open_weekends"] == 0:
                data[i]["open_weekends"] = "No"
            elif data[i]["open_weekends"] == 1:
                data[i]["open_weekends"] = "Yes"
            if data[i]["open_late_night"] == 0:
                data[i]["open_late_night"] = "No"
            elif data[i]["open_late_night"] == 1:
                data[i]["open_late_night"] = "Yes"
            if data[i]["approved"] == 0:
                data[i]["approved"] = "No"
            elif data[i]["approved"] == 1:
                data[i]["approved"] = "Yes"
            if data[i]["open_whole_day"] == 0:
                data[i]["open_whole_day"] = "No"
            elif data[i]["open_whole_day"] == 1:
                data[i]["open_whole_day"] = "Yes"
            if data[i]["is_public_visible"] == 0:
                data[i]["is_public_visible"] = "No"
            elif data[i]["is_public_visible"] == 1:
                data[i]["is_public_visible"] = "Yes"
            if data[i]["is_published"] == 0:
                data[i]["is_published"] = "No"
            elif data[i]["is_published"] == 1:
                data[i]["is_published"] = "Yes"

    with open('openfacilities.json', 'w') as outfile:   
        json.dump(data, outfile, indent=4)
    f.close()
    
    os.system('node toexcel.js')
    
    response = HttpResponse(open("openfacilities.xlsx", 'rb').read())
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename=openfacilities.xlsx'
    return response

