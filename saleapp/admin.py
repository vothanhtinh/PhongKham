from datetime import datetime
from flask import redirect, request
from saleapp import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from saleapp.models import UserRole, Thuoc, DanhMuc, DonViThuoc, User, DanhSachDatLich


class AuthenticatedModelView(ModelView):
    column_display_pk = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class UserView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    can_edit = False
    create_modal = True
    details_modal = True
    column_filters = ['username']
    column_searchable_list = ['username']
    column_exclude_list = ['active', 'ngayThamGia', 'password']
    column_labels = {
        'name': 'Họ và tên',
        'username': 'Tên đăng nhập',
        'user_role': 'Quyền',
        'joined_date': 'Ngày tạo'
    }
    # form_excluded_columns = ['active', 'details', 'bills', 'joined_date']


class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã đơn vị',
        'name': 'Tên đơn vị',
        # 'medicines': 'Thuốc'
    }
    form_excluded_columns = ['medicines']


class CateView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã loại thuốc',
        'name': 'Tên loại thuốc'
    }
    form_excluded_columns = ['medicine']


class MedicineView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_filters = 'id', 'name'
    column_display_all_relations = True
    column_exclude_list = ['phieuKhamBenh']
    column_labels = {
        'id': 'Mã thuốc',
        'name': 'Tên thuốc',
        'donViThuoc_id': 'Đơn vị tính',
        'giaThuoc': 'Giá tiền',
        'CachSD': 'Cách dùng',
        'DonViThuoc': 'Đơn vị thuốc',
        'danh_muc_thuoc': 'Danh Mục'
        # 'cates': 'Loại thuốc',
        # 'medicalbill': 'Đơn thuốc'
    }
    form_excluded_columns = ['phieuKhamBenh']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class ListDetailView(AuthenticatedModelView):
    can_create = False
    edit_modal = True
    column_labels = {
        'tenBN': 'Tên bệnh nhân',
        'gioiTinh': 'Giới tính',
        'namSinh': 'Năm sinh',
        'diaChi': 'Địa chỉ',
        'user': 'Tên người đăng kí'
    }
    column_exclude_list = ['user']
    form_excluded_columns = ['user']


class Stats(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        kw = request.args.get('kw')
        id = request.args.get('id')
        return self.render('admin/stats.html',
                           medi_month_stats=dao.medicine_month_stats(kw=kw, id=id, month=month)
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        total = 0
        month = request.args.get('month', datetime.now().month)
        return self.render('admin/index.html', month_stats=dao.bill_stats(month), total=dao.total_bill(month))


admin = Admin(app=app, name='QUẢN LÝ PHÒNG MẠCH', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(ListDetailView(DanhSachDatLich, db.session, name='Danh sách đặt lịch', category='Quản lý danh sách khám'))
admin.add_sub_category(name='medicine_manager ', parent_name='Quản lý danh sách khám')

admin.add_view(UnitView(DonViThuoc, db.session, name='Đơn vị tính', category='Quản lý thuốc'))
admin.add_view(CateView(DanhMuc, db.session, name='Loại thuốc', category='Quản lý thuốc'))
admin.add_view(MedicineView(Thuoc, db.session, name='Thuốc', category='Quản lý thuốc'))
admin.add_sub_category(name='medicine_manager ', parent_name='Quản lý thuốc')

admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(Stats(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))