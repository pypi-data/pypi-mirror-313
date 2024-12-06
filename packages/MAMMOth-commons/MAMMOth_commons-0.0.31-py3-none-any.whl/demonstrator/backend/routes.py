from flask import request
from demonstrator.backend.utils import *
from demonstrator.backend.handlers.handle_fairness_analysis import *
from demonstrator.backend.handlers.handle_select_model import *
from demonstrator.backend.handlers.handle_new_task import *
from demonstrator.backend.handlers.handle_create_variation import *


def initialize_routes(app, database):
    @app.route("/")
    def index():
        return render_template("index.html", tasks=database.tasks.values())

    @app.route("/new_task", methods=["GET", "POST"])
    def new_task():
        if request.method == "POST":
            return handle_new_task_post(request, database)
        return handle_new_task_get(database)

    @app.route("/select_model/<int:task_id>", methods=["GET", "POST"])
    def select_model(task_id):
        if request.method == "POST":
            return handle_select_model_post(request, database, task_id)
        return handle_select_model_get(database, task_id)

    @app.route("/fairness_analysis/<int:task_id>", methods=["GET", "POST"])
    def fairness_analysis(task_id):
        if request.method == "POST":
            return handle_fairness_analysis_post(request, database, task_id)
        return handle_fairness_analysis_get(database, task_id)

    @app.route("/task_results/<int:task_id>")
    def task_results(task_id):
        return handle_task_results(database, task_id)

    @app.route("/create_variation/<int:task_id>", methods=["GET", "POST"])
    def create_variation(task_id):
        if request.method == "POST":
            return handle_create_variation_post(request, database, task_id)
        return handle_create_variation_get(database, task_id)

    @app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
    def edit_task(task_id):
        task = database.get(task_id)
        if not task:
            return redirect(url_for("index"))
        task["status"] = "created"
        return redirect(url_for("create_variation", task_id=task_id))

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    @app.route("/delete_task/<int:task_id>", methods=["POST"])
    def delete_task(task_id):
        return handle_deletion(database, task_id)
