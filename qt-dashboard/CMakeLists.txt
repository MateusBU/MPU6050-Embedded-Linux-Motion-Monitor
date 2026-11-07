cmake_minimum_required(VERSION 3.16)

project(MPU6050Dashboard LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 REQUIRED COMPONENTS
    Core
    Gui
    Qml
    Quick
)

qt5_add_resources(QML_RESOURCES qml.qrc)

add_executable(mpu6050_dashboard
    main.cpp
    ${QML_RESOURCES}
)

target_link_libraries(mpu6050_dashboard
    Qt5::Core
    Qt5::Gui
    Qt5::Qml
    Qt5::Quick
)
