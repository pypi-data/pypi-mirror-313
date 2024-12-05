from setuptools import setup, find_packages

setup(
    name="better-test-preview",
    version="0.0.6",
    description="FastAPI app",
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
