from setuptools import setup, find_packages

def read_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name='comsel',  # Имя вашей библиотеки
    version='2.0.0',  # Версия
    description='A Python library for selecting COM port and baudrate',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Molisc',
    author_email='ivanrudko445@gmail.com',
    url='https://github.com/Molisc/comsel',  # URL вашего репозитория
    packages=find_packages(),  # Поиск всех пакетов в директории comsel
    install_requires=[  # Зависимости, которые будут установлены
        'pyserial',
        'dearpygui',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Минимальная поддерживаемая версия Python
)
