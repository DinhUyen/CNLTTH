from django.db import connection
from rest_framework import pagination
from multimethod import multimethod
import re
from datetime import date
# create funtion get dict object in database
def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

@multimethod
def getDictFromQuery(query_String:str,param:list,page:str=None,size:str=None):  
    with connection.cursor() as cursor:
        if page is not None:
            query_String=query_String+" LIMIT %s OFFSET %s"
            if size is not None:
                param =param + [int(size),(int(page)-1)*int(size)]
            else:
                param =param + [pagination.PageNumberPagination.page_size,int(page)*pagination.PageNumberPagination.page_size]    
        # print(query_String)       
        cursor.execute(query_String,param)
        obj = dictfetchall(cursor)
    return obj
   

@multimethod
def getDictFromQuery(cursor:object,query_String:str,param:list,page:str=None,size:str=None):
    if page is not None:
        query_String=query_String+" LIMIT %s OFFSET %s"
        if size is not None:
            param =param + [int(size),(int(page)-1)*int(size)]
        else:
            param =param + [pagination.PageNumberPagination.page_size,int(page)*pagination.PageNumberPagination.page_size]     
    cursor.execute(query_String,param)
    obj = dictfetchall(cursor)
    return obj
