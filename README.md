# Semantic version number tool (SVNT)

You can use this project to maintain a register of versions (especially API ones) of your projects.

All the versions will be saved in a database. You will be able to get the current version of project and update the version of the project via API.

## Local Environment 🚀

### Prerequisites 📋

You will need in your computer `Docker`, `docker-compose` and, of course, `git` to run it, but, is
highly recommended having also `Make`

The project will run inside Docker containers, and you can see what python packages are used in the pyproject.toml
file (poetry-based).

### Install 🔧

Installing SVNT is quite simple if you have Make.

Go to your project path and clone the repository:

After cloning it, go to the main path:

```shell script
$ cd SemanticVersionNumberTool
```

Then just use `make` command:

```shell script
$ make
```

Now all the magic will start if you have `docker` and `docker-compose` installed, all the volumes and containers
will be created.

After the deployment, you can check if all was ok by going to `http://localhost/admin/`. Then, if you see the Django-admin login
page ... IT WORKS!

![](https://media.tenor.com/images/202be43371949d5b86f8e58319debd88/tenor.gif)

By default, it will create a user with the name `admin` and password `root1234`.

If it does not work you can check for problems in logs using the following command:

```shell script
$ make alllogs
```

## Passing tests 🖥️

You can pass the test in your local environment just using the following command:

```shell script
$ make test
```

Or you can enter the docker container and be more specific

```shell script
$ make sh
$ pytest core/models/tests/test_version.py::VersionTest::test_next_version_not_valid
```

If there are more than 5 test that does not pass, you should use the next command if you want to run them all:

```shell script
$ make localtest
```
