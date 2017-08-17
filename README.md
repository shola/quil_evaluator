# Quil Evaluator Web App

### Table of Contents

- [Intro](#intro)
- [Folder Structure](#folder-structure)
- [Available Scripts](#available-scripts)
  - [python start.py](#npm-start)

### Intro
This web app allows you to type in the text of a Quil program, and evaluate
it using Rigetti Forest. All Quil programs that you evaluate will be saved in
the `your_quil_files` directory for future reference, and can be manually
deleted at any time.

**WARNING:** This app is  only intended to be hosted from your laptop
(for security reasons).

**REQUIREMENTS**
- You have a valid Forest API Key and have already setup pyQuil on your laptop. If you need help doing so, please see the resources here: [pyQuil Installation and Getting Started](http://pyquil.readthedocs.io/en/latest/getting_started.html)
- NodeJS is installed globally
- the following python libraries are installed: flask, flask_cors, numpy.

### Folder Structure

The filesystem should look like this:
```
quil_evaluator
├── .pyquil_config_template
├── LICENSE
├── README.md
├── index.py
├── start.py
├── quil_frontend
│   ├── README.md
│   ├── build
│   │   ├── index.html
│   │   └── static
│   │       ├── css
│   │       │   └── main.XXXXXXXXX.css
│   │       └── js
│   │           └── main.XXXXXXXXX.js
│   ├── package.json
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   └── index.js
│   └── yarn.lock
├── static -> quil_frontend/build/static/
├── templates
│   └── index.html -> ../quil_frontend/build/index.html
└── your_quil_files/
```

### Available Scripts

In the project directory, you can run:

#### `python start.py --setup`

Only needed for the first time run of this app. You will be prompted for your
Rigetti Forest API Key, which will then be saved into `.pyquil_config`.

#### `python start.py`

Start up the app on your laptop.
Open [http://localhost:5000](http://localhost:5000) to view it in the browser,
then try entering this Quil program into the web app and evaluate it:
```
H 0
CNOT 0 1
MEASURE 0 [0]
```

#### TODO
- [ ] localforage persistence
- [ ] click to copy wavefunction or classical measurement to clipboard
