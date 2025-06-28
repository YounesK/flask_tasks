from flask import Flask, render_template, request, redirect, url_for
from models import db, Category, Task
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    db.create_all()

@app.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()

    # Extraire toutes les tâches terminées sous forme de liste de tuples (category, task)
    completed_tasks = []
    for category in categories:
        for task in category.tasks:
            if task.done:
                completed_tasks.append((category.name, task.label))

    # Choisir la tâche Pomodoro en cours (première tâche non terminée)
    current_task = None
    for category in categories:
        for task in category.tasks:
            if not task.done:
                current_task = task
                break
        if current_task:
            break

    return render_template('index.html', current_task=current_task, completed_tasks=completed_tasks)


@app.route('/add', methods=['POST'])
def add():
    category_name = request.form.get('category').strip()
    task_label = request.form.get('task').strip()

    if not category_name or not task_label:
        return redirect(url_for('index'))

    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()

    task = Task(label=task_label, done=False, category=category)
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return ('', 204)  # Réponse vide pour fetch JS

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))