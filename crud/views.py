from django.http import response
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
import ast

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
            "tags" : ast.literal_eval(company.tags)
        }

        return JsonResponse({'Message':result}, status=200)

class AutoCompleteAPIView(APIView):
    def get(self, request):
        search_value      = request.query_params.get("query", "")
        decode_search_value = parse.unquote(search_value)
        x_wanted_language = request.headers.get('x-wanted-language')

        try:
            companies = Company.objects.filter(name__icontains=decode_search_value)
        except:
            raise Http404

        suggestions = []
        for company in companies:
            company_connection = Company_connection.objects.get(pk = company.company_id.pk) 
            company = company_connection.connection_company.filter(lang_type = x_wanted_language)[0]
            suggestions.append(company.name)

        results = {
            'company_name' : suggestions
        } 

        return JsonResponse({'Message':results}, status=200)
      
class companyEnrollmentView(APIView):
    def post(self,request):
        x_wanted_language = request.headers.get('x-wanted-language')
        company_name = request.data['company_name']
        tags = request.data['tags']
        length = len(company_name)


        company_connection = Company_connection()
        company_connection.save()
                # print(row)
        result_tags = None

        for lan,name in company_name.items():
            company = Company()
            company.name = name
            company.lang_type = lan
            tag_list = []
            for tag in tags:
                tag_list.append( tag['tag_name'][lan]) 
            company.tags = str(tag_list)
            company.company_id = company_connection
            company.save()

            if lan == x_wanted_language:
                result_tags = tag_list

            results = {
                'company_name' : company_name[x_wanted_language],
                'tags' : result_tags
            }
        return JsonResponse({'Message':results}, status=200)






