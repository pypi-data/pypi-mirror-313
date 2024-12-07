from flask import render_template, redirect, url_for
from demonstrator.backend.loaders import name_to_runnable, dataset_loaders
import traceback
from datetime import datetime


def handle_create_variation_get(
    database, task_id, error_title=None, error_message=None
):
    base_task = database.get(task_id)
    if not base_task:
        return redirect(url_for("index"))

    base_task = {
        key: value
        for key, value in base_task.items()
        if key not in ["dataset_loaded", "model_loaded", "result"]
    }
    base_task["status"] = "created"

    return render_template(
        "new_task.html",
        dataset_loaders=dataset_loaders,
        base_task=base_task,
        default_task_name=base_task.get("name", "Task " + base_task["id"]),
        error_title=error_title,
        error_message=error_message,
    )


def handle_create_variation_post(request, database, task_id):
    base_task = database.get(task_id)
    if not base_task:
        return redirect(url_for("index"))

    dataset_loader_name = request.form["dataset_loader"]
    dataset_parameters = {
        key: request.form[key]
        for key in request.form
        if key != "dataset_loader" and key != "task_name"
    }
    call_parameters = {
        key: (
            value
            if not isinstance(value, str) or "," not in value or len(value.strip()) == 1
            else [val.strip() for val in value.split(",")]
        )
        for key, value in dataset_parameters.items()
    }

    new_task = {
        "dataset_loader": dataset_loader_name,
        "dataset_parameters": dataset_parameters,
        "model_loader": base_task.get("model_loader"),
        "model_parameters": base_task.get("model_parameters"),
        "analysis_method": base_task.get("analysis_method"),
        "analysis_parameters": base_task.get("analysis_parameters"),
        "sensitive_attributes": base_task.get("sensitive_attributes", list()),
        "name": request.form["task_name"],
        "status": "created",
        "modified": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    if base_task["status"] == "completed":
        new_task_id = database.register(new_task)
    else:
        new_task_id = database.replace(new_task, task_id)

    try:
        new_task["dataset_loaded"] = name_to_runnable[dataset_loader_name](
            **call_parameters
        )
        new_task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not hasattr(new_task["dataset_loaded"], "cols"):
            raise Exception(
                "Invalid dataset loader: the selected dataset loader failed to create an initial estimation of sensitive attribute candidates (it must initialize a data type with a `cols` attribute)."
            )
    except (Exception, RuntimeError) as e:
        new_task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_task["status"] = "failed"
        traceback.print_exception(e)
        return handle_create_variation_get(
            database=database,
            task_id=new_task_id,
            error_title="Error loading dataset",
            error_message=str(e),
        )
    return redirect(url_for("select_model", task_id=new_task_id))
