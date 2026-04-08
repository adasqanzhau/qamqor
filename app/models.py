from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


def _utcnow():
    """Timezone-aware UTC now (replaces deprecated datetime.utcnow)."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='patient')  # superadmin, clinic_admin, doctor, patient
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # Relationships
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=True)
    clinic = db.relationship('Clinic', back_populates='users', foreign_keys=[clinic_id])

    # Doctor-specific
    specialization = db.Column(db.String(128))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    consultation_price = db.Column(db.Float)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<User {self.email}>'


class Clinic(db.Model):
    __tablename__ = 'clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(300))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    logo = db.Column(db.String(256))
    primary_color = db.Column(db.String(7), default='#0d6efd')
    secondary_color = db.Column(db.String(7), default='#6c757d')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # Working hours
    working_hours_start = db.Column(db.String(5), default='09:00')
    working_hours_end = db.Column(db.String(5), default='18:00')
    working_days = db.Column(db.String(50), default='1,2,3,4,5')  # 1=Mon, 7=Sun

    users = db.relationship('User', back_populates='clinic', foreign_keys=[User.clinic_id],
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Clinic {self.name}>'



