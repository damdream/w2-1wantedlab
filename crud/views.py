from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http.response import JsonResponse
from .models import Company_connection,Company

from django.http           import JsonResponse
from django.views          import View
import csv, json

from urllib import parse
from django.http import Http404

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

     def get(self, request, *args, **kwargs):
        company_name = None 
        if kwargs.get("company_name", None) is not None: #url path로 받은 회사 이름이 존재하면 초기화
            company_name = kwargs["company_name"]
        return_type = request.headers.get('x-wanted-language') # 리턴 언어 타입
        try:
            company = Company.objects.get(name = company_name) #만약 입력된 회사가 존재하지 않으면
        except:
            raise Http404
            
        company_connection = Company_connection.objects.get(pk = company.company_id.pk) 
        company = company_connection.connection_company.filter(lang_type = return_type)[0]
        
        result = {
            "company_name" : company.name,
            "tags" : company.tags
        }

        return Response(result)

class AutoCompleteAPIView(APIView):
    def get(self, request):
        search_value      = request.query_params.get("query", "")
        decode_search_value = parse.unquote(search_value)
        x_wanted_language = request.headers.get('x-wanted-language')

        try:
            companies = Company.objects.filter(name__icontains=decode_search_value)
        except:
            raise Http404

        results = [{
            'company_name' : company.name
        } for company in companies]

        return JsonResponse({'Message':results}, status=200)
      
class companyEnrollmentView(APIView):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if data["name"] == " " :
                return JsonResponse ({"MESSAGE":"company name null"}, status = 400) 

            if Company.objects.filter(company_name = data["company_name"]).exists():
                return JsonResponse ({"MESSAGE": "already exists company"}, status=400)

            Company.objects.create(
                company_name = data["company_name"],
                lang_type    = data["lang_type"],
                tags         = data["tags"],
                company_id   = data["company_id"]
            )

            return JsonResponse ({"MESSAGE": "success"}, status=200)
        except KeyError:    
            return JsonResponse ({"MESSAGE": "key error"}, status=404)