def safeexec(code: str, out: str = "commons", whitelist: list[str] = None):
    #  assert "import" not in code, "MAMMOth-commons prevented the execution of an externally-defined code snippet that internally performs an import statement"
    if code.endswith(".py"):
        with open(code, "r") as file:
            code = file.read()

    exec_context = locals().copy()
    exec(code, exec_context)
    return exec_context[out]
