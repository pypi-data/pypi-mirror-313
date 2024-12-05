from setuptools import setup, find_packages

setup(
    name="pingpongx",
    version="0.1.1",
    author="Karan Kapoor",
    author_email="kaykay9464769@gmail.com",
    description="A dynamic notification delivery system with Redis and Kafka integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/karan-kap00r/PingPong",  # GitHub repository link
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "redis",
        "kafka-python",
        "google-cloud-firestore",
        "requests",
        "pydantic",
        "Jinja2",
        "PyJWT",
        "passlib",
        "bcrypt",
        "twilio"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
