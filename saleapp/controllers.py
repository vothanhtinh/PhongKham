
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required
from saleapp import dao, app
from saleapp.decorators import annonynous_user
from saleapp.models import UserRole, Thuoc, HoaDon


