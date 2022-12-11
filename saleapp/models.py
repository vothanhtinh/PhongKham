from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class BacSi(BaseModel):

    name = Column(String(50), nullable=False)
    diaChi = Column(String(200))
    gioiTinh = Column(String(50))
    SDT = Column(String(100))
    PhieuKham_id = relationship('PhieuKham', backref='BacSi', lazy=True)


    def __str__(self):
        return self.name


class YTa(BaseModel):
    name = Column(String(50), nullable=False)
    diaChi = Column(String(200))
    gioiTinh = Column(String(50))
    SDT = Column(String(100))
    DSKhamBenh_id = relationship('DSKhamBenh', backref='YTa', lazy=True)


    def __str__(self):
        return self.name

class DSKhamBenh(BaseModel):
    soLuongBN= Column(Integer,default=0)
    ngaylap =Column(DateTime, default=datetime.now())
    BenhNhan_id  = relationship('BenhNhan', backref='DSKhamBenh', lazy=True)
    PhieuKham_id  = relationship('PhieuKham', backref='DSKhamBenh', lazy=True)
    Yta_id = Column(Integer, ForeignKey(YTa.id), nullable=False)

class PhieuKham(BaseModel):
    chanDoan = Column(String(300))
    trieuChung = Column(String(300))
    ngaylap =Column(DateTime, default=datetime.now())
    DSKhamBenh_id = Column(Integer, ForeignKey(DSKhamBenh.id), nullable=False)
    BacSi_id = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    thuoc = relationship('Thuoc', secondary='ChiTietPhieuKham', lazy='subquery',
                        backref=backref('PhieuKham', lazy=True))

class Thuoc(BaseModel):
    tenThuoc = Column(String(300))
    giathuoc= Column(Float, default=0)
    DonViThuoc = relationship("DonViThuoc", uselist=False,backref="Thuoc")

class DonViThuoc(BaseModel):
    donVi=Column(String(100))
    Thuoc_id = Column(ForeignKey(Thuoc.id))



class ChiTietPhieuKham(BaseModel):
    Thuoc_id=  Column(Integer, ForeignKey(Thuoc.id), nullable=False, primary_key=True)
    PhieuKham_id= Column(Integer, ForeignKey(PhieuKham.id), nullable=False, primary_key=True)
    HoaDon_id = relationship('HoaDon', backref='ChiTietPhieuKham', uselist=False)
    tienKham=Column( Float, default=100000)
    tienthuoc= Column( Float, default=0)


class BenhNhan(BaseModel):
    name = Column(String(50), nullable=False)
    diaChi = Column(String(200))
    gioiTinh = Column(String(50))
    SDT = Column(String(100))
    DSKhamBenh_id = Column(Integer, ForeignKey(DSKhamBenh.id), nullable=False)
    def __str__(self):
        return self.name


class NhanVienThanhtoan(BaseModel):
    name = Column(String(50), nullable=False)
    diaChi = Column(String(200))
    gioiTinh = Column(String(50))
    SDT = Column(String(100))
    HoaDon_id  = relationship('HoaDon', backref='NhanVienThanhtoan', lazy=True)


    def __str__(self):
        return self.name



class QuanTri(BaseModel):
    name = Column(String(50), nullable=False)
    diaChi = Column(String(200))
    gioiTinh = Column(String(50))
    SDT = Column(String(100))

    def __str__(self):
        return self.name

class HoaDon(BaseModel):
    ngayLapHD= Column(String(100))
    tongTien=Column(Float,default=0 )
    NhanVienThanhtoan_id = Column(Integer, ForeignKey(NhanVienThanhtoan.id), nullable=False)
    ChiTietPhieuKham_id = Column(Integer, ForeignKey(ChiTietPhieuKham.id),unique=True)




















if __name__ == '__main__':
    with app.app_context():
        db.create_all()







