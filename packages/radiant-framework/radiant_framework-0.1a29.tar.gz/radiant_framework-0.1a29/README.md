# Radiant Framework

A Brython Framework for Web Apps development.

![GitHub top language](https://img.shields.io/github/languages/top/un-gcpds/brython-radiant?)
![PyPI - License](https://img.shields.io/pypi/l/radiant?)
![PyPI](https://img.shields.io/pypi/v/radiant?)
![PyPI - Status](https://img.shields.io/pypi/status/radiant?)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/radiant?)
![GitHub last commit](https://img.shields.io/github/last-commit/un-gcpds/brython-radiant?)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/UN-GCPDS/brython-radiant?)
[![Documentation Status](https://readthedocs.org/projects/radiant/badge/?version=latest)](https://radiant-framework.readthedocs.io/en/latest/?badge=latest)



## Overview
Radiant Framework is a novel web framework designed to leverage the capabilities of [Brython](https://brython.info/), a browser-based Python implementation. This innovative approach allows developers to write web applications entirely in Python, bypassing the conventional requirements of HTML, CSS, or JavaScript for frontend development.

## Key Features

### Python-Centric Development
- **Unified Language Usage**: Write your entire web application using Python, ensuring a consistent and streamlined coding experience.
- **Brython Integration**: Utilizes Brython for executing Python code in the browser, enabling a seamless transition of server-side code to client-side execution.

### Server and Browser Compatibility
- **Dual Environment Execution**: Radiant enables the same application code to run both on the server and in the browser, maximizing code reusability and efficiency.
- **Tornado Web Server**: On the server-side, Radiant harnesses the [Tornado](https://www.tornadoweb.org/) web server to deploy applications, known for its scalability and non-blocking network I/O capabilities.

### Resource Management
- **Static File Handling**: Simplifies the management of static files (images, stylesheets, etc.), by setting up a local path for their serving, facilitating their inclusion in the application.

### Runtime Configuration
- **Dynamic HTML Templates**: Radiant offers a custom HTML template system, configurable at runtime, to dynamically import server-side scripts into the browser environment.

## Benefits
- **Streamlined Development Process**: By unifying the development language and environment, Radiant significantly reduces the complexity and learning curve associated with traditional web development.
- **Code Efficiency**: Eliminates the need for writing separate frontend and backend code, leading to more maintainable and concise codebases.
- **Focus on Quality**: Developers can concentrate on crafting high-quality Python code, without the distractions of dealing with various web technologies.

## Installation

To install Radiant, you can use `pip`, the Python package manager. Simply run the following command in your terminal:



```python
pip install radiant-framework
```

## Bare minimum

To help you get started with Radiant, let's walk through a bare minimum example. This example will demonstrate how to create a simple web page that displays some text. We'll utilize the Radiant framework to craft the page and run it on a local server. This is an excellent way to familiarize yourself with how Radiant functions and to begin exploring its capabilities.

### Prerequisites
Before proceeding, ensure that you have Radiant installed on your system. If you haven't installed Radiant yet, please refer to the [Installation](#installation) section for guidance.

### Creating a Simple Web Page

The following script illustrates a basic application using Radiant. This script will set up a simple web page displaying a heading.


```python
from radiant.framework.server import RadiantAPI
from browser import document, html

class BareMinimum(RadiantAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        document.select_one('body') <= html.H1('Radiant-Framework')

if __name__ == '__main__':
    BareMinimum()
```
