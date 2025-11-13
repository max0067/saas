"""Workout models."""
from datetime import datetime
from fitgang_app import db


class Workout(db.Model):
    """Workout model (workout plan)."""

    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Workout details
    week_number = db.Column(db.Integer)  # Which week of the program
    day_number = db.Column(db.Integer)  # Which day of the week
    duration_minutes = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))

    # Instructions
    warmup = db.Column(db.Text)
    cooldown = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', back_populates='workouts')
    exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    sessions = db.relationship('WorkoutSession', back_populates='workout', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Workout {self.name}>'


class Exercise(db.Model):
    """Exercise model (exercise library)."""

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    # Basic information
    name = db.Column(db.String(200), nullable=False, unique=True)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)

    # Exercise details
    muscle_group = db.Column(db.String(100))
    equipment = db.Column(db.String(200))
    difficulty = db.Column(db.String(20))

    # Media
    video_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    instructions = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Exercise {self.name}>'


class WorkoutExercise(db.Model):
    """Association table between workouts and exercises with details."""

    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # Exercise parameters
    order = db.Column(db.Integer, default=0)  # Order in the workout
    sets = db.Column(db.Integer)
    reps = db.Column(db.String(50))  # Can be "12" or "8-12" or "AMRAP"
    rest_seconds = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Relationships
    workout = db.relationship('Workout', back_populates='exercises')
    exercise = db.relationship('Exercise')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'


class WorkoutSession(db.Model):
    """User workout session (completed workout tracking)."""

    __tablename__ = 'workout_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))

    # Session details
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Performance data (JSON array of exercises with actual performance)
    performance_data = db.Column(db.JSON)
    # Example: [{"exercise_id": 1, "sets": [{"reps": 12, "weight": 50}, {"reps": 10, "weight": 50}]}]

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='workout_sessions')
    workout = db.relationship('Workout', back_populates='sessions')

    def __repr__(self):
        return f'<WorkoutSession {self.id} - User {self.user_id}>'
