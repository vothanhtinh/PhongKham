from saleapp import app, dao, admin, login_manager, controllers


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


app.add_url_rule("/", "home", controllers.home)
app.add_url_rule("/introduce", "introduce", controllers.introduce)
app.add_url_rule("/booking", "booking", controllers.booking)
app.add_url_rule("/booking", "book_schedule", controllers.book_schedule, methods=['POST'])
app.add_url_rule("/login", "login_my_user", controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', "logout_my_user", controllers.logout_my_user)
app.add_url_rule("/register", "register", controllers.register, methods=['get', 'post'])
app.add_url_rule("/admin-login", "signin_admin", controllers.signin_admin, methods=['post'])
app.add_url_rule("/doctor-login", "doctor_login", controllers.doctor_login, methods=['get', 'post'])
app.add_url_rule("/doctor-logout", "doctor_logout", controllers.doctor_logout)
app.add_url_rule("/add-phieu-kham", "add_phieu_kham", controllers.add_phieu_kham, methods=['get', 'post'])
app.add_url_rule("/api/update-quantity", "update_quantity", controllers.update_quantity, methods=['put'])
app.add_url_rule("/api/add-medicine-to-cart", "add_medicine_to_cart", controllers.add_medicine_to_cart,
                 methods=['POST'])
app.add_url_rule("/staff_login", " staff_login", controllers.staff_login, methods=['get', 'post'])
app.add_url_rule("/staff_logout", "staff_logout", controllers.staff_logout)
app.add_url_rule("/bills_staff/", "bills_staff", controllers.bills_staff, methods=['get', 'post'])
app.add_url_rule("/api/pay", "pay", controllers.pay, methods=['post'])
app.add_url_rule("/api/timKiem", "timKiem", controllers.timKiem, methods=['post'])

if __name__ == "__main__":
    app.run(debug=True)
