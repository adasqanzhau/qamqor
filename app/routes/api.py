from flask import Blueprint, jsonify, request
from flask_login import login_required

from app import db
from app.models import User, Clinic

api_bp = Blueprint('api', __name__)


@api_bp.route('/doctors/<int:clinic_id>', methods=['GET'])
@login_required
def get_doctors(clinic_id):
    clinic = Clinic.query.get_or_404(clinic_id)
    doctors = User.query.filter_by(
        clinic_id=clinic.id,
        role='doctor',
        is_active=True
    ).all()

    result = []
    for doctor in doctors:
        result.append({
            'id': doctor.id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization,
            'experience_years': doctor.experience_years,
            'consultation_price': doctor.consultation_price,
            'avatar': doctor.avatar,
        })

    return jsonify(result), 200

@api_bp.route('/search/doctors', methods=['GET'])
@login_required
def search_doctors():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([]), 200

    search = f'%{query}%'
    doctors = User.query.filter(
        User.role == 'doctor',
        User.is_active == True,
        db.or_(
            User.first_name.ilike(search),
            User.last_name.ilike(search),
            User.specialization.ilike(search),
        )
    ).limit(20).all()

    result = []
    for doctor in doctors:
        result.append({
            'id': doctor.id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization,
            'clinic_id': doctor.clinic_id,
            'clinic_name': doctor.clinic.name if doctor.clinic else None,
            'avatar': doctor.avatar,
            'consultation_price': doctor.consultation_price,
        })

    return jsonify(result), 200
