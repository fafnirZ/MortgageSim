# Minimum required version of CMake
cmake_minimum_required(VERSION 3.16)

# Set the project name and version
project(MyQt6App VERSION 1.0.0 LANGUAGES CXX)

# --- C++ Standard Setting ---

# Enforce the C++17 standard for the entire project
set(CMAKE_CXX_STANDARD 17)
# Ensure the compiler uses the specific standard, not just "at least" it
set(CMAKE_CXX_STANDARD_REQUIRED True)
# Enable common compiler extensions (often needed for Qt code)
set(CMAKE_CXX_EXTENSIONS OFF) 

# --- Qt Setup ---

# Find the Qt6 package. We minimally need 'Core' and 'Widgets' for a GUI app.
# Add more modules (like Network, Qml, Sql, etc.) as needed.
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)

# --- Source Files and Executable ---

# Define the list of source files
set(SOURCE_FILES
    main.cpp
    mainwindow.cpp
)

# Define the list of header files
set(HEADER_FILES
    mainwindow.hpp
)

# Define the list of Qt resource files (optional)
# set(RESOURCE_FILES
#    resources.qrc
# )

# Define the list of Qt UI form files (optional)
# set(UI_FILES
#    mainwindow.ui
# )

# Use Qt's macro to handle the build steps for UI and resources (if you have them)
# if(UI_FILES)
#     qt_add_executable(MyQt6App
#         ${SOURCE_FILES}
#         ${HEADER_FILES}
#         ${UI_FILES}
#         ${RESOURCE_FILES}
#     )
# else()
    # Basic executable if no UI or resources are used
    qt_add_executable(MyQt6App
        ${SOURCE_FILES}
        ${HEADER_FILES}
    )
# endif()


# --- Linking and Target Configuration ---

# Link the executable against the required Qt modules
target_link_libraries(MyQt6App
    PRIVATE
        Qt6::Core
        Qt6::Widgets
)

# Apply standard Qt property settings (needed for things like moc, rcc, and uic)
target_compile_features(MyQt6App PRIVATE cxx_std_17)
target_compile_options(MyQt6App PRIVATE "$<$<CXX_COMPILER_ID:MSVC>:/W3>" "$<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall>")
target_include_directories(MyQt6App PRIVATE "${CMAKE_SOURCE_DIR}")
set_target_properties(MyQt6App PROPERTIES 
    # This property ensures the MOC tool is run for headers with the Q_OBJECT macro
    AUTORCC ON
    AUTOMOC ON
    AUTOUIC ON
)