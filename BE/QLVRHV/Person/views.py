
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
from datetime import datetime, timedelta
import pytz


class PersonPermission(custom_permission.CustomPermissions):
    def __init__(self):
        super().__init__()

    # def get_allowed_methods(self, username):
    #     ## query in database here
    #     username = username
    #     return ['GET']
class VeBinhPermission(custom_permission.CustomPermissions):
    def __init__(self):
        super().__init__()

    def get_allowed_methods(self, CODE_VIEW):
        if int(CODE_VIEW) == GUARDSMAN_ROLE:
            return ['GET','POST','PUT','DELETE']
        if int(CODE_VIEW) > NO_ROLE: # role admin
            return ['GET']       
        else:
            return []

# Create your views here.
class PersonViewSet(viewsets.ViewSet):
    """
    Interact with UserCam
    """

    permission_classes = [PersonPermission]

    # all swagger's parameters should be defined here
    sw_page = openapi.Parameter(
        name='page', type=openapi.TYPE_STRING, description="Page number", in_=openapi.IN_QUERY)
    sw_size = openapi.Parameter(
        name='size', type=openapi.TYPE_STRING, description="Number of results to return per page", in_=openapi.IN_QUERY)
    sw_DonViID = openapi.Parameter(
        name='donViID', type=openapi.TYPE_STRING, description="Mã đơn vị ( lớp, đại đội, tiểu đoàn)", default="DD155", in_=openapi.IN_QUERY)
    sw_MaHV = openapi.Parameter(
        name='maHV', type=openapi.TYPE_STRING, description="MaHV", default="201901058", in_=openapi.IN_QUERY)
    sw_PersonId = openapi.Parameter(
        name='personId', type=openapi.TYPE_STRING, default=1, in_=openapi.IN_QUERY)
    sw_PersonName = openapi.Parameter(
        name='personName', type=openapi.TYPE_STRING, description="Tên", default="Anh", in_=openapi.IN_QUERY) 
    sw_TimeStart = openapi.Parameter(
        name='timeStart', type=openapi.TYPE_STRING, description="Thời gian đi", default="22-06-2023", in_=openapi.IN_QUERY)
    sw_TimeBetween = openapi.Parameter(
        name='timeBetween', type=openapi.TYPE_STRING, description="Time trong tuần", default="22-06-2023", in_=openapi.IN_QUERY)
    sw_NameHV = openapi.Parameter(
        name='nameHV', type=openapi.TYPE_STRING, description="Tên học viên", default="Anh", in_=openapi.IN_QUERY)    
    sw_SttDangKy = openapi.Parameter(
        name='sttDangKy', type=openapi.TYPE_INTEGER, description="Số thứ tự đăng ký", default=15, in_=openapi.IN_QUERY)
    sw_SttCamTrai = openapi.Parameter(
        name='sttCamTrai', type=openapi.TYPE_INTEGER, description="Số thứ tự cấm trại", default=15, in_=openapi.IN_QUERY)
    sw_MaLoaiGiayToRN = openapi.Parameter(
        name='maLoaiGiayToRN', type=openapi.TYPE_INTEGER, description="Mã loại giấy tờ ra ngoài", default=15, in_=openapi.IN_QUERY)
    sw_SttGiayToRN = openapi.Parameter(
        name='sttGiayToRN', type=openapi.TYPE_INTEGER, description="Số thứ tự giấy tờ ra ngoài", default=15, in_=openapi.IN_QUERY)


    get_list_person_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_204_NO_CONTENT: 'NO_CONTENT',
        status.HTTP_200_OK: 'JSON',
    }

    post_list_person_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_304_NOT_MODIFIED: 'NOT_MODIFIED',
        status.HTTP_200_OK: 'JSON',
    }

    def CheckQuyetDinhCamTrai(self, maHV, time_go: "12-03-2023"):
        try:
            if isinstance(type(time_go), str):
                time_go = datetime.strptime(time_go, '%d-%m-%Y').date()
            query_string = f'SELECT * FROM QUYETDINHCAMTRAI \
                            WHERE MAHV = %s \
                            AND TG_BatDau <= %s\
                            AND TG_BatDau <= %s  '
            obj = generics_cursor.getDictFromQuery(
                query_string, [maHV, time_go, time_go])
            if len(obj) > 0:
                return True, obj
        except:
            return True, []
        return False, []

    def getTimeStartAndFinishWeek(self, time_beetween: "12-03-2023"):
        try:
            dt = datetime.strptime(time_beetween, '%d-%m-%Y')
            start = dt - timedelta(days=dt.weekday())
            end = start + timedelta(days=6)
            return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')
        except:
            return None, None

    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size, sw_DonViID], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-hoc-vien')
    def get_list_hoc_vien(self, request):
        """
        API này dùng để lấy danh sách học viên của một đơn vị cụ thể nào, có thể là lớp,đại đội, tiểu đoàn. Để sử dụng phân trang thì nhập thêm param page, size vào.
         KHuVUC : 0 Nước ngoài, 1 MB, 2 MT, 3MN
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        donViID = str(request.query_params.get('donViID'))
        try:
            query_string = "SELECT * FROM HOCVIEN \
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID\
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN LOAIHOCVIEN ON LOAIHOCVIEN.MALOAI = HOCVIEN.LOAIHOCVIEN \
                            WHERE PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)\
                            ORDER BY DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan,HOCVIEN.LOAIHOCVIEN "
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size, sw_DonViID], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-person')
    def get_list_person(self, request):
        """
        API này dùng để lấy danh sách person của một đơn vị cụ thể nào, có thể là lớp,đại đội, tiểu đoàn. Để sử dụng phân trang thì nhập thêm param page, size vào. KHuVUC : 0 Nước ngoài, 1 MB, 2 MT, 3MN
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        donViID = str(request.query_params.get('donViID'))
        try:
            query_string = "SELECT * FROM PERSON \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            WHERE PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s) \
                            ORDER BY DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-account')
    def get_list_account(self, request):
        """
        API này dùng để lấy danh sách person của một đơn vị cụ thể nào, có thể là lớp,đại đội, tiểu đoàn. Để sử dụng phân trang thì nhập thêm param page, size vào. KHuVUC : 0 Nước ngoài, 1 MB, 2 MT, 3MN
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        try:
            query_string = "SELECT * FROM Account_user \
                            LEFT JOIN PERSON ON PERSON.PersonID = Account_user.personID\
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            ORDER BY DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan"
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID,sw_NameHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-info-hoc-vien-by-name')
    def get_info_hoc_vien_by_name(self, request):
        """
        API này dùng để tìm kiếm theo tên học viên của một đơn vị cụ thể nào đó( có thể là lớp,đại đội, tiểu đoàn). 
        """
        donViID = str(request.query_params.get('donViID'))
        nameHV = str(request.query_params.get('nameHV'))

        try:
            query_string = "SELECT * FROM HOCVIEN \
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID\
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN LOAIHOCVIEN ON LOAIHOCVIEN.MALOAI = HOCVIEN.LOAIHOCVIEN \
                            WHERE LOWER(PERSON.HoTen) LIKE LOWER(%s) AND \
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)"
            obj = generics_cursor.getDictFromQuery(
                query_string, [f"%{nameHV}%",donViID, donViID, donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID,sw_PersonName], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-info-person-by-name')
    def get_info_person_by_name(self, request):
        """
        API này dùng để tìm kiếm theo tên một người của một đơn vị cụ thể nào đó( có thể là lớp,đại đội, tiểu đoàn). 
        """
        donViID = str(request.query_params.get('donViID'))
        personName = str(request.query_params.get('personName'))

        try:
            query_string = "SELECT * FROM PERSON \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            WHERE LOWER(PERSON.HoTen) LIKE LOWER(%s) AND \
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)"
            obj = generics_cursor.getDictFromQuery(
                query_string, [f"%{personName}%",donViID, donViID, donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID,sw_MaHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-info-hoc-vien-by-id')
    def get_info_hoc_vien_by_id(self, request):
        """
        API này dùng để tìm kiếm theo mã học viên của một đơn vị cụ thể nào đó( có thể là lớp,đại đội, tiểu đoàn).  KHuVUC : 0 Nước ngoài, 1 MB, 2 MT, 3MN
        """
        donViID = str(request.query_params.get('donViID'))
        maHV = str(request.query_params.get('maHV'))

        try:
            query_string = "SELECT * FROM HOCVIEN \
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID\
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN LOAIHOCVIEN ON LOAIHOCVIEN.MALOAI = HOCVIEN.LOAIHOCVIEN \
                            WHERE HOCVIEN.MaHV = %s AND \
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)"
            obj = generics_cursor.getDictFromQuery(
                query_string, [maHV,donViID, donViID, donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID,sw_PersonId], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-info-person-by-id')
    def get_info_person_by_id(self, request):
        """
        API này dùng để tìm kiếm theo personID của một đơn vị cụ thể nào đó( có thể là lớp,đại đội, tiểu đoàn). KHuVUC : 0 Nước ngoài, 1 MB, 2 MT, 3MN
        """
        donViID = str(request.query_params.get('donViID'))
        personId = str(request.query_params.get('personId'))

        try:
            query_string = "SELECT * FROM PERSON \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID\
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            WHERE PERSON.PersonID = %s AND \
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)"
            obj = generics_cursor.getDictFromQuery(
                query_string, [personId,donViID, donViID, donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size,sw_MaHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-ket-qua-ren-luyen-by-id')
    def get_list_ket_qua_ren_luyen(self, request):
        """
        API này dùng lấy một list danh sách kết quả rèn luyện học viên sắp xếp theo thời gian giảm dần
        """
        donViID = str(request.query_params.get('donViID'))
        try:
            query_string = "SELECT HOCVIEN.MAHV,HOCVIEN.personID,HoTen,NgSinh,PERSON.DonViID,ThoiGian,PhanLoaiRL FROM HV_RENLUYEN  \
                            LEFT JOIN HOCVIEN ON HOCVIEN.MaHV = HV_RENLUYEN.MaHV \
                            LEFT JOIN KQRL ON KQRL.MaLoai = HV_RENLUYEN.MaLoai\
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID  \
                            WHERE  PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)\
                            ORDER BY ThoiGian DESC"
            print(query_string)
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size,sw_MaHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-ket-qua-ren-luyen-by-id')
    def get_list_ket_qua_ren_luyen_by_id(self, request):
        """
        API này dùng lấy một list danh sách kết quả rèn luyện học viên theo mã học viên sắp xếp theo thời gian giảm dần
        """
        maHV = str(request.query_params.get('maHV'))

        try:
            query_string = "SELECT HOCVIEN.MAHV,HOCVIEN.personID,HoTen,NgSinh,PERSON.DonViID,ThoiGian,PhanLoaiRL FROM HV_RENLUYEN  \
                            LEFT JOIN HOCVIEN ON HOCVIEN.MaHV = HV_RENLUYEN.MaHV \
                            LEFT JOIN KQRL ON KQRL.MaLoai = HV_RENLUYEN.MaLoai\
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID  \
                            WHERE HOCVIEN.MAHV = %s \
                            ORDER BY ThoiGian DESC"
            print(query_string)
            obj = generics_cursor.getDictFromQuery(
                query_string, [maHV,])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-permission')
    def get_permission(self, request):
        """
        API này dùng để lấy quyền truy cập ( roleID) của user hiện tại).
        """
        roleId = request.user.roleID
        username= request.user.username
        try:
            query_string = f"SELECT DONVI.MaLop,LOP.TenLop, DONVI.MaDaiDoi,DAIDOI.TenDD,DONVI.MaTieuDoan,TIEUDOAN.TenTD FROM PERSON \
                            INNER JOIN Account_user ON Account_user.personID = PERSON.PersonID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN LOP ON LOP.MaLop= DONVI.MaLop \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            WHERE username= %s "
            info_donvi = generics_cursor.getDictFromQuery( query_string, [username])
            if info_donvi is None or len(info_donvi) == 0:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
            info_donvi=info_donvi[0]
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if roleId == CLASS_ROLE:
            code = info_donvi.get('MaLop')
            name=info_donvi.get('TenLop')
        elif roleId == COMPANY_ROLE:
            code = info_donvi.get('MaDaiDoi')
            name=info_donvi.get('TenDD')
        elif roleId == BATTALION_ROLE:
            code = info_donvi.get('TD01')
            name=info_donvi.get('TenTD')
        elif roleId >= GUARDSMAN_ROLE:
            code = "HV"
            name="Học viện kỹ thuật quân sự"
        else:
            code = ""
            name=""
        return Response({"permission": int(roleId),"code":code,"name":name}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_MaHV, sw_TimeStart], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-check-cam-trai')
    def get_check_cam_trai(self, request):
        """
        API này dùng để check thử xem học viên có bị cấm trại trong khoảng thời gian đăng ký ra ngoài không, tham số nhập vào là mã học viên và thời gian đăng ký ra ngoài.
        """
        maHV = request.query_params.get('maHV')
        timeStart = request.query_params.get('timeStart')

        checkCamTrai, listReason = self.CheckQuyetDinhCamTrai(maHV, timeStart)
        if checkCamTrai:
            if len(listReason) == 0:
                return Response(data={"result": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data={"result": True, "reason": listReason}, status=status.HTTP_200_OK)

        return Response(data={"result": False}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-cam-trai-in-week')
    def get_list_cam_trai_in_week(self, request):
        """
        API này dùng để lấy danh sách các học viên bị cắm trại trong một đơn vị nào đó. timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên bị cấm trại từ đầu tuần đến cuối tuần nằm trong timeBetween đó.
        """
        donViID = request.query_params.get('donViID')
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_start, time_end = self.getTimeStartAndFinishWeek(timeBetween)
        print(time_start, time_end)
        try:
            query_string = f"SELECT STT, QUYETDINHCAMTRAI.MAHV, PERSON.HOTEN, TG_BATDAU, TG_KETTHUC, LIDO FROM QUYETDINHCAMTRAI \
                            LEFT JOIN HOCVIEN ON HOCVIEN.MaHV = QUYETDINHCAMTRAI.MaHV \
                            LEFT JOIN PERSON ON HOCVIEN.PERSONID = PERSON.PersonID \
                            LEFT JOIN DONVI ON PERSON.DonViID = DONVI.DonViID  \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE ((TG_BatDau BETWEEN '{time_start}'AND '{time_end}') OR \
                            (TG_KetThuc BETWEEN '{time_start}'AND '{time_end}') OR  \
                            (TG_BatDau <= '{time_start}' AND TG_KetThuc >= '{time_end}'))\
                            AND HOCVIEN.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))\
                            ORDER BY DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan,TG_BatDau"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'reason': openapi.Schema(type=openapi.TYPE_STRING, description="Lý di cấm trại", default="Vi phạm tác phong"),
            'time_start': openapi.Schema(type=openapi.TYPE_STRING, default='22-05-2023'),
            'time_end': openapi.Schema(type=openapi.TYPE_STRING, default='22-07-2023'),
            'ma_HV': openapi.Schema(type=openapi.TYPE_STRING, default='202104043'),
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-them-hoc-vien-cam-trai')
    def post_them_hoc_vien_cam_trai(self, request):
        """
        API này dùng để thêm học viên ra ngoài, chỉ tài khoản có quyền từ đại đội trở lên mới thêm được.
        """
        dataDict = request.data
        ma_HV = dataDict.get("ma_HV")
        timeStart = dataDict.get("time_start")
        timeEnd = dataDict.get("time_end")
        reason = dataDict.get("reason")
        roleId = request.user.roleID
        if roleId < COMPANY_ROLE:
            return Response(data={}, status=status.HTTP_304_NOT_MODIFIED)
        try:
            timeStart = datetime.strptime(timeStart, "%d-%m-%Y").strftime("%Y-%m-%d")
            timeEnd = datetime.strptime(timeEnd, "%d-%m-%Y").strftime("%Y-%m-%d")    

            query_string = f'INSERT INTO QUYETDINHCAMTRAI("MaHV","TG_BatDau","TG_KetThuc","LIDO") VALUES (%s,%s,%s,%s);'
            param = [ma_HV,timeStart,timeEnd,reason]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'reason': openapi.Schema(type=openapi.TYPE_STRING, description="Lý do cấm trại", default="Vi phạm tác phong"),
            'time_start': openapi.Schema(type=openapi.TYPE_STRING, default='22-05-2023'),
            'time_end': openapi.Schema(type=openapi.TYPE_STRING, default='22-07-2023'),
            'STT': openapi.Schema(type=openapi.TYPE_INTEGER, default=15),
        }
    ), responses=post_list_person_response)
    @action(methods=['PUT'], detail=False, url_path='put-thay-doi-thong-tin-cam-trai')
    def put_thay_doi_thong_tin_cam_trai(self, request):
        """
        API này dùng để sửa đổi thông tin cấm trại của học viên, chỉ tài khoản có quyền từ đại đội trở lên mới thêm được.
        """
        dataDict = request.data
        STT = dataDict.get("STT")
        timeStart = dataDict.get("time_start")
        timeEnd = dataDict.get("time_end")
        reason = dataDict.get("reason")
        roleId = request.user.roleID
        if roleId < COMPANY_ROLE:
            return Response(data={}, status=status.HTTP_304_NOT_MODIFIED)
        try:
            timeStart = datetime.strptime(timeStart, "%d-%m-%Y").strftime("%Y-%m-%d")
            timeEnd = datetime.strptime(timeEnd, "%d-%m-%Y").strftime("%Y-%m-%d")    

            query_string = f'UPDATE QUYETDINHCAMTRAI SET TG_BatDau = %s, TG_KetThuc = %s, LIDO = %s WHERE STT = %s;'
            param = [timeStart,timeEnd,reason,STT]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='delete', manual_parameters=[sw_SttCamTrai], responses=get_list_person_response)
    @action(methods=['DELETE'], detail=False, url_path='delete-cam-trai')
    def delete_cam_trai(self, request):
        """
        API này dùng để xóa một quyết định cấm trại của học viên.
        """
        sttCamTrai = request.query_params.get('sttCamTrai')
        try:
            query_string = f"DELETE FROM QUYETDINHCAMTRAI WHERE  STT  = %s"
            param = [sttCamTrai]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)            
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    
    
    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'hinh_thuc_RN': openapi.Schema(type=openapi.TYPE_INTEGER, description="0 là tranh thủ,1 là ra ngoài", default=1),
            'dia_diem': openapi.Schema(type=openapi.TYPE_STRING, description="Địa điểm", default="Hà Nội"),
            'time_start': openapi.Schema(type=openapi.TYPE_STRING, default='2023-03-11 16:30'),
            'time_end': openapi.Schema(type=openapi.TYPE_STRING, default='2023-03-13 18:00'),
            'ma_HV': openapi.Schema(type=openapi.TYPE_STRING, default='202104043'),
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-dang-ky-ra-ngoai')
    def post_dang_ky_ra_ngoai(self, request):
        """
        API này dùng để đăng ký học viên ra ngoài nếu học viên không nằm trong danh sách cấm trại. Mặc định trái thái xét duyệt sẽ là 0. Đối với hình thức ra ngoài, nhập 0 nếu là tranh thủ, nhập 1 nếu là tranh thủ miền Nam, nhập 2 nếu là ra ngoài. 
        """
        dataDict = request.data
        print(dataDict)
        try:
            hinhThucRN =dataDict.get("hinh_thuc_RN")
            # if hinhThucRN == 0:
            #     hinhThucRN = "Tranh thủ miền Nam"
            # elif hinhThucRN == 1:
            #     hinhThucRN = "Tranh thủ miền Bắc"
            # else:
            #     hinhThucRN="Ra ngoài"


            diaDiem = dataDict.get("dia_diem")
            maHV = dataDict.get("ma_HV")
            timeStart = dataDict.get("time_start")
            timeEnd = dataDict.get("time_end")
            timeStart = datetime.strptime(timeStart, '%Y-%m-%d %H:%M')
            timeEnd = datetime.strptime(timeEnd, '%Y-%m-%d %H:%M')
            checkCamTrai, listReason = self.CheckQuyetDinhCamTrai(maHV, timeStart)

            if checkCamTrai:
                print("cam trai")
                return Response(data={}, status=status.HTTP_403_FORBIDDEN)           
            print("khong cam trai")
            query_string = f'INSERT INTO DSDANGKY("HinhThucRN","DiaDiem","ThoiGianDi","ThoiGianVe","MaHV","TRANGTHAIXD") VALUES (%s,%s,%s,%s,%s,1);'
            param = [hinhThucRN, diaDiem, timeStart, timeEnd, maHV]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-hinh-thuc-ra-ngoai')
    def get_list_hinh_thuc_RN(self, request):
        """
        API này dùng để lấy danh sách các hình thức ra ngoài
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')

        try:
            query_string = f"SELECT * FROM HINHTHUCRN"
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'STT': openapi.Schema(type=openapi.TYPE_INTEGER, default=23),
            'hinh_thuc_RN': openapi.Schema(type=openapi.TYPE_INTEGER, description="0 là tranh thủ,1 là ra ngoài", default=1),
            'dia_diem': openapi.Schema(type=openapi.TYPE_STRING, description="Địa điểm", default="Hà Nội"),
            'time_start': openapi.Schema(type=openapi.TYPE_STRING, default='2023-06-19 16:30'),
            'time_end': openapi.Schema(type=openapi.TYPE_STRING, default='2026-06-21 18:00'),
        }
    ), responses=post_list_person_response)
    @action(methods=['PUT'], detail=False, url_path='put-thay_doi-thong-tin-dang-ky')
    def put_thay_doi_thong_tin_dang_ky(self, request):
        """
        API này dùng để  thay đổi thông tin học viên ra ngoài. Đối với hình thức ra ngoài, nhập 0 nếu là tranh thủ, nhập 1 nếu là ra ngoài. 
        """
        dataDict = request.data
        try:
            # hinhThucRN = int(dataDict.get("hinh_thuc_RN"))
            hinhThucRN = dataDict.get("hinh_thuc_RN")
            # if hinhThucRN == 0:
            #     hinhThucRN = "Tranh thủ"
            # else:
            #     hinhThucRN = "Ra ngoài"

            STT = dataDict.get("STT")
            diaDiem = dataDict.get("dia_diem")
            timeStart = dataDict.get("time_start")
            timeEnd = dataDict.get("time_end")
            timeStart = datetime.strptime(timeStart, '%Y-%m-%d %H:%M')
            timeEnd = datetime.strptime(timeEnd, '%Y-%m-%d %H:%M')         

            query_string = f'UPDATE DSDANGKY SET HinhThucRN = %s, DiaDiem = %s, ThoiGianDi = %s, ThoiGianVe = %s, TRANGTHAIXD = 1 WHERE STT = %s AND TRANGTHAIXD=1;'
            param = [hinhThucRN, diaDiem, timeStart, timeEnd,STT]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-dang-ky')
    def get_list_dang_ky(self, request):
        """
        API này dùng để lấy danh sách các học viên đăng ký theo  đơn vị(lớp, đại đội, tiểu đoàn). timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên đăng ký từ đầu tuần đến cuối tuần nằm trong timeBetween đó.TrạngThaiXD >0 là được duyệt, nếu < 0 là không được  duyệt, còn =0 là chưa được xét duyệt.
        """
        donViID = request.query_params.get('donViID')
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        # if timeBetween is None:
        #     timeBetween = datetime.now().strftime("%d-%m-%Y")
        # time_start, time_end = self.getTimeStartAndFinishWeek(timeBetween)
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_format = "%d-%m-%Y"
        current_time = datetime.strptime(timeBetween, time_format)
        current_weekday = current_time.weekday()
        week_start = current_time - timedelta(days=current_weekday)
        week_end = week_start + timedelta(days=6)
        time_start = (week_start - timedelta(days=1)).strftime("%Y-%m-%d")
        time_end = (week_end + timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.STT AS STT_HTRN, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,HOCVIEN.MAHV, PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}') \
                            AND DSDANGKY.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='delete', manual_parameters=[sw_SttDangKy], responses=get_list_person_response)
    @action(methods=['DELETE'], detail=False, url_path='delete-dang-ky')
    def delete_dang_ky(self, request):
        """
        API này dùng để xóa một yêu cầu đăng ký ra ngoài. Để xóa được, học viên đăng ký ra ngoài phải chưa được xét duyệt.
        """
        sttDangKy = request.query_params.get('sttDangKy')
        try:
            query_string = f"DELETE FROM DSDANGKY WHERE TRANGTHAIXD = 1 AND STT  = %s"
            param = [sttDangKy]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)            
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-duoc-duyet')
    def get_list_danh_sach_duoc_duyet(self, request):
        """
        API này dùng để lấy danh sách các học viên được xét duyệt theo đơn vị(lớp, đại đội, tiểu đoàn). timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên được xét duyệt từ đầu tuần đến cuối tuần nằm trong timeBetween đó.
        """
        donViID = request.query_params.get('donViID')
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        # if timeBetween is None:
        #     timeBetween = datetime.now().strftime("%d-%m-%Y")
        # time_start, time_end = self.getTimeStartAndFinishWeek(timeBetween)
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_format = "%d-%m-%Y"
        current_time = datetime.strptime(timeBetween, time_format)
        current_weekday = current_time.weekday()
        week_start = current_time - timedelta(days=current_weekday)
        week_end = week_start + timedelta(days=6)
        time_start = (week_start - timedelta(days=1)).strftime("%Y-%m-%d")
        time_end = (week_end + timedelta(days=1)).strftime("%Y-%m-%d")
        print(time_start, time_end)
        time_xetduyet = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe, HOCVIEN.MAHV, PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE (TRANGTHAIXD >= HinhThucRN.QUYEN ) AND \
                            (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}') \
                            AND '{time_xetduyet}' < ThoiGianDi \
                            AND DSDANGKY.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-khong-duoc-duyet')
    def get_list_danh_sach_khong_duoc_duyet(self, request):
        """
        API này dùng để lấy danh sách các học viên không được duyệt theo đơn vị(lớp, đại đội, tiểu đoàn). timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên không được duyệt từ đầu tuần đến cuối tuần nằm trong timeBetween đó.
        """
        donViID = request.query_params.get('donViID')
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        # if timeBetween is None:
        #     timeBetween = datetime.now().strftime("%d-%m-%Y")
        # time_start, time_end = self.getTimeStartAndFinishWeek(timeBetween)
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_format = "%d-%m-%Y"
        current_time = datetime.strptime(timeBetween, time_format)
        current_weekday = current_time.weekday()
        week_start = current_time - timedelta(days=current_weekday)
        week_end = week_start + timedelta(days=6)
        time_start = (week_start - timedelta(days=1)).strftime("%Y-%m-%d")
        time_end = (week_end + timedelta(days=1)).strftime("%Y-%m-%d")
        
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,HOCVIEN.MAHV, PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE TRANGTHAIXD < 0 AND \
                            (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}') \
                            AND DSDANGKY.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-chua-duoc-duyet')
    def get_list_danh_sach_chua_duoc_duyet(self, request):
        """
        API này dùng để lấy danh sách các học viên chưa được xét duyệt theo đơn vị(lớp, đại đội, tiểu đoàn). timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên chưa được xét duyệt từ đầu tuần đến cuối tuần nằm trong timeBetween đó.
        """
        donViID = request.query_params.get('donViID')
        permission = request.user.roleID
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        # if timeBetween is None:
        #     timeBetween = datetime.now().strftime("%d-%m-%Y")
        # time_start, time_end = self.getTimeStartAndFinishWeek(timeBetween)
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_format = "%d-%m-%Y"
        current_time = datetime.strptime(timeBetween, time_format)
        current_weekday = current_time.weekday()
        week_start = current_time - timedelta(days=current_weekday)
        week_end = week_start + timedelta(days=6)
        time_start = (week_start - timedelta(days=1)).strftime("%Y-%m-%d")
        time_end = (week_end + timedelta(days=1)).strftime("%Y-%m-%d")
        time_xetduyet = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        print(time_xetduyet)
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,HOCVIEN.maHV, PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE (TRANGTHAIXD >= 0) AND (TRANGTHAIXD < {permission}) AND  \
                            (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}')  AND\
                            '{time_xetduyet}' < ThoiGianDi AND\
                            TRANGTHAIXD < HinhThucRN.QUYEN \
                            AND DSDANGKY.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'STT_dang_ky': openapi.Schema(type=openapi.TYPE_INTEGER, description="Số thứ tự trong danh sách đăng ký ra ngoài", default=1),
            'xet_duyet': openapi.Schema(type=openapi.TYPE_INTEGER,description="Trạng thái xét duyệt,1 là được duyệt,-1 là không được duyệt", default=1)
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-xet-duyet-ra-ngoai')
    def post_xet_duyet_ra_ngoai(self, request):
        """
        API này dùng để xét duyệt học viên ra ngoài. Đối với trạng thái xét duyệt, nhập 1 nếu duyệt và nhập -1 nếu không được duyệt. 
        """
        roleId = int(request.user.roleID)
        dataDict = request.data
        STT_dang_ky =int(dataDict.get("STT_dang_ky"))
        xet_duyet = int(dataDict.get("xet_duyet"))
        if xet_duyet == 1:
            xet_duyet = roleId
        elif xet_duyet == -1:
            xet_duyet = -roleId
        else:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try: 
            query_string = f"SELECT * FROM DSDANGKY WHERE STT = {STT_dang_ky}"
            obj = generics_cursor.getDictFromQuery(query_string, [])
            if len(obj) > 0:
                data_dang_ky= obj[0]
            if  abs(int(data_dang_ky["TRANGTHAIXD"])) > abs(xet_duyet):
                return Response(data={"status": False}, status=status.HTTP_304_NOT_MODIFIED)
          
            query_string = f'UPDATE "DSDANGKY" SET TRANGTHAIXD= {xet_duyet} WHERE STT = {STT_dang_ky}'
            with connection.cursor() as cursor:
                cursor.execute(query_string, [])
                rows_affected = cursor.rowcount
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)
    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-loai-giay-to')
    def get_list_loai_giay_to(self, request):
        """
        API này dùng để lấy danh sách các loại giấy tờ ra ngoài.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')

        try:
            query_string = f"SELECT * FROM GIAYTORN"
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'ten_loai': openapi.Schema(type=openapi.TYPE_STRING,description="Tên loại giấy tờ")
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-them-loai-giay-to-RN')
    def post_them_loai_giay_to_RN(self, request):
        """
        API này dùng để thêm loại giấy tờ ra ngoài.
        """
        dataDict = request.data
        ten_loai = dataDict.get("ten_loai")       
        try:             
            query_string = f'INSERT INTO GIAYTORN("TenLoai") VALUES (%s)'
            with connection.cursor() as cursor:
                cursor.execute(query_string, [ten_loai])
                rows_affected = cursor.rowcount
            if rows_affected == 0:
                return Response(data={"status": False,"msg":"Có lỗi xảy ra"}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True,"msg":"Thêm thành công"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='delete', manual_parameters=[sw_MaLoaiGiayToRN], responses=get_list_person_response)
    @action(methods=['DELETE'], detail=False, url_path='delete-loai-giay-to-RN')
    def delete_loai_giay_to_RN(self, request):
        """
        API này dùng để xóa một yêu cầu đăng ký ra ngoài. Để xóa được, học viên đăng ký ra ngoài phải chưa được xét duyệt.
        """
        maLoaiGiayToRN = request.query_params.get('maLoaiGiayToRN')
        try:
            query_string = f"DELETE FROM GIAYTORN WHERE MaLoai  = %s"
            param = [maLoaiGiayToRN]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)            
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID, sw_TimeBetween,sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-giay-to-RN-hoc-vien')
    def get_list_giay_to_RN_hoc_vien(self, request):
        """
        API này dùng để lấy danh sách các giấy tờ ra ngoài của học viên trong một khoảng thời gian của một đơn vị nào đó.
        """
        donViID = request.query_params.get('donViID')
        timeBetween = request.query_params.get('timeBetween')
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        if timeBetween is None:
            timeBetween = datetime.now().strftime("%d-%m-%Y")
        time_format = "%d-%m-%Y"
        current_time = datetime.strptime(timeBetween, time_format)
        current_weekday = current_time.weekday()
        week_start = current_time - timedelta(days=current_weekday)
        week_end = week_start + timedelta(days=6)
        time_start = (week_start - timedelta(days=1)).strftime("%Y-%m-%d")
        time_end = (week_end + timedelta(days=1)).strftime("%Y-%m-%d")
        
        try:
            query_string = f"SELECT * FROM HV_GIAYTORN \
                            LEFT JOIN GIAYTORN ON GIAYTORN.MaLoai = HV_GIAYTORN.MaLoai  \
                            LEFT JOIN DSDANGKY ON DSDANGKY.STT = HV_GIAYTORN.STTDaDuyet    \
                            LEFT JOIN HOCVIEN ON HOCVIEN.MaHV = DSDANGKY.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE TRANGTHAIXD > 0 AND \
                            (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}') \
                            AND DSDANGKY.MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_SttGiayToRN], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-giay-to-RN-hoc-vien-by-stt')
    def get_giay_to_RN_hoc_vien_by_stt(self, request):
        """
        API này dùng để thông tin giấy tờ ra ngoài qua số thứ tự giấy tờ ra ngoài.
        """
        sttGiayToRN = request.query_params.get('sttGiayToRN')

        try:
            query_string = f"SELECT * FROM HV_GIAYTORN \
                            LEFT JOIN GIAYTORN ON GIAYTORN.MaLoai = HV_GIAYTORN.MaLoai  \
                            LEFT JOIN DSDANGKY ON DSDANGKY.STT = HV_GIAYTORN.STTDaDuyet    \
                            LEFT JOIN HOCVIEN ON HOCVIEN.MaHV = DSDANGKY.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE TRANGTHAIXD > 0 AND STTGiayTo= %s  "
            obj = generics_cursor.getDictFromQuery(
                query_string, [sttGiayToRN])
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'ma_loai': openapi.Schema(type=openapi.TYPE_INTEGER,description="Mã loại giấy tờ"),
            'stt_da_duyet': openapi.Schema(type=openapi.TYPE_INTEGER,description="Số thứ tự trong danh sách học viên được duyệt"),
            'so_ve': openapi.Schema(type=openapi.TYPE_INTEGER,description="Mã số vé"),
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-tao-giay-to-RN-hoc-vien')
    def post_tao_giay_to_RN_hoc_vien(self, request):
        """
        API này dùng để thêm loại giấy tờ ra ngoài. Điền số vé nếu là thẻ gắn chip, còn không để trống.
        """
        dataDict = request.data
        ma_loai = dataDict.get("ma_loai")       
        stt_da_duyet = dataDict.get("stt_da_duyet")       
        so_ve = dataDict.get("so_ve")       
        try:             
            query_string = f'INSERT INTO HV_GIAYTORN("MaLoai","STTDaDuyet","SoVe") VALUES (%s,%s,%s)'
            with connection.cursor() as cursor:
                cursor.execute(query_string, [ma_loai,stt_da_duyet,so_ve])
                rows_affected = cursor.rowcount
                stt = cursor.lastrowid
            if rows_affected == 0:
                return Response(data={"status": False,"msg":"Có lỗi xảy ra"}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True,"msg":stt}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(method='delete', manual_parameters=[sw_SttGiayToRN], responses=get_list_person_response)
    @action(methods=['DELETE'], detail=False, url_path='delete-giay-to-RN-hoc-vien')
    def delete_giay_to_RN_hoc_vien(self, request):
        """
        API này dùng để xóa một giấy tờ ra ngoài của học viên
        """
        sttGiayToRN = request.query_params.get('sttGiayToRN')
        try:
            query_string = f"DELETE FROM HV_GIAYTORN WHERE STTGiayTo = %s"
            param = [sttGiayToRN]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)            
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'STT': openapi.Schema(type=openapi.TYPE_INTEGER,description="Số thứ tự giấy tờ", default=23),
            'maLoaiGiayTo': openapi.Schema(type=openapi.TYPE_INTEGER, description="Mã loại giấy tờ", default=1),
            'SoVe': openapi.Schema(type=openapi.TYPE_INTEGER,description="Số vé", default=23),
        }
    ), responses=post_list_person_response)
    @action(methods=['PUT'], detail=False, url_path='put-thay-doi-giay-to-RN-HV')
    def put_thay_doi_giay_to_RN_HV(self, request):
        """
        API này dùng để  thay đổi thông tin giấy tờ ra ngoài của học viên
        """
        dataDict = request.data
        try:
            STT = dataDict.get("STT")
            maLoaiGiayTo = dataDict.get("maLoaiGiayTo")
            SoVe = dataDict.get("SoVe")           

            query_string = f'UPDATE HV_GIAYTORN SET MaLoai = %s, SoVe = %s WHERE STTGiayTo = %s;'
            param = [maLoaiGiayTo,SoVe,STT]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

class VeBinhViewSet(viewsets.ViewSet):
    """
    Interact with UserCam
    """

    permission_classes = [VeBinhPermission]

    # all swagger's parameters should be defined here
    sw_page = openapi.Parameter(
        name='page', type=openapi.TYPE_STRING, description="Page number", in_=openapi.IN_QUERY)
    sw_size = openapi.Parameter(
        name='size', type=openapi.TYPE_STRING, description="Number of results to return per page", in_=openapi.IN_QUERY)
    sw_TimeStartGo = openapi.Parameter(
        name='timeStartGo', type=openapi.TYPE_STRING, description="Thời gian đi", default="2023-06-21 16:30", in_=openapi.IN_QUERY)
    sw_TimeStart = openapi.Parameter(
        name='timeStart', type=openapi.TYPE_STRING, description="Thời gian bắt đầu", default="2023-06-23", in_=openapi.IN_QUERY)
    sw_TimeEnd = openapi.Parameter(
        name='timeEnd', type=openapi.TYPE_STRING, description="Thời gian kết thúc", default="2023-06-25", in_=openapi.IN_QUERY)
    sw_DonViID = openapi.Parameter(
        name='donViID', type=openapi.TYPE_STRING, description="Mã đơn vị ( lớp, đại đội, tiểu đoàn)", default="DD155", in_=openapi.IN_QUERY)
    sw_MaHV = openapi.Parameter(
        name='maHV', type=openapi.TYPE_STRING, description="MaHV", default="201901058", in_=openapi.IN_QUERY)
    sw_SttDangKy = openapi.Parameter(
        name='sttDangKy', type=openapi.TYPE_INTEGER, description="Số thứ tự đăng ký", default=15, in_=openapi.IN_QUERY)
    sw_SttCamTrai = openapi.Parameter(
        name='sttCamTrai', type=openapi.TYPE_INTEGER, description="Số thứ tự cấm trại", default=15, in_=openapi.IN_QUERY)

    get_list_person_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_204_NO_CONTENT: 'NO_CONTENT',
        status.HTTP_200_OK: 'JSON',
    }

    post_list_person_response = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'INTERNAL_SERVER_ERROR',
        status.HTTP_304_NOT_MODIFIED: 'NOT_MODIFIED',
        status.HTTP_200_OK: 'JSON',
    }

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-loai-loi_vi_pham')
    def get_list_loai_loi_vi_pham(self, request):
        """
        API này dùng để lấy danh sách các loại giấy tờ ra ngoài.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')

        try:
            query_string = f"SELECT * FROM LOIVIPHAM"
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size,sw_TimeStart,sw_TimeEnd], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-vao-ra-cong')
    def get_list_danh_sach_vao_ra_cong(self, request):
        """
        API này dùng để lấy danh sách học viên vào ra cổng trong khoảng ngày nào đó.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        timeStart = request.query_params.get('timeStart')
        timeEnd = request.query_params.get('timeEnd')
        try:
            query_string = f'SELECT * FROM VAORACONG \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_GIAYTORN.STTDaDuyet = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE "{timeStart}" <= DATE(TG_RA) AND DATE(TG_RA) <= "{timeEnd}" \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size,sw_DonViID,sw_TimeStart,sw_TimeEnd], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-vao-ra-cong-theo-don-vi')
    def get_list_danh_sach_vao_ra_cong_theo_don_vi(self, request):
        """
        API này dùng để lấy danh sách học viên vào ra cổng trong khoảng ngày nào đó.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        donViID = str(request.query_params.get('donViID'))
        timeStart = request.query_params.get('timeStart')
        timeEnd = request.query_params.get('timeEnd')
        try:
            query_string = f'SELECT * FROM VAORACONG \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_GIAYTORN.STTDaDuyet = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE "{timeStart}" <= DATE(TG_RA) AND DATE(TG_RA) <= "{timeEnd}" AND \
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s) \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID,donViID,donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)


    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-ra-ngoai-chua-vao')
    def get_list_danh_sach_ra_ngoai_chua_vao(self, request):
        """
        API này dùng để lấy danh sách học viên vào đi ra ngoài nhưng chưa vào.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        try:
            query_string = f'SELECT * FROM VAORACONG \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_GIAYTORN.STTDaDuyet = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE TG_VAO = "" OR TG_Vao IS NULL \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size,sw_DonViID], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-danh-sach-ra-ngoai-chua-vao-theo-don-vi')
    def get_list_danh_sach_ra_ngoai_chua_vao_theo_don_vi(self, request):
        """
        API này dùng để lấy danh sách học viên vào đi ra ngoài nhưng chưa vào theo đơn vị.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        donViID = str(request.query_params.get('donViID'))

        try:
            query_string = f'SELECT * FROM VAORACONG \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_GIAYTORN.STTDaDuyet = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE TG_VAO = "" OR TG_Vao IS NULL AND\
                            PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s) \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID,donViID,donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'STTGiayTo': openapi.Schema(type=openapi.TYPE_INTEGER,description="Số thứ tự giấy tờ ra ngoài", default=23),
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-bat-dau-ra-cong')
    def post_bat_dau_ra_cong(self, request):
        """
        API này dùng để  thay đổi thông tin giấy tờ ra ngoài của học viên
        """
        dataDict = request.data
        try:
            time_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            STTGiayTo = dataDict.get("STTGiayTo")
            query_string = f'INSERT INTO VAORACONG("STTGiayTo","TG_Ra") VALUES (%s,%s);'
            param = [STTGiayTo,time_start]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', manual_parameters=[], request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, required=None,
        properties={
            'STTGiayTo': openapi.Schema(type=openapi.TYPE_INTEGER,description="Số thứ tự giấy tờ", default=23),
        }
    ), responses=post_list_person_response)
    @action(methods=['POST'], detail=False, url_path='post-vao-cong')
    def post_vao_cong(self, request):
        """
        API này dùng để  thay đổi thông tin giấy tờ ra ngoài của học viên
        """
        dataDict = request.data
        try:
            time_end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            STTGiayTo = dataDict.get("STTGiayTo")
            query_string = f'UPDATE VAORACONG SET TG_Vao = %s WHERE STTGiayTo= %s'
            param = [time_end,STTGiayTo]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
                print(rows_affected)
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size,sw_DonViID], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-loi-vi-pham-theo-theo-don-vi')
    def get_list_loi_vi_pham_theo_theo_don_vi(self, request):
        """
        API này dùng để lấy danh sách học viên vào đi ra ngoài nhưng chưa vào theo đơn vị.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')
        donViID = str(request.query_params.get('donViID'))

        try:
            query_string = f'SELECT * FROM HV_VIPHAM \
                            LEFT JOIN LOIVIPHAM ON HV_VIPHAM.MaLoiVP = LOIVIPHAM.MaLoiVP \
                            LEFT JOIN VAORACONG ON VAORACONG.STTRaNgoai = HV_VIPHAM.STTRaNgoai \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_VIPHAM.STTRaNgoai = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            WHERE PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s) \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID,donViID,donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get', manual_parameters=[sw_page,sw_size], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-loi-vi-pham-')
    def get_list_loi_vi_pham(self, request):
        """
        API này dùng để lấy danh sách học viên vi pham khi vào ra cổng.
        """
        page = request.query_params.get('page')
        size = request.query_params.get('size')

        try:
            query_string = f'SELECT * FROM HV_VIPHAM \
                            LEFT JOIN LOIVIPHAM ON HV_VIPHAM.MaLoiVP = LOIVIPHAM.MaLoiVP \
                            LEFT JOIN VAORACONG ON VAORACONG.STTRaNgoai = HV_VIPHAM.STTRaNgoai \
                            LEFT JOIN HV_GIAYTORN ON VAORACONG.STTGiayTo = HV_GIAYTORN.STTGiayTo \
                            LEFT JOIN GIAYTORN ON HV_GIAYTORN.MaLoai = GIAYTORN.MaLoai \
                            LEFT JOIN DSDANGKY ON HV_VIPHAM.STTRaNgoai = DSDANGKY.STT \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MaHV = HOCVIEN.MaHV \
                            LEFT JOIN PERSON ON PERSON.PersonID = HOCVIEN.PERSONID \
                            LEFT JOIN DONVI ON DONVI.DonViID = PERSON.DonViID \
                            LEFT JOIN TIEUDOAN ON TIEUDOAN.MaTD = DONVI.MaTieuDoan \
                            LEFT JOIN DAIDOI ON DAIDOI.MaDD = DONVI.MaDaiDoi \
                            LEFT JOIN LOP ON LOP.MaLop = DONVI.MaLop \
                            ORDER BY TG_Ra DESC,DONVI.MaLop,DONVI.MaDaiDoi,DONVI.MaTieuDoan'
            obj = generics_cursor.getDictFromQuery(
                query_string, [], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)