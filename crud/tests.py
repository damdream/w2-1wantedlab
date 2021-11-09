from django.test import TestCase, Client
from django.http import response
from crud.models import Company, Company_connection

from rest_framework.response import Response

class AutoCompleteAPIViewTeest(TestCase):
    def setUp(self):
        company_connection1 = Company_connection.objects.create(id=1)
        company_connection2 = Company_connection.objects.create(id=2)
        company_connection3 = Company_connection.objects.create(id=3)

        company1 = Company.objects.create(id=1, name='원티드랩', lang_type='ko', tags=['태그_4', '태그_20', '태그_16'], company_id=company_connection1)
        company2 = Company.objects.create(id=2, name='주식회사 링크드코리아', lang_type='ko', tags=['태그_12', '태그_6', '태그_8'], company_id=company_connection2)
        company3 = Company.objects.create(id=3, name='스피링크', lang_type='ko', tags=['태그_19', '태그_9'], company_id=company_connection3)

    def test_auto_complete_get_success(self):

        client = Client()
        # headers = {"HTTP_X_WANTED_LANGUAGE": "ko"}

        results = [
            {
                'company_name' : '주식회사 링크드코리아'
            },
            {
                'company_name' : '스피링크'
            },
        ]

        response = client.get('/crud/search?query=링크')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'Message' : results}
        )

    def tearDown(self):
        Company.objects.all().delete()
        Company_connection.objects.all().delete()




class SearchAPIViewTeest(TestCase):
    def setUp(self):
        company_connection = Company_connection.objects.create(id=1)
        

        company = Company.objects.create(id=1, name='원티드랩', lang_type='ko', tags=['태그_4', '태그_20', '태그_16'], company_id=company_connection)
        

    def test_search_get_success(self):

        client = Client()
        header = {"HTTP_X_WANTED_LANGUAGE": "ko"}

        results = {
        "company_name": "원티드랩",
        "tags": [
            "태그_4",
            "태그_20",
            "태그_16"
        ]
    }
        response = client.get('/crud/search/Wantedlab/',**header)
        print("----------------------")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'Message' : results}
        )

    def tearDown(self):
        Company.objects.all().delete()
        Company_connection.objects.all().delete()


