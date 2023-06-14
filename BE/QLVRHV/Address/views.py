
from rest_framework import viewsets
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import pagination
from Common import generics_cursor, custom_permission
from Common.generics import *
class AddressPermission(custom_permission.CustomPermissions):
    def __init__(self):
        super().__init__()

    # def get_allowed_methods(self, username):
    #     ## query in database here
    #     username = username
    #     return ['GET']


# Create your views here.
class AddressViewSet(viewsets.ViewSet):
    """
    Interact with UserCam
    """
    
    permission_classes = [AddressPermission]

    # all swagger's parameters should be defined here 
    sw_page = openapi.Parameter(
        name='page', type=openapi.TYPE_STRING, description="Page number", in_=openapi.IN_QUERY)
    sw_size = openapi.Parameter(
        name='size', type=openapi.TYPE_STRING, description="Number of results to return per page", in_=openapi.IN_QUERY)
    sw_DonViID = openapi.Parameter(
        name='donViID', type=openapi.TYPE_STRING, description="DonViID", in_=openapi.IN_QUERY)
    sw_UserID = openapi.Parameter(
        name='UserID', type=openapi.TYPE_STRING, description="UserID", in_=openapi.IN_QUERY)

    get_list_don_vi_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_204_NO_CONTENT: 'NO_CONTENT',
        status.HTTP_200_OK: 'JSON',
    }

    def getNameDonVi(self,donViID):
        try:
            if donViID.startswith("TD"):
                query_string="SELECT MaTD code, TenTD name FROM TIEUDOAN WHERE TIEUDOAN.MaTD =  %s "
            elif donViID.startswith("DD"):
                query_string="SELECT MaDD code, TenDD name FROM DAIDOI WHERE DAIDOI.MaDD =  %s "
            elif donViID.startswith("L"):
                query_string="SELECT MALOP code, TenLop name FROM LOP WHERE LOP.MaLop =  %s "
            obj=generics_cursor.getDictFromQuery(query_string,[donViID])
            if obj is None or len(obj)==0:
                return ""
        except:
            return ""
        return obj[0]["name"]

    @swagger_auto_schema(method='get', manual_parameters=[], responses=get_list_don_vi_response)
    @action(methods=['GET'], detail=False, url_path='get-list-don-vi')
    def get_list_don_vi(self, request):    
        """
        API này dùng để lấy danh sách đơn vị thuộc quyền quản lý của người dùng hiện tại. Level: 1- lớp, 2 - đại đội , 3 - tiểu đoàn, 4 - học viện
        """    
        username= request.user.username
        roleId = request.user.roleID
        query_string="SELECT * FROM DONVI WHERE DONVIID=    \
                        (                                   \
                        SELECT DONVIID FROM ACCOUNT_USER    \
                        INNER JOIN PERSON ON PERSON.PersonID = ACCOUNT_USER.personID\
                        WHERE USERNAME = %s            \
                        )"
        address_user=generics_cursor.getDictFromQuery(query_string,[username])[0]
        list_tieu_doan={}
        query_string="SELECT * FROM TIEUDOAN"
        address = generics_cursor.getDictFromQuery(query_string,[])
        list_tieu_doan['HV']=[]
        for add in address:
            list_tieu_doan['HV'].append(add['MaTD'])

        list_don_vi={}
        temp_list_tieu_doan= {'HV':address_user['MaTieuDoan']} if address_user['MaTieuDoan']  is not None else {'HV':[]}
        temp_list_tieu_doan = list_tieu_doan['HV'] if len(list_tieu_doan)>0 else temp_list_tieu_doan
        for tieu_doan in temp_list_tieu_doan:
            query_string="SELECT MADAIDOI FROM DONVI WHERE MaTieuDoan = %s "
            list_MaDD = generics_cursor.getDictFromQuery(query_string,[tieu_doan])
            list_don_vi[tieu_doan]={}
            for dai_doi in list_MaDD:
                if dai_doi['MaDaiDoi'] is not None:
                    list_don_vi[tieu_doan][dai_doi['MaDaiDoi']]=[]
                    query_string="SELECT MaLop FROM DONVI WHERE MaDaiDoi = %s"
                    list_lop = generics_cursor.getDictFromQuery(query_string,[dai_doi['MaDaiDoi']])
                    for lop in list_lop:
                        if lop['MaLop'] is not None:
                            list_don_vi[tieu_doan][dai_doi['MaDaiDoi']].append(lop['MaLop'])
        level=0

        if roleId == GUARDSMAN_ROLE or roleId == ACADEMY_ROLE:
            output=list_don_vi
            level=4
        elif roleId == BATTALION_ROLE:
            output={address_user['MaTieuDoan']:list_don_vi[address_user['MaTieuDoan']]}
            level=3
        elif roleId == COMPANY_ROLE:
            output={address_user['MaDaiDoi']:list_don_vi[address_user['MaTieuDoan']][address_user['MaDaiDoi']]}
            level=2
        elif roleId == CLASS_ROLE:
            output = address_user['MaLop'] 
            level=1
        result = []
        if isinstance(output, dict):
            for k,v in output.items():
                name = self.getNameDonVi(k)
                outer_dict = {"code": k,"name":name, "data": []}
                if isinstance(v, dict):
                    for inner_k, inner_v in v.items():
                        list_lop=[]
                        for lop in inner_v:
                            name_lop= self.getNameDonVi(lop)
                            list_lop.append({"code":lop, "name":name_lop,})
                        inner_name=self.getNameDonVi(inner_k)
                        inner_dict = {"code": inner_k, "name":inner_name,"data": list_lop}
                        outer_dict["data"].append(inner_dict)
                else:
                    print(v)
                    for lop in v:
                        name_lop= self.getNameDonVi(lop)
                        outer_dict["data"].append({"code":lop, "name":name_lop,})
                result.append(outer_dict)
        else:
            for lop in output:
                name_lop= self.getNameDonVi(lop)
                result.append({"code":lop, "name":name_lop,})
        return Response(data={"level":level,"data":result}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID], responses=get_list_don_vi_response)
    @action(methods=['GET'], detail=False, url_path='get-info-don-vi')
    def get_info_don_vi(self, request):
        """
        API này dùng để lấy thông tin của đơn vị, tham số nhập vào có thể là mã lớp, mã đại đội hoặc mã tiểu đoàn.
        """ 
        donViID =str(request.query_params.get('donViID'))
        try:
            if donViID.startswith("TD"):
                query_string="SELECT * FROM TIEUDOAN WHERE TIEUDOAN.MaTD = %s "
            elif donViID.startswith("DD"):
                query_string="SELECT * FROM DAIDOI WHERE DAIDOI.MaDD = %s "
            elif donViID.startswith("L"):
                query_string="SELECT * FROM LOP WHERE LOP.MaLop = %s "
            obj=generics_cursor.getDictFromQuery(query_string,[donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID], responses=get_list_don_vi_response)
    @action(methods=['GET'], detail=False, url_path='get-name-don-vi')
    def get_name_don_vi(self, request):
        """
        API này dùng để lấy ttên của đơn vị, tham số nhập vào có thể là mã lớp, mã đại đội hoặc mã tiểu đoàn.
        """ 
        donViID =str(request.query_params.get('donViID'))
        try:
            if donViID.startswith("TD"):
                query_string="SELECT MaTD code, TenTD name FROM TIEUDOAN WHERE TIEUDOAN.MaTD =  %s "
            elif donViID.startswith("DD"):
                query_string="SELECT MaDD code, TenDD name FROM DAIDOI WHERE DAIDOI.MaDD =  %s "
            elif donViID.startswith("L"):
                query_string="SELECT MALOP code, TenLop name FROM LOP WHERE LOP.MaLop =  %s "
            obj=generics_cursor.getDictFromQuery(query_string,[donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
