* website: <https://arrizza.com/pyalamake>
* installation: see <https://arrizza.com/setup-common>

## Summary

This Python module generates a multi-target Makefile for cross-platform projects all of which is compatible with
JetBrain's Clion IDE.

For example, see gen.py for a Python script (gen.py) that generates:

* two Arduino projects and an Arduino core for them
* a GTest project to run UTs against an Arduino Project
* a C/++ project

all into one Makefile, and all recognized by CLion.

See also gen_3cores.py that shows how to build 3 Arduino on 3 different boards in the same project and same Makefile.

## Why not CMake?

I use JetBrain's CLion. Ut can handle only a CMake or Makefile based project.

Also, I like to use GTest to UT my Arduino projects (if possible). But CMake can't handle a project that uses
two compilers i.e. avr-gcc for Arduino and gcc for GTest. It tried some different CMake techniques
to allow that but they either didn't work or CLion still didn't recognize the components being used.

The only option then was to use Python to generate a Makefile that CLion was compatible with.

## Why not ninja instead of make?

Because CLion can't use that to self-configure. CMake in CLion can be configured to use
Ninja, but the IDE uses CMake to configure itself for the project. Therefore, Makefile.

## Why?

Currently, I have relatively simple projects using one Arduino and some GTest UTs. But I do have some
projects that could use multiple Arduino's communicating with each other. And possibly some other
microcontrollers e.g. STM32, ESP32, etc. that communicate with Arduino's or themselves.

CLion can't handle that.

But (finger crossed) I should be able to extend pyalamake to build STM32 and ESP32 targets relatively easily, still
allow
GTests for those microcontrollers, etc.

## Limitations

* works only on Ubuntu. There will likely be additional work needed for macOS and Windows.
* Arduino libraries can not be added to a target.
* See todo.md for more work to be done.
* tested with an Arduino Nano (boardid: nano-atmega328old), Arduino MegaADK (boardid: megaadk) and Arduino Uno (boardid:
  uno).
  Other boards should work correctly, but there is always a possibility it fails.
* I have not tested using an Arduino programmer
* I have not tested an app that requires Arduino EEPROM uploads.

## How to use

```bash
./gen.py    # to generate/update the Makefile

make help   # to show the list of makefile targets

make                # build all targets: Arduino core, both blink targets, GTest UT, and sample C++ app

make blink-upload   # upload the blink app to an Arduino; 
                    # should blink random times (2 - 15) and random rate (0 - 255ms);
make blink2-upload  # upload the blink2 app to an Arduino;
                    # should blink 2 times
make core           # build the Arduino Core

make ut-run         # run the GTEST unit tests
make ut-cov         # show the source code coverage of the GTEST UTs
                    # open debug/ut.html in a browser for a gcov HTML report
make ut-cov-reset   # reset the coverage data

make hello-run            # run C++ hello world app
make hello-run s="john"   # to pass a CLI args to hello world 

make clean         # clean all
make <tgt>-clean   # clean a specific target
```

## updating gen.py

```python
from pyalamake.lib.pyalamake import alamake

# specify all components to be added to the makefile
# ... skip see below ...

# === generate makefile for all targets
alamake.makefile()

```

At this point, the Makefile should contain all targets specified

#### Arduino targets

Creating an Arduino .hex requires 3 steps:

1) gen an Arduino Shared component
    * holds common, shared information like boardid, serial port, etc.
2) gen an Arduino Core
    * use the same shared component created above
    * holds the Arduino Core library compiled for the same boardid, etc.
3) gen the Arduino App
    * use the same shared component created above
    * holds the Arduino app compiled for the same boardid etc.

A shared component and core can be used with multiple Arduino targets.

Example generation of an Arduino shared component:

```python
sh1 = alamake.create_arduino_shared()
sh1.set_boardid('nano-atmega328old')
# sh1.set_boardid('uno')
# sh1.set_boardid('megaadk')

# on Ubuntu, different boards use different serial ports 
if sh1.boardid in ['uno', 'megaadk']:
    sh1.set_avrdude_port('/dev/ttyACM0')
else:
    sh1.set_avrdude_port('/dev/ttyUSB0')

# at this point sh1 is only missing core related settings
```

Example generation of an Arduino core:

```python
# share the same component created above
core = alamake.create('core', 'arduino-core', shared=sh1)
# no additional directories, libs, etc. needed
core.check()
```

Example generation of an Arduino target:

```python
# share the same component created above
blink = alamake.create('blink', 'arduino', shared=sh1)
blink.add_sources([
    'src/blink.cpp',
    'src/common.cpp',
])
blink.add_include_directories(['src'])
```

#### GTest target

Example generation of a GTest target that tests an Arduino app

```python
ut = alamake.create('ut', 'gtest')

# tests the blink2.cpp (Arduino) in src2 directory
ut.add_include_directories([
    'src2',
    'ut/mock_arduino',
])

# uses a Mock Arduino library to check blink2 behavior
ut.add_sources([
    'ut/mock_arduino/mock_arduino.cpp',
    'ut/ut_test1.cpp',
])

# specify the directory(s) that should be part of the coverage report
ut.add_coverage(['src2'])

```

#### C++ targets

Example generation of a C++ target

```python
hello = alamake.create('hello', 'cpp')
hello.add_include_directories(['src'])
hello.add_sources([
    'src/hello.cpp',
])
```

## Convert Arduino from cmake

Convert:

```cmake
cmake_minimum_required(VERSION 3.16)
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/arduino-cmake/ArduinoToolchain.cmake)

project(blink)
print_board_list()
# set to your board
set(MY_BOARD nano328p)
set(MY_PORT /dev/ttyUSB0)
```

to:

```python
# === create a shared component for core and arduino project
sh1 = alamake.create_arduino_shared()
sh1.set_boardid('nano-atmega328old')
sh1.set_avrdude_port('/dev/ttyUSB0')
# at this point sh1 is only missing core related settings

# === arduino core
core = alamake.create('core', 'arduino-core', shared=sh1)
# no additional directories, libs, etc. needed
core.check()

# === arduino blink
blink = alamake.create('blink', 'arduino', shared=sh1)
```

Convert:

```cmake
generate_arduino_firmware(${CMAKE_PROJECT_NAME}
        # NOTE: these are converted above
        BOARD ${MY_BOARD}
        PORT ${MY_PORT}   # note: required otherwise will not generate upload target

        SRCS src/main.cpp
)
```

to:

```python

blink = alamake.create('blink', 'arduino', shared=sh1)
blink.add_sources([
    'src/main.cpp',
])
blink.add_include_directories(['src'])
```

## Convert gtest

TODO

## Convert C++

TODO
