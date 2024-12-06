from setuptools import setup, find_packages

readme = """
# ~~Flask-BigApp~~

**🚨PROJECT HAS MOVED TO Flask-Imp🚨**

[https://github.com/CheeseCake87/flask-imp](https://github.com/CheeseCake87/flask-imp)

---

Do you have an idea for a flask extension and want to use the name 
Flask-BigApp? 

Contact me and we can discuss it.

(The name is up for grabs on the condition that your Flask extension is 
transferred to the [Pallets-Ecosystem](https://github.com/pallets-eco))

---

## What is Flask-BigApp?

Flask-BigApp's main purpose is to help simplify the importing of blueprints, resources and models.
It has a few extra features built in to help with securing pages and password authentication.

## Getting Started

### Setup.

Create a new project folder and navigate to it.

```text
# Linux
cd /path/to/project-folder

# Windows
cd C:\path\to\project-folder
```

### Create a virtual environment and activate it.

**Linux / MacOS**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

### Install Flask-BigApp

```bash
pip install flask-bigapp
```

### Create a new project.

```bash
flask-bigapp init
```

---

## Working on this project.

### Setup.

**Create a new project folder and navigate to it in the terminal, then clone this repository.**

```bash
git clone https://github.com/CheeseCake87/Flask-BigApp.git
```

### Create a virtual environment and activate it.

**Linux / MacOS**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

### Install the requirements.

```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Install the local version of Flask-BigApp.

```bash
pip install -e .
```

### Run the Flask app.

```bash
Flask run
```

### Run the tests.

```bash
pytest
```

### Info

The Flask app is located in the `app` folder. The tests are located in the `tests` folder.

The tests are linked to the tests blueprint located at `app/blueprints/tests`.
"""

setup(
    name='Flask-BigApp',
    version='2.4.0',
    url='https://github.com/CheeseCake87/Flask-BigApp',
    license='GNU Lesser General Public License v2.1',
    author='David Carmichael',
    author_email='david@uilix.com',
    description='A Flask auto importer that allows your Flask apps to grow big.',
    long_description=f'{readme}',
    long_description_content_type='text/markdown',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
    ],
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'toml',
    ],
    zip_safe=False,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flask-bigapp = flask_bigapp_cli:cli',
        ]
    }
)
