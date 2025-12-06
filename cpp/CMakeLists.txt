# Minimum required version of CMake
cmake_minimum_required(VERSION 3.16)

# Set the project name and version
project(pni_pilot VERSION 1.0.0 LANGUAGES CXX)


# --- C++ Standard Setting ---

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_EXTENSIONS OFF) 

# --- Qt Setup ---

find_package(Qt6 COMPONENTS Core Widgets Gui REQUIRED)

add_subdirectory(src)
qt_add_executable(pni_pilot src/main.cpp)


# --- Linking and Target Configuration ---

# Link the executable against the required Qt modules
target_link_libraries(pni_pilot
    PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
)


# Apply standard Qt property settings (needed for things like moc, rcc, and uic)
target_compile_features(pni_pilot PRIVATE cxx_std_17)
target_compile_options(pni_pilot PRIVATE "$<$<CXX_COMPILER_ID:MSVC>:/W3>" "$<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall>")
target_include_directories(pni_pilot PRIVATE "${CMAKE_SOURCE_DIR}")
set_target_properties(pni_pilot PROPERTIES 
    # This property ensures the MOC tool is run for headers with the Q_OBJECT macro
    AUTORCC ON
    AUTOMOC ON
    AUTOUIC ON
)