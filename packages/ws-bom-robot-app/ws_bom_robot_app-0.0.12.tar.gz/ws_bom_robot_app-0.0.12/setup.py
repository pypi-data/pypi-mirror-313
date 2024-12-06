from setuptools import setup, find_packages

setup(
    name="ws_bom_robot_app",
    version="0.0.12",
    description="A FastAPI application serving ws bom/robot/llm platform ai.",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Websolute Spa",
    author_email="dev@websolute.it",
    url="https://github.com/websolutespa/bom",
    packages=find_packages(),
    install_requires=[line.split('#')[0].strip() for line in open("ws_bom_robot_app/requirements.txt").readlines() if all([line.strip(), not line.startswith("#")])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)

