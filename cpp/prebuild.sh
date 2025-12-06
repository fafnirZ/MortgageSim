#!/bin/bash

# ensures clean build
rm -rf build

cmake -S . -B build \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake