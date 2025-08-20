from flask import Flask, render_template, request, redirect, url_for
import random
import os,json,random

app = Flask(__name__)

DATA_FILE=os.path.join(app.root_path,"todos.json")
def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

todos = load_todos()   # initialize list
def gen_id():
    existing = {t["id"] for t in todos}
    cur = random.randint(1, 1_000_000)
    while cur in existing:
        cur = random.randint(1, 1_000_000)
    return cur

todos = []

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        todo_priority = request.form.get("todo_priority")
        due_date = request.form.get("due_date")

        if todo_name:  
            cur_id = random.randint(1, 10000)
            todos.append({
                "id": cur_id,
                "name": todo_name,
                "checked": False,
                "priority": todo_priority if todo_priority else "Normal",
                "due_date": due_date if due_date else "No date"
            })
            save_todos(todos)
        return redirect(url_for("home"))

    total = len(todos)
    done = sum(1 for t in todos if t["checked"])

    return render_template(
        "index.html",
        items=todos,
        total=total,
        done=done
    )

@app.route("/check/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["checked"] = not todo["checked"]
            break
        save_todos(todos)
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
