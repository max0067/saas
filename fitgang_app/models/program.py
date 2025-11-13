"""Program models for structured sport/diet programs."""
from datetime import datetime
import json
from fitgang_app import db


class ProgramWeek(db.Model):
    """Program week model."""

    __tablename__ = 'program_weeks'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    goals = db.Column(db.Text)  # Objectifs de la semaine

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', backref=db.backref('weeks', lazy='dynamic', cascade='all, delete-orphan'))
    days = db.relationship('ProgramDay', back_populates='week', cascade='all, delete-orphan', order_by='ProgramDay.day_number')

    def __repr__(self):
        return f'<ProgramWeek {self.week_number} of Product {self.product_id}>'


class ProgramDay(db.Model):
    """Program day model."""

    __tablename__ = 'program_days'

    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('program_weeks.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)  # 1-7
    title = db.Column(db.String(200))

    # Workout details
    workout_type = db.Column(db.String(100))  # Cardio, Force, Repos, etc.
    workout_description = db.Column(db.Text)
    _workout_exercises = db.Column('workout_exercises', db.Text)  # Stored as JSON TEXT
    workout_duration = db.Column(db.Integer)  # en minutes
    workout_video_url = db.Column(db.String(500))
    workout_image_url = db.Column(db.String(500))

    # Diet details
    diet_description = db.Column(db.Text)
    diet_calories = db.Column(db.Integer)
    _diet_meals = db.Column('diet_meals', db.Text)  # Stored as JSON TEXT

    # Notes and tips
    notes = db.Column(db.Text)
    coach_tips = db.Column(db.Text)

    # Status
    is_rest_day = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    week = db.relationship('ProgramWeek', back_populates='days')

    @property
    def workout_exercises(self):
        """Get workout exercises as Python object."""
        if self._workout_exercises:
            try:
                return json.loads(self._workout_exercises)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @workout_exercises.setter
    def workout_exercises(self, value):
        """Set workout exercises from Python object."""
        if value is None:
            self._workout_exercises = None
        elif isinstance(value, str):
            # Already a string, store as is
            self._workout_exercises = value
        else:
            # Convert to JSON string
            self._workout_exercises = json.dumps(value) if value else None

    @property
    def diet_meals(self):
        """Get diet meals as Python object."""
        if self._diet_meals:
            try:
                return json.loads(self._diet_meals)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @diet_meals.setter
    def diet_meals(self, value):
        """Set diet meals from Python object."""
        if value is None:
            self._diet_meals = None
        elif isinstance(value, str):
            # Already a string, store as is
            self._diet_meals = value
        else:
            # Convert to JSON string
            self._diet_meals = json.dumps(value) if value else None

    def __repr__(self):
        return f'<ProgramDay {self.day_number} of Week {self.week_id}>'


class UserProgramProgress(db.Model):
    """Track user progress through programs."""

    __tablename__ = 'user_program_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    current_week = db.Column(db.Integer, default=1)
    current_day = db.Column(db.Integer, default=1)
    _completed_days = db.Column('completed_days', db.Text)  # Stored as JSON TEXT

    # Stats
    total_workouts_completed = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('program_progress', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('user_progress', lazy='dynamic'))

    @property
    def completed_days(self):
        """Get completed days as Python object."""
        if self._completed_days:
            try:
                return json.loads(self._completed_days)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @completed_days.setter
    def completed_days(self, value):
        """Set completed days from Python object."""
        if value is None:
            self._completed_days = None
        elif isinstance(value, str):
            self._completed_days = value
        else:
            self._completed_days = json.dumps(value) if value else None

    def mark_day_complete(self, week, day):
        """Mark a specific day as completed."""
        completed = self.completed_days if self.completed_days else []

        # Check if already completed
        for item in completed:
            if item['week'] == week and item['day'] == day:
                return False

        completed.append({
            'week': week,
            'day': day,
            'completed_at': datetime.utcnow().isoformat()
        })
        self.completed_days = completed
        self.total_workouts_completed += 1
        self.last_activity = datetime.utcnow()
        return True

    def is_day_completed(self, week, day):
        """Check if a specific day is completed."""
        completed = self.completed_days if self.completed_days else []

        for item in completed:
            if item['week'] == week and item['day'] == day:
                return True
        return False

    def get_completion_percentage(self):
        """Calculate program completion percentage."""
        if not self.product or not self.product.duration_weeks:
            return 0

        total_days = self.product.duration_weeks * 7
        completed = len(self.completed_days) if self.completed_days else 0
        return int((completed / total_days) * 100) if total_days > 0 else 0

    def __repr__(self):
        return f'<UserProgramProgress User:{self.user_id} Product:{self.product_id}>'
