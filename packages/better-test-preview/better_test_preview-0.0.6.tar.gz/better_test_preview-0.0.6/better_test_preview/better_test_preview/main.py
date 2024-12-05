from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import glob
import subprocess
from pydantic import BaseModel
from typing import List
from ansi2html import Ansi2HTMLConverter

TEMPLATE_PATH = "templates"

class TestOptions(BaseModel):
    verbose: bool
    report: bool
    tests: List[str]

test_router = APIRouter()
template_path = os.path.join(os.path.dirname(__file__), TEMPLATE_PATH)

templates = Jinja2Templates(directory=template_path)

def run_test(options: dict):
    command = ["pytest"]
    if options.get("verbose"):
        command.append("-vv")
    if options.get("report"):
        subprocess.run(["pytest", "--html=report.html", "--self-contained-html"])
    if len(options.get("tests")) > 0:
        command.extend(options.get("tests"))
    command.append("tests")


    command.append("--color=yes")
    result = subprocess.run(command, capture_output=True, text=True)
    conv = Ansi2HTMLConverter()
    html_logs = conv.convert(result.stdout)
    return html_logs

def find_all_tests_in_project():
    test_files = glob.glob("tests/**/*test*.py", recursive=True)
    tests = []
    for file in test_files:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("def test_"):
                    function_name = line.split("(")[0].replace("def ", "").strip()
                    tests.append(f'{file}::{function_name}')

    return tests

@test_router.get("/", response_class=HTMLResponse)
def output_tests(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tests": find_all_tests_in_project()}, media_type="text/html")

@test_router.post("/run")
def run_background(options: TestOptions):
    data = options.model_dump()
    logs = run_test(data)
    return {"logs": logs}



