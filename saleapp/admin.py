from datetime import datetime
from flask import redirect, request
from saleapp import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from saleapp.models import UserRole, Thuoc, DanhMuc, DonViThuoc, User, DanhSachDatLich


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class UserView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    # column_filters = ['fullname', 'username']
    # column_searchable_list = ['fullname', 'username']
    # column_exclude_list = ['active', 'joined_date']
    # column_labels = {
    #     'id': 'STT',
    #     'fullname': 'Họ và tên',
    #     'username': 'Tên đăng nhập',
    #     'password': 'Mật khẩu',
    #     'user_role': 'Quyền',
    #     'joined_date': 'Ngày tạo'
    # }
    # form_excluded_columns = ['active', 'details', 'bills', 'joined_date']

class ListDetailView(AuthenticatedModelView):
    can_create = False
    edit_modal = True
    column_labels = {
        # 'listschedule': 'Ngày khám',
        # 'fullname': 'Tên bệnh nhân',
        # 'gender': 'Giới tính',
        # 'year_born': 'Năm sinh',
        # 'address': 'Địa chỉ',
        # 'user': 'Tên người đăng kí'
    }
    # column_exclude_list = ['user']
    # form_excluded_columns = ['user']

class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    # column_searchable_list = ['id', '']
    # column_labels = {
    #     'id': 'Mã đơn vị',
    #     'name': 'Tên đơn vị',
    #     'medicines': 'Thuốc'
    # }
    # form_excluded_columns = ['medicines']


class CateView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    # column_searchable_list = ['id', 'name']
    # column_labels = {
    #     'id': 'Mã loại thuốc',
    #     'name': 'Tên loại thuốc'
    # }
    # form_excluded_columns = ['medicine']

class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    # column_searchable_list = ['id', 'name', 'donViThuoc_id']
    # column_filters = 'id', 'name', 'medicalbill'
    # column_display_all_relations = True
    # column_exclude_list = ['medicalbill']
    # column_labels = {
    #     'id': 'Mã thuốc',
    #     'name': 'Tên thuốc',
    #     'donViThuoc_id': 'Đơn vị tính',
    #     'giaThuoc': 'Giá tiền',
    #     'CachSD': 'Cách dùng',
    #     'unitmedicine': 'Đơn vị tính',
    #     'muc': 'Loại thuốc',
    #     'medicalbill': 'Đơn thuốc'
    # }
    # form_excluded_columns = ['medicalbill']

# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         total = 0
#         month = request.args.get('month', datetime.now().month)
#         return self.render('admin/index.html', month_stats=dao.bill_stats(month), total=dao.total_bill(month))


admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4')

# admin.add_view(ListDetailView(DanhSachDatLich, db.session, name='Danh sách ngày khám', DanhMuc='Quản lý danh sách khám'))
# admin.add_sub_DanhMuc(name='medicine_manager ', parent_name='Quản lý danh sách khám')
#
# admin.add_view(UnitView(DonViThuoc, db.session, name='Đơn vị tính', DanhMuc='Quản lý thuốc'))
# admin.add_view(CateView(DanhMuc, db.session, name='Loại thuốc', DanhMuc='Quản lý thuốc'))
# admin.add_view(MedicineView(Thuoc, db.session, name='Thuốc', DanhMuc='Quản lý thuốc'))
# admin.add_sub_DanhMuc(name='medicine_manager ', parent_name='Quản lý thuốc')

# admin.add_view(UserView(User, db.session, name='Người dùng'))
# admin.add_view(Stats(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
