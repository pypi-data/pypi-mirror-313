from flask import render_template, redirect, url_for
from demonstrator.backend.loaders import (
    analysis_methods,
    parameters_to_class,
)
import traceback
from datetime import datetime


def handle_fairness_analysis_get(
    database, task_id, error_title=None, error_message=None
):
    task = database.get(task_id)
    if not task:
        return redirect(url_for("index"))

    compatible_methods = {
        method: {
            "parameters": entries["parameters"][3:],
            "description": entries["description"],
            "parameter_options": entries["parameter_options"],
        }
        for method, entries in analysis_methods.items()
        if issubclass(
            parameters_to_class[task["dataset_loader"]]["return"],
            parameters_to_class[method][entries["parameters"][0][0]],
        )
        and issubclass(
            parameters_to_class[task["model_loader"]]["return"],
            parameters_to_class[method][entries["parameters"][1][0]],
        )
    }

    # Extract existing information from the task (if available)
    preselected_method = task.get("analysis_method", None)
    prefilled_parameters = task.get("analysis_parameters", {})
    prefilled_sensitive_attributes = task.get("sensitive_attributes", [])

    return render_template(
        "fairness_analysis.html",
        analysis_methods=compatible_methods,
        task=task,
        preselected_method=preselected_method,
        prefilled_parameters=prefilled_parameters,
        prefilled_sensitive_attributes=prefilled_sensitive_attributes,
        sensitive_attributes=task["dataset_loaded"].cols,
        default_task_name=task.get("name", "Task " + task["id"]),
        error_title=error_title,
        error_message=error_message,
    )


def handle_fairness_analysis_post(request, database, task_id):
    from demonstrator.backend.loaders import name_to_runnable, analysis_methods

    task = database.get(task_id)
    if not task:
        return redirect(url_for("index"))

    selected_method = request.form["analysis_method"]

    # Get parameter types
    method_info = analysis_methods[selected_method]
    parameters = method_info["parameters"]

    # Create a dict mapping parameter names to types
    param_types = {param[0]: param[1] for param in parameters}

    analysis_parameters = {}
    for key in request.form:
        if key in ("analysis_method", "sensitive_attributes", "task_name"):
            continue
        value = request.form[key]
        param_type = param_types.get(key, "str")  # Default to 'str' if type not found
        if param_type == "bool":
            value = value == "true"
        elif param_type == "int":
            value = int(value)
        elif param_type == "float":
            value = float(value)
        # else keep as string
        analysis_parameters[key] = value

    task["analysis_method"] = selected_method
    task["analysis_parameters"] = analysis_parameters
    task["sensitive_attributes"] = request.form.getlist("sensitive_attributes")
    task["status"] = "running"
    task["name"] = request.form["task_name"]
    task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        result = name_to_runnable[selected_method](
            task["dataset_loaded"],
            task["model_loaded"],
            task["sensitive_attributes"],
            **task["analysis_parameters"]
        )
        task["result"] = result.text()
        task["status"] = "completed"
        task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    except (Exception, RuntimeError) as e:
        task["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        task["status"] = "failed"
        traceback.print_exception(e)
        return handle_fairness_analysis_get(
            database=database,
            task_id=task_id,
            error_title="Error during fairness analysis",
            error_message=str(e),
        )

    return redirect(url_for("task_results", task_id=task_id))
