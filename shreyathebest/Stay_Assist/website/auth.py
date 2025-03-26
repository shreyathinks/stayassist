from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash,send_from_directory, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from . import db, login_manager  # Import from package level
from .models import User, ServiceRequest
from werkzeug.utils import secure_filename
import os


auth = Blueprint('auth', __name__)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# User loader must be defined at module level
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        hostel = request.form.get('hostel')
        block = request.form.get('block')
        room_number = request.form.get('room_number')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                hostel=hostel,
                block=block,
                room_number=room_number
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.features'))

    return render_template('sign_up.html')

@auth.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('auth.features'))

        flash('Invalid email or password.', category='error')

    return render_template('sign_in.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_in'))

@auth.route('/features')
@login_required
def features():
    return render_template('features.html')

@auth.route('/book-service', methods=['POST'])
@login_required
def submit_service_request():
    try:
        # Handle both JSON and form data for backward compatibility
        if request.is_json:
            data = request.get_json()
            image_file = None
        else:
            data = request.form
            image_file = request.files.get('image')

        if not data or 'service' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        # Log the received form data and files for debugging
        print(f"Received form data: {dict(data)}")
        print(f"Received files: {request.files}")
        print(f"Image file: {image_file}")

        # Handle image upload if present using the logic from views.py
        image_path = None
        if image_file:
            if not allowed_file(image_file.filename):
                print(f"Invalid file type: {image_file.filename}")
                return jsonify({
                    "error": "Invalid file type. Allowed: png, jpg, jpeg, gif",
                    "success": False
                }), 400

            try:
                # Define the upload directory (same as in views.py)
                uploads_dir = os.path.join(os.getcwd(), 'uploads')
                # Ensure the upload directory exists
                os.makedirs(uploads_dir, exist_ok=True)
                print(f"Upload directory: {uploads_dir}")

                # Generate a unique filename with timestamp
                filename = secure_filename(image_file.filename)
                unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
                full_image_path = os.path.join(uploads_dir, unique_filename)

                # Save the image file
                print(f"Saving file to: {full_image_path}")
                image_file.save(full_image_path)

                # Verify the file was saved
                if not os.path.exists(full_image_path):
                    raise FileNotFoundError("File was not saved to the expected location")

                # Check file size to ensure it's not empty
                file_size = os.path.getsize(full_image_path)
                print(f"Saved file size: {file_size} bytes")
                if file_size == 0:
                    os.remove(full_image_path)
                    raise ValueError("Saved file is empty")

                print(f"Image successfully saved to: {full_image_path}")

                # Store relative path for web access (relative to static/)
                image_path = os.path.join('uploads', unique_filename)

            except Exception as e:
                print(f"Image upload error: {str(e)}")
                return jsonify({
                    "error": f"Image upload failed: {str(e)}",
                    "success": False
                }), 500

        # Create new service request
        try:
            new_request = ServiceRequest(
                user_id=current_user.id,
                service_type=data['service'],
                issue_description=data.get('issue', ''),
                date=datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M'),
                status='pending'
            )

            # Prepare service-specific data
            service_data = {}
            if data['service'] == 'cleaning':
                service_data = {'frequency': data.get('frequency', 'once')}
            elif data['service'] == 'pest':
                service_data = {'pest_type': data.get('pest_type', 'unknown')}
            elif data['service'] == 'ac':
                service_data = {'service_type': data.get('service_type', 'general')}
            elif data['service'] == 'furniture':
                service_data = {'furniture_type': data.get('furniture_type', 'other')}

            # Add image path to service_data if an image was uploaded
            if image_path:
                service_data['image_path'] = image_path

            new_request.set_service_data(service_data)
            
            db.session.add(new_request)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Request submitted successfully!",
                "request_id": new_request.id,
                "redirect_url": url_for('auth.booking_confirmation', request_id=new_request.id),
                "image_url": url_for('auth.uploaded_file', filename=os.path.basename(image_path)) if image_path else None

            })

        except ValueError as e:
            return jsonify({"error": "Invalid date format", "success": False}), 400
        except Exception as db_error:
            db.session.rollback()
            return jsonify({
                "error": f"Database error: {str(db_error)}",
                "success": False
            }), 500

    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }), 500

