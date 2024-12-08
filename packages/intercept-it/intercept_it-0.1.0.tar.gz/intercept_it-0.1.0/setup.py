from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='intercept-it',
    version='0.1.0',
    author="Simon Shalnev",
    author_email="shalnev.sema@mail.ru",
    description="Generic exception handlers",
    long_description=readme,
    url="https://github.com/pro100broo/intercept-it",
    keywords=["exceptions", "handler", "logger", "notifier", "asyncio"],
    packages=[
        'intercept_it',
        'intercept_it/utils',
        'intercept_it/loggers',
        'intercept_it/interceptors'],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed"
    ],
    install_requires=[
        "annotated-types==0.7.0",
        "colorama==0.4.6",
        "loguru==0.7.2",
        "pydantic==2.9.2",
        "pydantic_core==2.23.4",
        "pytz==2024.2",
        "setuptools==75.5.0",
        "typing_extensions==4.12.2",
        "win32-setctime==1.1.0"
    ]
)
