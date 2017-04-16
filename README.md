PyTriggerTrap
=============

Control a TriggerTrap device without the smartphone app.

A TriggerTrap is (or
[was](https://medium.com/triggertrap-playbook/triggertrap-going-out-of-business-faq-988112eebfef))
a device that you can plug into your camera in order to control it with your smartphone.

However, in some cases you don't really want to actually control it with your smartphone although
it's nice to have a simple way to control it. The sad thing is that isn't any documentation or API
to do that. The good thing is that the protocol is actually pretty simple and the aim of this
project is to provide a way for Python developers to control TriggerTrap devices.

## Installation

Well, use the source Luke. Releasing may come soon.

### Non-python requirements

This tool uses the `ffmpeg` binary, please make sure that it is installed and present in your
`PATH`.


## Usage

There is two ways to use this too:

- Using the `pytt` CLI tool, that allows to do most things from the shell
- Using the `TTController` class, for developers

If you want to use the class, then read the code, it is documented via docstrings.

### The `pytt` tool

Different actions allow you to access the different features of the controller class.

#### `timelapse_file`

This will generate a "timelapse file". Here's the idea: a TriggerTrap is controlled via an audio
signal. So if a device can generate the appropriate audio, then it will be able to control the
camera. In the case of time lapses, it involves letting the thing running for a long time, maybe
while you're not even there. In this case, it is really annoying to have to leave your phone there.

The solution is the following: you just need to dig out an old MP3 player (anything will do the job)
and then to generate a MP3 file that will be a pre-generated audio signal. You can generate it of
the right size if you want a precise duration or just generate a few iterations and then put the
file on "loop" in your player.

So:

1. Generate the timelapse MP3 file
2. Put the file in your player
3. Plug the TriggerTrap on your player
4. Play the music
5. Wait for your timelapse to be complete

Suppose that I want to watch something for 6 hours (21600 seconds) in order to produce a 30 seconds
timelapse video. Here's the command:

```
pytt timelapse_file -i 21600 -o 30 -f timelapse.mp3
```

See the command's built-in help for the options.

#### `trigger`

This will simply send a trigger to the camera. Just make sure that the TriggerTrap is connected to
your computer's audio.

Example

```
pytt trigger
```

See the command's built-in help for more options.
