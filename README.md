# VoteApp

## Introduction

This is an app that emulates an electronic voting system like those used on machine voting driven elections.
Developed in ***Python*** with *KivyMD*.

## Video Presentation

[![Vote App Video](https://img.youtube.com/vi/CBtlW1eGJSk/mqdefault.jpg)](https://youtu.be/CBtlW1eGJSk)

## Packaging

### Packaging App for Android

First you’ll need to install a package called ***buildozer*** with pip:
```
pip install buildozer
```

Then, create a new folder and navigate to it in your terminal. Once you’re there, you’ll need to run the following command:
```
buildozer init
```

This will create a `buildozer.spec` file that you’ll use to configure your build. For this example, you can edit the first few lines of the spec file as follows:
```
[app]

# (str) Title of your application
title = Vote

# (str) Package name
package.name = vote

# (str) Package domain (needed for android/ios packaging)
package.domain = org.vote
```

At this point, you’re almost ready to build your application, but first, you’ll want to install the [dependencies](https://buildozer.readthedocs.io/en/latest/installation.html#targeting-android) for buildozer. Once those are installed, copy your calculator application into your new folder and rename it to main.py. This is required by buildozer. If you don’t have the file named correctly, then the build will fail.

Now you can run the following command:

```
buildozer -v android debug
```

The build step takes a long time! Depending on your hardware, it may take even longer, so feel free to grab a cup of coffee or go for a run while you wait. Buildozer will download whatever ***Android SDK*** pieces it needs during the build process. If everything goes according to plan, then you’ll have a file named something like `vote-0.1-debug.apk` in your bin folder.


### Packaging App for iOS


The instructions for building an application for iOS are a bit more complex than Android. For the most up-to-date information, you should always use Kivy’s official packaging [documentation](https://kivy.org/doc/stable/guide/packaging-ios.html). You’ll need to run the following commands before you can package your application for iOS on your Mac:

```
brew install autoconf automake libtool pkg-config
```

```
brew link libtool
```

```
pip install cython kivy-ios
```

Once those are all installed successfully, you’ll need to compile the distribution using the following command:

```
toolchain build python3 kivy
```

If you get an error that says iphonesimulator can’t be found, then see this [StackOverflow](https://stackoverflow.com/questions/39564420/i-get-xcrun-error-sdk-iphonesimulator-cannot-be-located-when-running-the-t) answer for ways to solve that issue. Then try running the above commands again.

If you run into SSL errors, then you probably don’t have Python’s OpenSSL setup. This command should fix that:

```
cd /Applications/Python\ 3.7/
```

```
./Install\ Certificates.command
```

Now go back and try running the toolchain command again.

Once you’ve run all the previous commands successfully, you can create your Xcode project using the toolchain script. Your main application’s entry point must be named main.py before you create the Xcode project. Here is the command you’ll run:

```
toolchain create <title> <app_directory>
```

There should be a directory named title with your Xcode project in it. Now you can open that project in Xcode and work on it from there. Note that if you want to submit your application to the App Store, then you’ll have to create a developer account at [developer.apple.com](https://developer.apple.com/) and pay their yearly fee.


### Packaging App for Windows


You can package your Kivy application for Windows using `PyInstaller`. If you’ve never used it before, then check out [Using PyInstaller to Easily Distribute Python Applications](https://realpython.com/pyinstaller-python/) .

You can install PyInstaller using pip:

```
pip install pyinstaller
```

The following command will package your application:

```
pyinstaller main.py -w
```

This command will create a Windows executable and several other files. The `-w` argument tells PyInstaller that this is a windowed application, rather than a command-line application. If you’d rather have PyInstaller create a single executable file, then you can pass in the `--onefile `argument in addition to `-w`.


### Packaging App for macOS


You can use [PyInstaller](https://www.pyinstaller.org/) to create a Mac executable just like you did for Windows. The only requirement is that you run this command on a Mac:

```
pyinstaller main.py -w --onefile
```

This will create a single file executable in the dist folder. The executable will be the same name as the Python file that you passed to PyInstaller. If you’d like to reduce the file size of the executable, or you’re using GStreamer in your application, then check out Kivy’s [packaging page for macOS](https://kivy.org/doc/stable/guide/packaging-osx.html) for more information.

