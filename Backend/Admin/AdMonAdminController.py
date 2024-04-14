import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, render_template
from functools import wraps
from Backend.Models.QBmAdminModel import QBBiz
from Backend.Admin.AdMonBizLogic import GetAdminHomeData, GetAdminDashboardData, GetAdminAnalyticsData
from Backend.Connections.QBcDBConnector import db, bcrypt

admin_controller_bp = Blueprint('admin_controller', __name__)


class AdminController:
    @staticmethod
    @admin_controller_bp.route('/register', methods=['GET', 'POST'])
    def register_admin():
        if request.method == 'POST':
            username = request.json.get('username')
            email = request.json.get('email')
            password = request.json.get('password')

            # Check if the admin already exists
            existing_admin = QBBiz.query.filter_by(username=username).first()
            if existing_admin:
                return jsonify({'error': 'Username already exists'}), 400

            # Create a new admin
            new_admin = QBBiz(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password)
            )
            db.session.add(new_admin)
            db.session.commit()

            return jsonify({'message': 'Admin registered successfully'}), 201
        else:
            return render_template('AdminRegistration.html')

    @staticmethod
    @admin_controller_bp.route('/login', methods=['GET', 'POST'])
    def login_admin():
        if request.method == "POST":
            username = request.json.get('username')
            password = request.json.get('password')

            admin = QBBiz.query.filter_by(username=username).first()
            if admin and bcrypt.check_password_hash(admin.password, password):
                # Generate a JWT token
                payload = {
                    'admin_id': admin.id,
                    'exp': datetime.now() + timedelta(hours=24)
                }
                token = jwt.encode(payload, 'AdminQbBiz', algorithm='HS256')
                return jsonify({'token': token})
            else:
                return jsonify({'error': 'Invalid username or password'}), 401
        else:
            return render_template('AdminLogin.html')

    @staticmethod
    def admin_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'No token provided'}), 401

            try:
                payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
                admin_id = payload['admin_id']
            except jwt.exceptions.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

            # Check if the admin is valid and active
            admin = QBBiz.query.get(admin_id)
            if not admin or not admin.is_active:
                return jsonify({'error': 'Unauthorized'}), 403

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/home', methods=['GET', 'POST'])
    def admin_home():
        return render_template('AdminHome.html')

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/home/data', methods=['GET', 'POST'])
    def admin_home_data():
        home_data = GetAdminHomeData()
        return jsonify(home_data)

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/dashboard', methods=['GET', 'POST'])
    def admin_dashboard():
        return render_template('AdminDashboard.html')

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/dashboard/data', methods=['GET', 'POST'])
    def admin_dashboard_data():
        dashboard_data = GetAdminDashboardData()
        return jsonify(dashboard_data)

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/analytics', methods=['GET', 'POST'])
    def admin_analytics():
        return render_template('AdminAnalytics.html')

    @staticmethod
    @admin_required
    @admin_controller_bp.route('/analytics/data', methods=['GET', 'POST'])
    def admin_analytics_data():
        analytics_data = GetAdminAnalyticsData()
        return jsonify(analytics_data)
