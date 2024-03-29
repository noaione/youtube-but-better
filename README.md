# I Heckin' Love YouTube

[![Build Status](https://img.shields.io/github/actions/workflow/status/noaione/youtube-but-better/auto-build.yml)](https://github.com/noaione/youtube-but-better/actions/workflows/auto-build.yml) [![Release](https://img.shields.io/github/v/release/noaione/youtube-but-better)](https://github.com/noaione/youtube-but-better/releases/latest) [![Download Count](https://img.shields.io/github/downloads/noaione/youtube-but-better/latest/total)](https://github.com/noaione/youtube-but-better/releases/latest)

This repository provide an automated build for a certain YouTube client.

What it does:
- Check the latest YouTube target
- Download the `nodpi` version
- Do all default patching
  - Root
  - Non-root version
- Upload to [Releases](https://github.com/noaione/youtube-but-better/releases/latest)

## Installing

See [releases](https://github.com/noaione/youtube-but-better/releases/latest) section.

If you use non-root version, you will need:
- https://github.com/inotia00/VancedMicroG/releases

If you use rooted version, use `adb` to install the package, make sure you install whatever YouTube version that you want to patch with this version.

## Verifying

To make sure the APK's is not tampered by this repository author, each automated build will have a checksum section which are SHA256 hash of the APKs files to make sure it has not been tampered in one way or another.

You can also verify the build code in the [scripts](https://github.com/noaione/youtube-but-better/tree/master/scripts) folder

If somehow the releases part has been tampered, you can view the [Actions](https://github.com/noaione/youtube-but-better/actions/workflows/auto-build.yml) and see the latest successful release build and see the step summary which should have an unmodified checksum.
