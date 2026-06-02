"""
Dashboard blueprint for displaying user statistics and recent QR codes
Shows user profile information and quick access to QR generation
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import QRCode
from sqlalchemy import desc

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """
    Dashboard home page
    Displays user statistics and recent QR codes
    """
    
    # Get statistics
    total_qr_codes = current_user.qr_codes.count()
    
    # Get QR code types breakdown
    qr_types = {}
    qr_codes = current_user.qr_codes.all()
    
    for qr in qr_codes:
        qr_types[qr.qr_type] = qr_types.get(qr.qr_type, 0) + 1
    
    # Get recent 5 QR codes
    recent_qr_codes = current_user.qr_codes.order_by(
        desc(QRCode.created_at)
    ).limit(5).all()
    
    # Prepare statistics data
    stats = {
        'total_qr_codes': total_qr_codes,
        'qr_types': qr_types,
        'type_count': len(qr_types),
        'url_count': qr_types.get('url', 0),
        'text_count': qr_types.get('text', 0),
        'email_count': qr_types.get('email', 0),
        'phone_count': qr_types.get('phone', 0),
        'wifi_count': qr_types.get('wifi', 0),
    }
    
    return render_template(
        'dashboard.html',
        stats=stats,
        recent_qr_codes=recent_qr_codes,
        user=current_user
    )
