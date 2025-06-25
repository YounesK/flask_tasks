

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Liste des tâches : chaque tâche est un dictionnaire
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    label = request.form.get('task')
    if label:
        tasks.append({'label': label, 'done': False})
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
