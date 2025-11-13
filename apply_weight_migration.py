"""Apply weight entries migration."""
from fitgang_app import create_app, db

app = create_app()

with app.app_context():
    # Create weight_entries table using SQLAlchemy
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS weight_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            notes TEXT,
            recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    db.engine.execute("""
        CREATE INDEX IF NOT EXISTS idx_weight_entries_user_id ON weight_entries(user_id)
    """)

    db.engine.execute("""
        CREATE INDEX IF NOT EXISTS idx_weight_entries_recorded_at ON weight_entries(recorded_at)
    """)

    print("✓ weight_entries table created successfully")
