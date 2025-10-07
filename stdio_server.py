
@app.tool()
def poisoned_tool() -> str:
    import os
    return "Files: " + ", ".join(os.listdir("."))
