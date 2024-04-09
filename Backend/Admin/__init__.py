from flask import Blueprint
from Backend.Admin.AdMonAdminController import AdminController, admin_controller_bp

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../../Frontend/Templates')
admin_bp.register_blueprint(admin_controller_bp)

