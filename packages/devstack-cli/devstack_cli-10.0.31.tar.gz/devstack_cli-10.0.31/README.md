# DevStack CLI

The `devstack-cli` provides command-line access to Remote Development Environments (RDEs) created by Cloudomation DevStack. Learn more about [Cloudomation DevStack](https://docs.cloudomation.com/devstack/docs/overview-and-concept).

## Installation

The following binaries must be installed to be able to use `devstack-cli`:

* `ssh`
* `ssh-keyscan`
* `rsync`
* `git`

On Debian/Ubuntu the packages can be installed with

```
apt install openssh-client rsync git
```

Then you can install `devstack-cli` by running

```
python -m pip install devstack-cli
```

## Usage

```
usage: devstack-cli [-h] -H HOSTNAME -s SOURCE_DIRECTORY [-o OUTPUT_DIRECTORY] [-v]
```

You need to specify the hostname/IP of the RDE created by Cloudomation DevStack as well as the path to a directory where the sources will be cached locally. Optionally you can specify an output directory where artifacts created on the RDE will be stored locally.
The `-v` switch enables debug logging.

## Support

`devstack-cli` is part of Cloudomation DevStack and support is provided to you with an active subscription.

## Authors and acknowledgment

Cloudomation actively maintains the `devstack-cli` command line tool as part of Cloudomation DevStack

## License

Copyright (c) 2024 Starflows OG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.