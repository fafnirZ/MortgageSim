#!/bin/bash

cmake -S . -B build -G "Ninja" \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake