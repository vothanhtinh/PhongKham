from datetime import datetime
from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user
from saleapp import app, dao, admin
from saleapp.decorators import annonynous_user
from saleapp.models import UserRole, Thuoc, HoaDon


def home():
    return render_template("base.html")


def introduce():
    return render_template("introduce.html")


def booking():
    return render_template("booking.html")


def book_schedule():
    err_msg = ""
    msg_success = ''
    full_patient = ''
    if request.method.__eq__('POST'):
        tenBN = request.form.get('tenBN')
        SDT = request.form.get('SDT')
        namSinh = request.form.get('namSinh')
        diaChi = request.form.get('diaChi')
        gioiTinh = request.form.get('gioiTinh')
        ngayDL = request.form.get('ngayDL')

        try:
            count = dao.count_schedule_by_date(ngayDL)
            dem = 0
            for c in count:
                dem = dem + 1
            if dem < 40:
                dao.add_schedule(ngayTao=ngayDL, tenBN=tenBN, SDT=SDT, namSinh=namSinh, diaChi=diaChi,
                                 gioiTinh=gioiTinh)
            else:
                full_patient = "Đủ 40 bệnh nhân trong ngày"
        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)
        else:
            msg_success = "Đặt lịch thành công"
    return render_template('booking.html', err_msg=err_msg, msg_success=msg_success,
                           full_patient=full_patient)


@annonynous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['registerPassword']
        confirm = request.form['registerConfirmPassword']
        if password.__eq__(confirm):
            try:
                dao.register(name=request.form['registerName'],
                             email=request.form['registerEmail'],
                             password=password,
                             username=request.form['registerName'])

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')


def doctor_login():
    err_msg = ''
    msg_success = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password, role=UserRole.BACSI)
        if user:
            login_user(user=user)

        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!!!'

    medicine = Thuoc.query.order_by(Thuoc.name).all()
    return render_template('phieu_kham.html', err_msg=err_msg, msg_success=msg_success, Thuoc=medicine)


def doctor_logout():
    logout_user()
    return redirect('/doctor-login')


def add_phieu_kham():
    err_msg = ""
    msg_success = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('name')
        ngaylap = request.form.get('ngaylap')
        created_date = datetime.now()
        trieuChung = request.form.get('trieuChung')
        chanDoan = request.form.get('chanDoan')
        try:
            key = app.config['CART_KEY']
            cart = session.get(key)
            dao.add_medical_bill(fullname=fullname, ngay_lap=created_date, chan_doan=chanDoan, trieu_chung=trieuChung,
                                 cart=cart)
        except Exception as err:
            err_msg =  str(err)
        else:
            msg_success = "Lưu phiếu thành công"
        session[key] = {}
    medicine = Thuoc.query.order_by(Thuoc.name).all()
    return render_template('phieu_kham.html', err_msg=err_msg, Thuoc=medicine, msg_success=msg_success)


def update_quantity():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')
    try:
        key = app.config['CART_KEY']
        cart = session.get(key)
        if cart and id in cart:
            cart[id]['soLuong'] = quantity
        session[key] = cart
        print(cart)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


def add_medicine_to_cart():
    data = request.json
    thuoc_id = int(data.get('id'))
    p = dao.get_medicine_by_id(id=thuoc_id)
    giaThuoc = p.giaThuoc
    key = app.config['CART_KEY']
    cart = {}
    if key in session:
        cart = session[key]
    if thuoc_id in cart:
        cart[thuoc_id]['soLuong'] = cart[thuoc_id]['soLuong'] + 1
    else:
        cart[str(thuoc_id)] = {
            'id': thuoc_id,
            'giaThuoc': giaThuoc,
            'soLuong': 1
        }
    print(cart)
    session[key] = cart

    return jsonify({
        'donViThuoc_id': p.donViThuoc_id,
        'CachSD': p.CachSD,
        'thuoc_id': p.id
    })


@annonynous_user
def staff_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password, role=UserRole.NHANVIENTHANHTOAN)
        if user:
            login_user(user=user)
            return redirect('/bills_staff')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!!!'

    return render_template('hoadon.html', err_msg=err_msg)


def staff_logout():
    logout_user()
    return redirect("/staff_login")


def bills_staff():
    hoadon = HoaDon.query.all()
    medicine_bill_id = request.form.get('medicine_bill_id')
    if medicine_bill_id:
        return render_template('hoadon.html', bills=dao.search_medicine_bill_by_id(medicine_bill_id))
    return render_template('hoadon.html', bills=hoadon)


def pay():
    data = request.json
    id = str(data.get('id'))
    try:
        dao.reload_state_pay(id)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


def timKiem():
    name = []
    quantity = []
    data = request.json
    fullname = str(data.get('fullname'))

    search = dao.timKiem(fullname)

    for x in search:
        name.append(x[1])
        quantity.append(x[2])

    return jsonify({
        'name': name,
        'quantity': quantity
    })
