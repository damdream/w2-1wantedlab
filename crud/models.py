from django.db import models



class Company_connection(models.Model):
    pass

class Company(models.Model):
   
    name = models.CharField(max_length=200, null=False)
    lang_type = models.CharField(max_length=200, null=False)
    tags= models.CharField(max_length=200, null=False)
    company_id= models.ForeignKey(
        Company_connection,
        on_delete=models.CASCADE,null=True,
        related_name = 'connection_company'
    )
    



