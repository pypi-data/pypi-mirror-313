from setuptools import setup, find_packages # type: ignore

setup(
    name="pydatamining",  # Имя проекта (должно быть уникальным на PyPI)
    version="1.0.2",  # Версия проекта
    author="vladkanatov",
    author_email="vlad.kanatik@ya.ru",
    description="Parser module for send message in Apache Kafka",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/notickets/pydatamining",
    packages=find_packages(),  # Автоматически найдёт пакеты
    install_requires=[
        "aiohappyeyeballs==2.4.4",
        "aiohttp==3.11.9",
        "aiosignal==1.3.1",
        "attrs==24.2.0",
        "frozenlist==1.5.0",
        "idna==3.10",
        "kafka-python==2.0.2",
        "loguru==0.7.2",
        "multidict==6.1.0",
        "propcache==0.2.1",
        "python-decouple==3.8",
        "yarl==1.18.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)