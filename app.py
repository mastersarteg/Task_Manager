from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from models import db
from routes.auth import auth_bp
from routes.tasks import tasks_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def index():
        return redirect(url_for('tasks.dashboard'))

    with app.app_context():
        db.create_all()

    @app.cli.command('seed')
    def seed():
        from models.user import User
        from models.task import Task
        if User.query.filter_by(email='demo@example.com').first():
            print('Seed data already exists')
            return

        demo_user = User(username='demouser', email='demo@example.com')
        demo_user.set_password('password123')
        db.session.add(demo_user)
        db.session.commit()

        sample_tasks = [
            Task(
                title='Read Flask tutorial',
                description='Follow a quick Flask tutorial and build a simple app.',
                due_date='2026-12-01',
                priority='Medium',
                status='Pending',
                owner=demo_user,
            ),
            Task(
                title='Write task manager features',
                description='Capture MVP requirements and implement CRUD flows.',
                due_date='2026-11-15',
                priority='High',
                status='Pending',
                owner=demo_user,
            ),
            Task(
                title='Review completed tasks',
                description='See how many tasks are resolved and update the dashboard.',
                due_date='2026-10-31',
                priority='Low',
                status='Completed',
                owner=demo_user,
            ),
        ]

        db.session.add_all(sample_tasks)
        db.session.commit()
        print('Seed data added successfully.')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
