"""
History blueprint for viewing, searching, and managing QR code records
Provides pagination and filtering capabilities
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from models import db, QRCode
from sqlalchemy import desc
import os

# Create history blueprint
history_bp = Blueprint('history', __name__, url_prefix='/history')


@history_bp.route('/')
@login_required
def index():
    """Display QR code history with pagination"""
    
    # Get page number
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get search query
    search_query = request.args.get('search', '').strip()
    
    # Base query
    query = current_user.qr_codes.order_by(desc(QRCode.created_at))
    
    # Apply search filter
    if search_query:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                QRCode.qr_type.ilike(f'%{search_query}%'),
                QRCode.content.ilike(f'%{search_query}%'),
                QRCode.file_name.ilike(f'%{search_query}%')
            )
        )
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    qr_codes = pagination.items
    
    return render_template(
        'history.html',
        qr_codes=qr_codes,
        pagination=pagination,
        search_query=search_query
    )


@history_bp.route('/api/search', methods=['POST'])
@login_required
def search():
    """
    API endpoint for searching QR codes
    Returns paginated results as JSON
    """
    
    try:
        data = request.get_json()
        search_query = data.get('query', '').strip()
        page = data.get('page', 1, type=int)
        per_page = 10
        
        # Base query
        query = current_user.qr_codes.order_by(desc(QRCode.created_at))
        
        # Apply search filter
        if search_query:
            from sqlalchemy import or_
            query = query.filter(
                or_(
                    QRCode.qr_type.ilike(f'%{search_query}%'),
                    QRCode.content.ilike(f'%{search_query}%'),
                    QRCode.file_name.ilike(f'%{search_query}%')
                )
            )
        
        # Paginate results
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Format results
        qr_list = []
        for qr in pagination.items:
            qr_list.append({
                'id': qr.id,
                'type': qr.qr_type,
                'content': qr.content[:50] + '...' if len(qr.content) > 50 else qr.content,
                'file_name': qr.file_name,
                'created_at': qr.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_url': qr.get_file_url(),
                'download_url': f'/qr/download/{qr.id}'
            })
        
        return jsonify({
            'success': True,
            'qr_codes': qr_list,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@history_bp.route('/api/delete/<int:qr_id>', methods=['DELETE'])
@login_required
def delete_qr(qr_id):
    """
    API endpoint for deleting QR code record
    Removes file and database entry
    """
    
    try:
        # Get QR code
        qr_code = QRCode.query.get(qr_id)
        
        if not qr_code:
            return jsonify({'success': False, 'message': 'QR code not found'}), 404
        
        # Verify ownership
        if qr_code.user_id != current_user.id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Delete file if exists
        file_path = os.path.join(current_app.config['GENERATED_QR_FOLDER'], qr_code.file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f'Error deleting file: {str(e)}')
        
        # Delete logo if exists
        if qr_code.logo_used:
            # Logo info is not stored, so we skip deletion
            pass
        
        # Delete from database
        db.session.delete(qr_code)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'QR code deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@history_bp.route('/api/bulk-delete', methods=['POST'])
@login_required
def bulk_delete():
    """
    API endpoint for bulk deleting QR codes
    """
    
    try:
        data = request.get_json()
        qr_ids = data.get('qr_ids', [])
        
        if not qr_ids:
            return jsonify({'success': False, 'message': 'No QR codes selected'}), 400
        
        # Verify all QR codes belong to user
        qr_codes = QRCode.query.filter(
            QRCode.id.in_(qr_ids),
            QRCode.user_id == current_user.id
        ).all()
        
        if len(qr_codes) != len(qr_ids):
            return jsonify({'success': False, 'message': 'Some QR codes not found or unauthorized'}), 403
        
        # Delete files
        for qr_code in qr_codes:
            file_path = os.path.join(current_app.config['GENERATED_QR_FOLDER'], qr_code.file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f'Error deleting file: {str(e)}')
            
            # Delete from database
            db.session.delete(qr_code)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(qr_codes)} QR codes deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@history_bp.route('/api/export', methods=['GET'])
@login_required
def export_data():
    """
    API endpoint for exporting QR code history as CSV
    """
    
    try:
        import csv
        import io
        from datetime import datetime
        
        # Get all QR codes
        qr_codes = current_user.qr_codes.order_by(desc(QRCode.created_at)).all()
        
        # Create CSV
        si = io.StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['ID', 'Type', 'Content', 'File Name', 'Logo Used', 'Foreground Color', 'Background Color', 'Created At'])
        
        # Write data
        for qr in qr_codes:
            writer.writerow([
                qr.id,
                qr.qr_type,
                qr.content[:100],
                qr.file_name,
                'Yes' if qr.logo_used else 'No',
                qr.fg_color,
                qr.bg_color,
                qr.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Return CSV
        output = si.getvalue()
        return {
            'success': True,
            'csv_data': output,
            'filename': f'qr_history_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
