from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Company_connection,Company
from django.http           import JsonResponse
from django.views          import View
import csv, json
class DataInjectionView(APIView):
    def get(self, request):


        base_url = settings.BASE_DIR
        
        CSV_PATH = str(base_url) + "/wanted_temp_data.csv"
        print(CSV_PATH)
        with open(CSV_PATH, newline='') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                company_connection = Company_connection()
                company_connection.save()
                # print(row)
                company = Company()
                company.name     = row['company_ko']
                company.lang_type      = "ko"
                company.tags = str(row['tag_ko'].split('|'))
                company.company_id = company_connection
                company.save()
                

                company = Company()
                company.name     = row['company_en']
                company.lang_type      = "en"
                company.tags = str(row['tag_en'].split('|'))
                company.company_id = company_connection
                company.save()
        
               
                
                company = Company()
                company.name     = row['company_ja']
                company.lang_type      = "ja"
                company.tags = str(row['tag_ja'].split('|'))
                company.company_id = company_connection
                company.save()

                
        return Response("good!!")


class SearchAPIView(APIView):
     def post(self, request):
         return_lang = request.data



class companyEnrollmentView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if data["company_name"] == "" :
                return JsonResponse ({"MESSAGE":"company name null"}, status = 404) 

            Company.objects.create(
                name         = data["company_name"],
                lang_type    = data["lang_type"],
                tags         = data["tags"],
                profile      = data["profile"]
            )

            return JsonResponse ({"MESSAGE": "success"}, status=200)
        except:    
            return JsonResponse ({"MESSAGE": "already exists company"}, status=404)