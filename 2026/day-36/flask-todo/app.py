from flask import Flask, jsonify, request, render_template_string
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER', 'flaskuser'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'flaskdb')
    )


HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dockerized Flask Todo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            display: flex;
            flex-direction: column;
        }
        .header {
            padding: 24px 40px;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .header h1 { font-size: 22px; color: white; }
        .header p { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 4px; }
        .container { max-width: 580px; margin: 40px auto; padding: 0 20px; width: 100%; }
        .glass {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }
        .glass h2 { font-size: 14px; color: rgba(255,255,255,0.6); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 1px; }
        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            color: white;
            font-size: 14px;
            margin-bottom: 12px;
            outline: none;
        }
        input[type="text"]::placeholder { color: rgba(255,255,255,0.3); }
        input[type="text"]:focus { border-color: rgba(255,255,255,0.4); }
        button {
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        button:hover { background: rgba(255,255,255,0.25); }
        .todo-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .todo-item:last-child { border-bottom: none; }
        .todo-task { font-size: 14px; color: white; }
        .delete-btn {
            background: rgba(231,76,60,0.2);
            border-color: rgba(231,76,60,0.3);
            padding: 6px 12px;
            font-size: 12px;
        }
        .delete-btn:hover { background: rgba(231,76,60,0.4); }
        .badge {
            background: rgba(255,255,255,0.15);
            color: white;
            font-size: 11px;
            padding: 2px 10px;
            border-radius: 20px;
            margin-left: 8px;
        }
        .empty { color: rgba(255,255,255,0.3); font-size: 14px; text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>&#x1F433; Dockerized Flask Todo</h1>
        <p>by Uttam Tripathi &nbsp;&bull;&nbsp; Flask + MySQL + Docker Compose</p>
    </div>
    <div class="container">
        <div class="glass">
            <h2>New Todo</h2>
            <form method="POST" action="/todos">
                <input type="text" name="task" placeholder="What needs to be done?" required>
                <button type="submit">+ Add Todo</button>
            </form>
        </div>
        <div class="glass">
            <h2>My Todos <span class="badge">{{ todos|length }}</span></h2>
            {% if todos %}
                {% for todo in todos %}
                <div class="todo-item">
                    <span class="todo-task">{{ todo[1] }}</span>
                    <form method="POST" action="/todos/{{ todo[0] }}/delete">
                        <button class="delete-btn">Delete</button>
                    </form>
                </div>
                {% endfor %}
            {% else %}
                <p class="empty">No todos yet — add one above!</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''
@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    return render_template_string(HTML, todos=todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    conn.commit()
    return home()

@app.route('/todos/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
