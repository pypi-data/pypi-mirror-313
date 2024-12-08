from flask import render_template, redirect, url_for
from demonstrator.backend.loaders import name_to_runnable, model_loaders
import traceback
from datetime import datetime


def handle_select_model_get(database, task_id, error_title=None, error_message=None):
    task = database.get(task_id)
    if not task:
        return redirect(url_for("index"))

    loaders = {
        loader: loader_data
        for loader, loader_data in model_loaders.items()
        if task["dataset_loader"] in loader_data["compatible"]
    }

    selected_model_loader = task.get("model_loader")
    selected_parameters = task.get("model_parameters", {})

    return render_template(
        "model.html",
        model_loaders=loaders,
        task_id=task_id,
        selected_model_loader=selected_model_loader,
        selected_parameters=selected_parameters,
        default_task_name=task.get("name", "Task " + task["id"]),
        error_title=error_title,
        error_message=error_message,
    )


def handle_select_model_post(request, database, task_id):
    task = database.get(task_id)
    if not task:
        return redirect(url_for("index"))

    model_loader_name = request.form["model_loader"]
    model_parameters = {
        key: request.form[key]
        for key in request.form
        if key != "model_loader" and key != "task_name"
    }
    task["model_loader"] = model_loader_name
    task["model_parameters"] = model_parameters
    task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    task["name"] = request.form["task_name"]

    try:
        task["model_loaded"] = name_to_runnable[model_loader_name](**model_parameters)
        task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    except (Exception, RuntimeError) as e:
        task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        task["status"] = "failed"
        traceback.print_exception(e)
        return handle_select_model_get(
            database=database,
            task_id=task_id,
            error_title="Error loading model",
            error_message=str(e),
        )
    return redirect(url_for("fairness_analysis", task_id=task_id))
