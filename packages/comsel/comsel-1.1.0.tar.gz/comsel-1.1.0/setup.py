from setuptools import setup, find_packages

setup(
    name='comsel',
    version='1.1.0',
    description='A wxPython-based COM port selection tool',
    long_description=open('README.md', encoding='utf-8').read(),  # Укажите кодировку
    long_description_content_type='text/markdown',
    author='Molisc',
    author_email='ivanrudko445@gmail.com',
    url='https://github.com/Molisc/ComSel',
    packages=find_packages(),  # Поиск всех пакетов (например, comsel, comsel.icons)
    include_package_data=True,  # Включение данных из MANIFEST.in
    install_requires=[
        'wxPython>=4.1.1',
        'pyserial>=3.5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
