"""
QR Code generation blueprint
Handles QR code generation for various content types (URL, text, email, phone, WiFi)
"""

import os
import io
import qrcode
from PIL import Image
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from models import db, QRCode

# Create QR generator blueprint
qr_bp = Blueprint('qr', __name__, url_prefix='/qr')


def get_safe_filename(filename):
    """
    Generate safe filename for QR code
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Safe filename with timestamp
    """
    import re
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    return f'{timestamp}_{filename[:30]}.png'


def generate_qr_code(content, qr_type, fg_color='#000000', bg_color='#FFFFFF', 
                     logo_path=None, qr_size=10):
    """
    Generate QR code image
    
    Args:
        content (str): Content to encode
        qr_type (str): Type of QR code
        fg_color (str): Foreground color (hex)
        bg_color (str): Background color (hex)
        logo_path (str): Path to logo image (optional)
        qr_size (int): Size of QR code boxes
        
    Returns:
        Image: PIL Image object of QR code
    """
    
    # Convert hex colors to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    fg_rgb = hex_to_rgb(fg_color)
    bg_rgb = hex_to_rgb(bg_color)
    
    # Prepare content based on type
    qr_content = prepare_qr_content(content, qr_type)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr_size,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    # Create QR image
    img = qr.make_image(fill_color=fg_rgb, back_color=bg_rgb)
    
    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            logo_width = img.size[0] // 5
            logo_height = (logo.size[1] * logo_width) // logo.size[0]
            logo = logo.resize((logo_width, logo_height))
            
            logo_position = (
                (img.size[0] - logo_width) // 2,
                (img.size[1] - logo_height) // 2
            )
            
            img.paste(logo, logo_position)
        except Exception as e:
            print(f'Error adding logo: {str(e)}')
    
    return img


def prepare_qr_content(content, qr_type):
    """
    Prepare content for QR encoding based on type
    
    Args:
        content (str): Raw content
        qr_type (str): Type of QR code
        
    Returns:
        str: Formatted content for QR encoding
    """
    
    if qr_type == 'url':
        if not content.startswith(('http://', 'https://')):
            content = 'https://' + content
        return content
    
    elif qr_type == 'email':
        return f'mailto:{content}'
    
    elif qr_type == 'phone':
        phone = ''.join(filter(str.isdigit, content))
        return f'tel:{phone}'
    
    elif qr_type == 'wifi':
        # Format: WIFI:T:WPA;S:SSID;P:PASSWORD;;
        try:
            ssid = content.get('ssid', '')
            password = content.get('password', '')
            security = content.get('security', 'WPA')
            return f'WIFI:T:{security};S:{ssid};P:{password};;'
        except:
            return content
    
    else:  # text
        return content


@qr_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    """Display QR generation form"""
    return render_template('generate_qr.html')


@qr_bp.route('/api/preview', methods=['POST'])
@login_required
def preview_qr():
    """
    API endpoint for QR code preview
    Returns QR code as base64 image
    """
    
    try:
        data = request.get_json()
        qr_type = data.get('qr_type', 'text').strip()
        content = data.get('content', '').strip()
        fg_color = data.get('fg_color', '#000000')
        bg_color = data.get('bg_color', '#FFFFFF')
        qr_size = int(data.get('qr_size', 10))
        
        # Validation
        if not content:
            return jsonify({'success': False, 'message': 'Content is required'}), 400
        
        if qr_type not in ['url', 'text', 'email', 'phone', 'wifi']:
            return jsonify({'success': False, 'message': 'Invalid QR type'}), 400
        
        # Validate content based on type
        if qr_type == 'email':
            if '@' not in content:
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        elif qr_type == 'phone':
            if len(''.join(filter(str.isdigit, content))) < 7:
                return jsonify({'success': False, 'message': 'Invalid phone number'}), 400
        
        # Generate QR code
        img = generate_qr_code(content, qr_type, fg_color, bg_color, qr_size=qr_size)
        
        # Convert to base64
        import base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@qr_bp.route('/api/create', methods=['POST'])
@login_required
def create_qr():
    """
    API endpoint for creating and saving QR code
    Saves QR code to database and file system
    """
    
    try:
        # Get form data
        qr_type = request.form.get('qr_type', 'text').strip()
        content = request.form.get('content', '').strip()
        fg_color = request.form.get('fg_color', '#000000')
        bg_color = request.form.get('bg_color', '#FFFFFF')
        qr_size = int(request.form.get('qr_size', 10))
        
        # Validation
        if not content:
            return jsonify({'success': False, 'message': 'Content is required'}), 400
        
        if qr_type not in ['url', 'text', 'email', 'phone', 'wifi']:
            return jsonify({'success': False, 'message': 'Invalid QR type'}), 400
        
        # Handle file upload for logo
        logo_path = None
        logo_used = False
        
        if 'logo' in request.files and request.files['logo'].filename:
            logo_file = request.files['logo']
            
            # Validate file
            if not allowed_file(logo_file.filename):
                return jsonify({'success': False, 'message': 'Invalid logo format'}), 400
            
            # Save logo
            logo_filename = get_safe_filename(logo_file.filename)
            logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename)
            logo_file.save(logo_path)
            logo_used = True
        
        # Generate QR code
        img = generate_qr_code(content, qr_type, fg_color, bg_color, logo_path, qr_size)
        
        # Save QR code to file system
        qr_filename = get_safe_filename(f'qr_{qr_type}')
        qr_filepath = os.path.join(current_app.config['GENERATED_QR_FOLDER'], qr_filename)
        img.save(qr_filepath)
        
        # Save to database
        qr_code = QRCode(
            user_id=current_user.id,
            qr_type=qr_type,
            content=content,
            file_name=qr_filename,
            logo_used=logo_used,
            fg_color=fg_color,
            bg_color=bg_color,
            qr_size=qr_size
        )
        
        db.session.add(qr_code)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'QR code generated successfully',
            'qr_id': qr_code.id,
            'qr_url': qr_code.get_file_url(),
            'download_url': f'/qr/download/{qr_code.id}'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@qr_bp.route('/download/<int:qr_id>')
@login_required
def download_qr(qr_id):
    """Download QR code file"""
    
    try:
        # Get QR code
        qr_code = QRCode.query.get(qr_id)
        
        if not qr_code:
            return jsonify({'success': False, 'message': 'QR code not found'}), 404
        
        # Verify ownership
        if qr_code.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get file path
        file_path = os.path.join(current_app.config['GENERATED_QR_FOLDER'], qr_code.file_name)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        # Send file
        return send_file(
            file_path,
            mimetype='image/png',
            as_attachment=True,
            download_name=qr_code.file_name
        )
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


def allowed_file(filename):
    """Check if file has allowed extension"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
