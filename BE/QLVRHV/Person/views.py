
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


class PersonPermission(custom_permission.CustomPermissions):
    def __init__(self):
        super().__init__()

    # def get_allowed_methods(self, username):
    #     ## query in database here
    #     username = username
    #     return ['GET']


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
    sw_TimeStart = openapi.Parameter(
        name='timeStart', type=openapi.TYPE_STRING, description="Thời gian đi", default="12-03-2023", in_=openapi.IN_QUERY)
    sw_TimeBetween = openapi.Parameter(
        name='timeBetween', type=openapi.TYPE_STRING, description="Time trong tuần", default="12-03-2023", in_=openapi.IN_QUERY)
    sw_NameHV = openapi.Parameter(
        name='nameHV', type=openapi.TYPE_STRING, description="Tên học viên", default="Anh", in_=openapi.IN_QUERY)

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
                            WHERE PERSON.DonViID IN (SELECT DonViID FROM DONVI WHERE DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s)"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
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

    @swagger_auto_schema(method='get', manual_parameters=[sw_DonViID,sw_MaHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-info-hoc-vien-by-id')
    def get_info_hoc_vien_by_id(self, request):
        """
        API này dùng để tìm kiếm theo mã học viên của một đơn vị cụ thể nào đó( có thể là lớp,đại đội, tiểu đoàn). 
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

    @swagger_auto_schema(method='get', manual_parameters=[sw_page, sw_size,sw_MaHV], responses=get_list_person_response)
    @action(methods=['GET'], detail=False, url_path='get-list-ket-qua-ren-luyen-by-id')
    def get_list_ket_qua_ren_luyen_by_id(self, request):
        """
        API này dùng lấy một list danh sách kết quả rèn luyện học viên sắp xếp theo thời gian giảm dần
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
        return Response({"permission": int(roleId)}, status=status.HTTP_200_OK)

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
        API này dùng để lấy danh sách các học viên bị cấm trại trong một đơn vị nào đó. timeBetween là lựa chọn, nếu không nhập sẽ lấy thời gian ngày hôm nay. API sẽ tìm tất cả các học viên bị cấm trại từ đầu tuần đến cuối tuần nằm trong timeBetween đó.
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
            query_string = f"SELECT * FROM QUYETDINHCAMTRAI WHERE \
                            ((TG_BatDau BETWEEN '{time_start}'AND '{time_end}') OR \
                            (TG_KetThuc BETWEEN '{time_start}'AND '{time_end}') OR  \
                            (TG_BatDau <= '{time_start}' AND TG_KetThuc >= '{time_end}'))\
                            AND MAHV IN (SELECT MAHV FROM HOCVIEN,PERSON,DONVI WHERE HOCVIEN.personID = PERSON.PersonID AND DONVI.DonViID=PERSON.DonViID\
                            AND (DONVI.MaLop = %s OR DONVI.MaDaiDoi= %s OR DONVI.MaTieuDoan =%s))"
            obj = generics_cursor.getDictFromQuery(
                query_string, [donViID, donViID, donViID], page=page, size=size)
            if obj is None:
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR", e)
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=obj, status=status.HTTP_200_OK)

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
        API này dùng để đăng ký học viên ra ngoài. Mặc định trái thái xét duyệt sẽ là 0. Đối với hình thức ra ngoài, nhập 0 nếu là tranh thủ, nhập 1 nếu là tranh thủ miền Nam, nhập 2 nếu là ra ngoài. 
        """
        dataDict = request.data
        print(dataDict)
        try:
            hinhThucRN = int(dataDict.get("hinh_thuc_RN"))
            if hinhThucRN == 0:
                hinhThucRN = "Tranh thủ miền Nam"
            elif hinhThucRN == 1:
                hinhThucRN = "Tranh thủ miền Bắc"
            else:
                hinhThucRN="Ra ngoài"


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
            query_string = f'INSERT INTO DSDANGKY("HinhThucRN","DiaDiem","ThoiGianDi","ThoiGianVe","MaHV","TRANGTHAIXD") VALUES (%s,%s,%s,%s,%s,0);'
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
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
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
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE (TRANGTHAIXD >= HinhThucRN.QUYEN ) AND \
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
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
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
        try:
            query_string = f"SELECT DSDANGKY.STT, HinhThucRN.Loai, DSDANGKY.DiaDiem, DSDANGKY.ThoiGianDi, DSDANGKY.ThoiGianVe,PERSON.HoTen, DSDANGKY.TRANGTHAIXD FROM DSDANGKY \
                            LEFT JOIN HOCVIEN ON DSDANGKY.MAHV = HOCVIEN.MAHV \
                            LEFT JOIN PERSON ON HOCVIEN.PersonID = PERSON.PersonID \
                            LEFT JOIN HinhThucRN ON DSDANGKY.HinhThucRN = HinhThucRN.STT \
                            WHERE (TRANGTHAIXD >= 0) AND (TRANGTHAIXD < {permission}) AND  \
                            (ThoiGianDi BETWEEN '{time_start}'AND '{time_end}')  AND\
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