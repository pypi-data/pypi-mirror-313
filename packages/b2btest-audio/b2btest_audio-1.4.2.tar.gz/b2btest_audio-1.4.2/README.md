# b2btest audio - audio data support for back-to-back tests


[![CI](https://github.com/vokimon/back2back_audio/actions/workflows/main.yml/badge.svg)](https://github.com/vokimon/back2back_audio/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/vokimon/back2back_audio/badge.svg?branch=master)](https://coveralls.io/github/vokimon/back2back_audio?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/b2btest_audio)](https://pypi.org/b2btest_audio)
[![PyPI - Version](https://img.shields.io/pypi/v/b2btest_audio)](https://pypi.org/b2btest_audio)


![B2BLogo](icon_b2btest.png)

This package adds audio file support to b2btest.
b2btest is a tool to automate tests that compare results
to some previous ones, and this plugin,
is helpful to compare audiofiles in a sensible way.

See [b2btest README](https://github.com/vokimon/back2back)
for a deeper discussion on why you should avoid back-to-back testing,
although sometimes it is the lesser evil way to proceed.

This plugin handles audiofiles specially in several ways:

- Instead of doing a text or byte difference, it interprets the audio contents and compares them sample by sample.
- It considers two outputs to be different if:
  - Metadata differs
  - Sample-by-sample differs relative to the audio level
- In the case of differences, it generates a diff audio by substracting both waves sample by sample.

By means of `python-wavefile`, it supports floating point samples, and multichannel waves.

How to install
--------------

Just use:

```bash
$ pip install b2btest_audio
```

Dependencies
------------

This plugin requires the [wavefile] module,
which in turn requires having [libsndfile] library installed in your system.

[wavefile]: https://github.com/vokimon/python-wavefile
[libsndfile]: http://www.mega-nerd.com/libsndfile/


Back2Back testing of cli programs
---------------------------------

When you are testing back-to-back the output of a command line,
you define a yaml file like this (name it b2bcases.yaml).

```yaml
#!/usr/bin/env back2back 

datapath: "b2bdata" # Point it to the directory containing your reference data
testcases:

  Generate1KHzSine:
    command: sox -n /tmp/sine.wav synth 1.0 sine  1000.0
    outputs:
    - /tmp/sine.wav
```

Ouputs with supported audio file extension will be recognize
and this plugin diff will be used for them.

See [b2btest] documentation on how to use this file.

Command line tool
-----------------

The package also provides a `diffaudio` CLI tool to generate the audio difference



