install:
	VCPKG_MAX_CONCURRENTY=3 && vcpkg install
prebuild:
	cmake -S . -B build
build:
	cmake --build build
start:
	./build/