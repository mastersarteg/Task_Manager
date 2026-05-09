from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from models import db
from models.task import Task


tasks_bp = Blueprint('tasks', __name__, template_folder='../templates')


@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', 'all')

    tasks_query = Task.query.filter_by(user_id=current_user.id)

    if search:
        tasks_query = tasks_query.filter(Task.title.ilike(f'%{search}%'))

    if status_filter == 'pending':
        tasks_query = tasks_query.filter_by(status='Pending')
    elif status_filter == 'completed':
        tasks_query = tasks_query.filter_by(status='Completed')

    tasks = tasks_query.order_by(Task.due_date.asc(), Task.priority.desc()).all()
    pending_tasks = [task for task in tasks if task.status == 'Pending']
    completed_tasks = [task for task in tasks if task.status == 'Completed']

    stats = {
        'total': len(tasks),
        'pending': len(pending_tasks),
        'completed': len(completed_tasks),
    }

    return render_template(
        'dashboard.html',
        tasks=tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        stats=stats,
        search=search,
        status_filter=status_filter,
    )


@tasks_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        priority = request.form.get('priority', 'Medium')

        if not title:
            flash('A task title is required.', 'warning')
            return redirect(url_for('tasks.new_task'))

        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status='Pending',
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully.', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('task_form.html', form_action=url_for('tasks.new_task'), task=None)


@tasks_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        task.title = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        task.due_date = request.form.get('due_date', '').strip()
        task.priority = request.form.get('priority', 'Medium')
        task.status = request.form.get('status', 'Pending')

        if not task.title:
            flash('A task title is required.', 'warning')
            return redirect(url_for('tasks.edit_task', task_id=task_id))

        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('task_form.html', form_action=url_for('tasks.edit_task', task_id=task_id), task=task)


@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'info')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.status = 'Completed' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    flash('Task status updated.', 'success')
    return redirect(url_for('tasks.dashboard'))
