from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="better-test-preview",
    version="0.1.0",
    description="FastAPI app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "jinja2",
        "pydantic",
        "pytest",
        "pytest-html",
        "ansi2html",
    ],
    author="HangoverHGV",
    include_package_data=True,
    data_files=[("templates", ["better_test_preview/better_test_preview/templates/index.html"])]
)
