install:
	VCPKG_MAX_CONCURRENTY=4 && vcpkg install
prebuild:
	./prebuild.sh
compile:
	cd build && ninja
start:
	./build/