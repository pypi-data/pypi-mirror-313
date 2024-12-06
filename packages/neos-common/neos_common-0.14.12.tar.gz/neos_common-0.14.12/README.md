# NEOS Platform Common Code v0.14.12

## Prerequisites

The following packages are used across python repositories. A global install of them all is *highly* recommended.

* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [Invoke](https://www.pyinvoke.org/installing.html)

### WSL

If running on Windows, you may need to install `distutils` to install the service.

```bash
$ sudo apt-get install python3.8-distutils
```

## Initial setup

```bash
$ invoke install-dev
```

### Install on MacOS

* Install kafka dependencies

```bash
$ brew install librdkafka
```

* Setup environment variables on .bashrc or .zshrc

```bash
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
export LIBRARY_PATH="/opt/homebrew/lib"
```

* Execute the following command to install the dependencies

```bash
$ invoke install-dev
```

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

## Linting

```bash
invoke check-style
invoke isort
```

## Releases

Release management is handled using `changelog-gen`. The below commands will
tag a new release, and generate the matching changelog entries. Jenkins will
then publish the release to the artifact repository.

```bash
$ invoke release
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
