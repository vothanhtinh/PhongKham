from datetime import datetime
from saleapp import app
from flask import render_template, request, redirect, session, jsonify
from flask_login import current_user, login_user, logout_user
from saleapp import app, dao, admin, login_manager, utils
from saleapp.decorators import annonynous_user
from saleapp.models import UserRole, Thuoc


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/introduce")
def introduce():
    return render_template("introduce.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/booking", methods=['POST'])
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
            if dem < 30:
                dao.add_schedule(ngayTao=ngayDL, tenBN=tenBN, SDT=SDT, namSinh=namSinh, diaChi=diaChi,
                                 gioiTinh=gioiTinh)
            else:
                full_patient = "Đủ 30 bệnh nhân trong ngày"
        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)
        else:
            msg_success = "Đặt lịch thành công"
            # message = client.messages.create(
            #     messaging_service_sid='MG7d95f17888d4b32c271025663602add6',
            #     body='Đặt lịch thành công',
            #     to='+84769669147'
            # )

    return render_template('booking.html', err_msg=err_msg, msg_success=msg_success,
                           full_patient=full_patient)


@app.route("/login", methods=['get', 'post'])
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


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route("/register", methods=['get', 'post'])
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


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/admin-login", methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')


@app.route("/doctor-login", methods=['get', 'post'])
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

    medicine = Thuoc.query.all()
    return render_template('phieu_kham.html', err_msg=err_msg, msg_success=msg_success, Thuoc=medicine)


@app.route("/doctor-logout")
def doctor_logout():
    logout_user()
    return redirect('/doctor-login')


@app.route("/add-phieu-kham", methods=['get', 'post'])
def add_phieu_kham():
    err_msg = ""
    msg_success = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('name')
        ngaylap = request.form.get('ngaylap')
        created_date = datetime.now()
        trieuChung = request.form.get('trieuChung')
        chanDoan = request.form.get('chanDoan')
        key = app.config['CART_KEY']
        cart = session.get(key) if key in session else {}
        dao.add_MedicalBill(fullname=fullname, created_date=created_date, chanDoan=chanDoan, trieuChung=trieuChung,
                                cart=cart)
        # except Exception as err:
        #     err_msg = "Hệ thống báo lỗi " + str(err)
        # else:
        #     msg_success = "Lưu phiếu thành công"
        #     del session[key]
    return render_template('phieu_kham.html', err_msg=err_msg)


@app.route("/api/add-medicine-to-cart", methods=['POST'])
def add_medicine_to_cart():
    data = request.json
    id = str(data.get('id'))

    p = dao.get_medicine_by_id(id=id)
    giaThuoc = p.giaThuoc

    key = app.config['CART_KEY']
    # ban đầu giỏ rỗng
    cart = {}
    # kiểm tra đã có giỏ hàng chưa
    if key in session:
        cart = session[key]  # có rồi

    if id in cart:
        cart[id]['soLuong'] = cart[id]['soLuong'] + 1
    else:
        cart[id] = {
            'id': id,
            'giaThuoc': giaThuoc,
            'soLuong': 1
        }
    session[key] = cart

    unit = p.donViThuoc_id
    CachSD = p.CachSD

    return jsonify({
        'donViThuoc_id': unit,
        'CachSD': CachSD
    })


if __name__ == "__main__":
    app.run(debug=True)
