# PC Builder

## Overview

The **PC Builder** is an application designed to help users plan and
configure their ideal personal computer setup.
It allows users to select components based on their needs,
budget, and preferences, providing recommendations and compatibility checks.

## Team Members

- **Domantas Petkevičius** - Back-End Developer, Team Leader
- **Dagnis Matulis** - Back-End Developer
- **Juozas Krukauskas** - Front-End Developer
- **Simona Vytytė** - Front-End Developer

## Project Description

The PC Builder application provides an intuitive interface for users to:

- Browse and select various computer components (CPU, GPU, RAM, etc.)
- Filter parts by price, name, sort by price range and sort by keyword
- Add and remove parts from their personal build and display the current configurations.
- Get compatibility checks for selected components.
- Get suggested parts based on incompatibilities.
- Get intelligent suggestions based on set budget and use case.
- Get suggested full build based on set budget and use case.
- View estimated costs based on selected parts.

## Technologies Used

- **Programming Language:** _python_
- **Frameworks:** _typer_ for CLI interface
- **Testing:** _pytest_ and _unittest_ for unit and integration testing
- **Build Tools:** _tox_ for testing automation and building, _PyInstaller_ for creating executable files
  
## Useful Documents
- All useful documents that allow new team members or stakeholders to familiarize with our project and its practices can be found in docs/
- QA Documentation provides with information about our approach at testing and ensuring quality of the application [Link](docs/QA_documentation.md)
- UML_Deployment diagram provides an overview of how our application is built and deployed as a package to PyPI [Link](docs/UML_deployment.pdf)
- UML_Sequence diagram provides a graphical overview of simple runtime scenarios [Link](docs/UML_sequence.pdf)
- Code Style Guidelines document outlines the code standards and formatting/style guidelines that we follow and all new contributors should follow [Link](docs/code-style-guidelines.md)
- User Documentation provides really detailed explanations about how our CLI works and how to use it with everything explained step by step [Link](docs/user_documentation.md)

## Infrastructure Management

The project leverages Git for version control and GitHub for repository hosting. Continuous integration and deployment (CI/CD) are set up using GitHub Actions, streamlining the development workflow through automated testing and package deployment.

### Key Features of CI/CD:
#### Build and Test Automation:
* The CI pipeline uses tox to run automated tests and validate the application.
* A virtual environment is created for Python 3.11, ensuring consistency across environments.
#### Artifact Management:
* Build artifacts, such as .tar.gz and .whl files, are generated using python -m build and uploaded for further use.
#### Conditional Deployment:
* Deployments to PyPI occur only on pushes to the main branch. If a version already exists, the deployment step is gracefully skipped.
#### Concurrency Management:
* Prevents multiple workflows for the same commit with a concurrency setup.
* This workflow ensures that each new change is thoroughly tested and, if valid, automatically packaged and deployed to PyPI, enabling continuous delivery of the application.

## Installing the PC Builder Package

- You can easily install the PC Builder package via pip from PyPI:
  ```bash
  pip install pc-builder
  ```
- Once installed, you can use the pcbuilder command in your terminal to run the application:
  ```bash
  pcbuilder
  ```

## Building and Running the Application from source

This guide provides instructions for developers or contributors to set up the PC Builder project, run tests, and build the application from source.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.7 or later**: Download and install Python from [python.org](https://www.python.org/downloads/).
- **pip**: This usually comes pre-installed with Python. You can check if you have pip installed by running:
  ```bash
  pip --version
  ```

### Building and Running the Application Locally

- Clone the repository https://github.com/mif-it-se-2024/group-project-pc-builders
- Navigate to the Project Directory
  ```bash
  cd pc_builder
  ```
- Create a Virtual Environment (Optional but Recommended)

  Windows:

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

  Linux:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- Install Project Dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Run tests and build the application

  ```bash
  tox
  ```

- Launch the application
  ```bash
  cd dist
  ```
  ```bash
  pcbuilder.exe ( Windows ) or ./pcbuilder ( Linux )
  ```
