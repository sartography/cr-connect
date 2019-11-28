# CR Connect Administrative Console
The CR Connect Administrative Console provides:
 * a development environment
 * a test runner
 * a deployment console

## Development and Administrative Setup
These steps are necessary both for spinning up the development
constellation and for enabling the administrative console for
deployments.

### Tools
These instructions assume you're using these development and tools:
- Operating System: Ubuntu

### Environment Setup
Make sure all of the following are properly installed on your system:
1. `python3` & `pip3`:
    - [Install python3 & pip3](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-18-04-server)
    - [Installing Python 3 on Linux](https://docs.python-guide.org/starting/install3/linux/)
2. `pipenv`:
    - [Install pipenv](https://pipenv-es.readthedocs.io/es/stable/)
    - [Add ${HOME}/.local/bin to your PATH](https://github.com/pypa/pipenv/issues/2122#issue-319600584)

### Project Initialization
1. Clone this repository.
2. Install the required packages:
    ```pipenv install```
3. Confirm you can run invoke:
    ```inv -l```

## How to use

Once things are setup, the basic operation is simple and takes place
via invoke tasks.

####To list the tasks available:
```
inv -l
```

####To get task-specific help:
```
inv <task name> -h
```
