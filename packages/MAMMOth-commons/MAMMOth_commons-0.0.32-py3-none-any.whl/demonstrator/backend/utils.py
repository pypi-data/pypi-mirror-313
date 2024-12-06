from flask import render_template, redirect, url_for


def handle_error(error):
    error_message = getattr(error, "description", "An unexpected error occurred.")
    return (
        render_template(
            "500.html",
            title="Error at unknown point",
            message=error_message,
            task_id="---",
        ),
        500,
    )


def handle_task_results(database, task_id):
    task = database.get(task_id)
    if not task:
        return redirect(url_for("index"))
    return render_template("task_results.html", task=task)


def handle_deletion(database, task_id):
    task = database.get(task_id)
    if task:
        database.remove(task)
    return redirect(url_for("index"))