@auth.route('/booking-confirmation/<int:request_id>')
@login_required
def booking_confirmation(request_id):
    # Verify the request belongs to the current user
    service_request = ServiceRequest.query.filter_by(
        id=request_id,
        user_id=current_user.id
    ).first_or_404()

    # Prepare data for template
    confirmation_data = {
        'service_type': service_request.service_type,
        'request_id': service_request.id,
        'issue': service_request.issue_description,
        'scheduled_date': service_request.date.strftime('%A, %B %d at %I:%M %p'),
        'status': service_request.status,
        'user': current_user
    }

    # Add service-specific data
    service_data = service_request.get_service_data()
    if service_request.service_type == 'cleaning':
        confirmation_data['frequency'] = service_data.get('frequency')
    elif service_request.service_type == 'pest':
        confirmation_data['pest_type'] = service_data.get('pest_type')
    elif service_request.service_type == 'ac':
        confirmation_data['service_type'] = service_data.get('service_type')
    elif service_request.service_type == 'furniture':
        confirmation_data['furniture_type'] = service_data.get('furniture_type')
    
    # Add image path if it exists
    if 'image_path' in service_data:
        confirmation_data['image_url'] = url_for('auth.uploaded_file', filename=os.path.basename(service_data['image_path']))


    return render_template('book_service.html', **confirmation_data)

@auth.route('/service-requests', methods=['GET'])
@login_required
def get_service_requests():
    service_type = request.args.get('service')
    
    query = ServiceRequest.query.filter_by(user_id=current_user.id)
    
    if service_type:
        query = query.filter_by(service_type=service_type)
    
    requests = query.order_by(ServiceRequest.date.desc()).all()
    
    requests_data = []
    for req in requests:
        request_data = {
            "id": req.id,
            "service_type": req.service_type,
            "issue": req.issue_description,
            "date": req.date.isoformat(),
            "status": req.status,
            "created_at": req.created_at.isoformat() if req.created_at else None
        }
        
        # Add service-specific fields
        service_data = req.get_service_data()
        if req.service_type == 'cleaning':
            request_data['frequency'] = service_data.get('frequency')
        elif req.service_type == 'pest':
            request_data['pest_type'] = service_data.get('pest_type')
        elif req.service_type == 'ac':
            request_data['service_type'] = service_data.get('service_type')
        elif req.service_type == 'furniture':
            request_data['furniture_type'] = service_data.get('furniture_type')
        
        # Add image path if it exists
        if 'image_path' in service_data:
            request_data['image_url'] = url_for('auth.uploaded_file', filename=os.path.basename(service_data['image_path']))

        
        requests_data.append(request_data)
    
    return jsonify(requests_data)

@auth.route('/user-dashboard')
@login_required
def user_dashboard():
    # Get all service requests for the user, newest first
    all_requests = ServiceRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(ServiceRequest.date.desc()).all()
    
    # Organize by status
    pending_requests = [r for r in all_requests if r.status == 'pending']
    confirmed_requests = [r for r in all_requests if r.status == 'confirmed']
    completed_requests = [r for r in all_requests if r.status == 'completed']
    
    # Prepare data for template with image support
    for request_list in [pending_requests, confirmed_requests, completed_requests]:
        for request in request_list:
            service_data = request.get_service_data()
            if 'image_path' in service_data:
                setattr(request, 'image_url', url_for('auth.uploaded_file', filename=os.path.basename(service_data['image_path'])))

    return render_template('user_dashboard.html',
                         user=current_user,
                         pending_requests=pending_requests,
                         confirmed_requests=confirmed_requests,
                         completed_requests=completed_requests)

@auth.route('/delete-request/<int:request_id>', methods=['POST'])
@login_required
def delete_request(request_id):
    try:
        # Fetch the request and verify it belongs to the current user
        request_to_delete = ServiceRequest.query.filter_by(
            id=request_id,
            user_id=current_user.id
        ).first()
        
        if not request_to_delete:
            flash('Request not found or you do not have permission to delete it.', 'error')
            return redirect(url_for('auth.user_dashboard'))
            
        db.session.delete(request_to_delete)
        db.session.commit()
        flash('Request deleted successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the request.', 'error')
        current_app.logger.error(f"Error deleting request {request_id}: {str(e)}")
        
    return redirect(url_for('auth.user_dashboard'))
@auth.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)