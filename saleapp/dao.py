import hashlib
from flask_login import current_user
from sqlalchemy import extract, func
from saleapp import utils
from saleapp.models import *
from saleapp.utils import count_cart, total_bill


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register(name, username, password, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=username, username=username.strip(), password=password, email=email, user_role=UserRole.KHACHHANG)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_schedule(ngayTao, tenBN, **kwargs):
    list = DanhSachLichKham.query.filter(DanhSachLichKham.ngayTao == ngayTao).first()

    if list is None:
        list = DanhSachLichKham(ngayTao=ngayTao)
        db.session.add(list)
        db.session.commit()

        d = DanhSachDatLich(DSLichKham_id=list.id, user=current_user,
                            tenBN=tenBN.strip(),
                            SDT=kwargs.get('SDT'),
                            gioiTinh=kwargs.get('gioiTinh'),
                            diaChi=kwargs.get('diaChi'),
                            namSinh=kwargs.get('namSinh'))
    else:
        d = DanhSachDatLich(DSLichKham_id=list.id, user=current_user,
                            tenBN=tenBN.strip(),
                            SDT=kwargs.get('SDT'),
                            gioiTinh=kwargs.get('gioiTinh'),
                            diaChi=kwargs.get('diaChi'),
                            namSinh=kwargs.get('namSinh'))

    db.session.add(d)
    db.session.commit()


def count_schedule_by_date(ngayTao='2022-12-12'):
    return db.session.query(DanhSachLichKham.id, DanhSachLichKham.ngayTao) \
        .join(DanhSachDatLich, DanhSachDatLich.DSLichKham_id.__eq__(DanhSachLichKham.id)) \
        .filter(DanhSachLichKham.ngayTao == ngayTao) \
        .group_by(DanhSachDatLich.id, DanhSachLichKham.ngayTao).all()


def check_login(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()

def get_medicine_by_id(id):
    return Thuoc.query.get(id)


def add_MedicalBill(fullname, ngaylap, chanDoan, trieuChung, cart):
    medicinalBill = PhieuKhamBenh(
        fullname=fullname,
        ngaylap=ngaylap,
        chanDoan=chanDoan,
        trieuChung=trieuChung,
        user_id=current_user.id)

    db.session.add(medicinalBill)
    db.session.commit()
    # tạo một cái bill
    add_Bills(medicalBill=medicinalBill, cart=cart)
    # add medicalBillDetail
    for c in cart.values():
        medicalBillDetail = ChiTietDonThuoc(phieuKhamBenh_id=medicinalBill.id,
                                            Thuoc_id=c['id'],
                                            soLuong=c['soLuong'])
        db.session.add(medicalBillDetail)
    db.session.commit()



def add_Bills(medicalBill, cart):
    user = get_user_by_id(medicalBill.user_id)
    bills = HoaDon(tenHD=medicalBill.fullname, ngayLapHD=medicalBill.ngaylap,
                  tienThuoc=utils.count_cart(cart),
                  tienKham=100000,
                  user_id=user.id,
                  phieuKhamBenh_id=medicalBill.id)
    db.session.add(bills)
    db.session.commit()


# def bill_stats(month):
#     p = total_bill(month)
#     q = p[0]
#     x = q[0]
#
#     p = db.session.query(extract('day', HoaDon.ngayLapHD), func.sum(HoaDon.tienThuoc + HoaDon.tienKham),
#                          func.count(HoaDon.phieuKhamBenh_id),
#                          func.round(((func.sum(HoaDon.tienThuoc + HoaDon.tienKham) / x) * 100), 2)) \
#         .filter(extract('month', HoaDon.ngayLapHD) == month) \
#         .group_by(extract('day', HoaDon.ngayLapHD)) \
#         .order_by(extract('day', HoaDon.ngayLapHD))
#
#     return p.all()


def get_medicine_by_id(id):
    return Thuoc.query.get(id)

def search_medicine_bill_by_id(medicine_bill_id):
    return HoaDon.query.filter(HoaDon.phieuKhamBenh_id.__eq__(medicine_bill_id))





