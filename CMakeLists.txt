cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(sapien LANGUAGES C CXX CUDA)

if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY MultiThreaded)
endif()


set(CMAKE_CXX_STANDARD 20)

if(MSVC)
    add_compile_options("$<$<COMPILE_LANGUAGE:CXX>:/W4>" "$<$<CONFIG:Release>:$<$<COMPILE_LANGUAGE:CXX>:/O2>>")
else()
    add_compile_options("-Wall"
        "$<$<CONFIG:Debug>:-g3>" "$<$<CONFIG:Debug>:-O0>"
        "$<$<CONFIG:Release>:-O3>")
endif()

add_compile_definitions("$<$<CONFIG:DEBUG>:_DEBUG>")
add_compile_definitions("$<$<CONFIG:DEBUG>:VK_VALIDATION>")
add_compile_definitions("$<$<CONFIG:DEBUG>:VK_CORE_LOGGING>")
add_compile_definitions("$<$<NOT:$<CONFIG:Debug>>:NDEBUG>")

set(CMAKE_DEBUG_POSTFIX "")

option(BUILD_SHARED_LIBS "Build using shared libraries" OFF)
option(SAPIEN_PROFILE "Build SAPIEN with profiler" ON)
option(SAPIEN_DEBUG_VIEWER "Build debug viewer for debugging renderer in C++" OFF)
option(SAPIEN_CUDA "Enable SAPIEN CUDA functionalities, including dlpack, CUDA buffer, denoiser, and simsense" ON)

option(SAPIEN_BUILD_PYTHON "Build Python binding, only intended to generate compile_commands.json for IDE" OFF)
option(SAPIEN_BUILD_TEST "build unit tests")


set(SAPIEN_PHYSX5_DIR "" CACHE STRING "Directory for precompield PhysX5")

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif ()

if (WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

macro(FetchContent_MakeAvailableExclude)
    FetchContent_GetProperties(${ARGV})
    if(NOT ${ARGV}_POPULATED)
        FetchContent_Populate(${ARGV})
        add_subdirectory(${${ARGV}_SOURCE_DIR} ${${ARGV}_BINARY_DIR} EXCLUDE_FROM_ALL)
    endif()
endmacro()

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(glm REQUIRED)
find_package(assimp REQUIRED)
find_package(spdlog REQUIRED)
find_package(VulkanHeaders REQUIRED)
find_package(svulkan2 REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenImageDenoise REQUIRED)

find_package(PkgConfig REQUIRED)

pkg_check_modules(CUDART REQUIRED cudart)
include_directories(${CUDART_INCLUDE_DIRS})
link_directories(${CUDART_LIBRARY_DIRS})

set(PHYSX_VERSION 105.1-physx-5.3.1.patch0)
add_library(physx5 INTERFACE)
target_link_directories(physx5 INTERFACE NIX_PATH_TO_PHYSX5/bin/linux.clang/release>)
target_link_libraries(physx5 INTERFACE
-Wl,--start-group
libPhysXCharacterKinematic_static_64.a libPhysXCommon_static_64.a
libPhysXCooking_static_64.a libPhysXExtensions_static_64.a
libPhysXFoundation_static_64.a libPhysXPvdSDK_static_64.a
libPhysX_static_64.a libPhysXVehicle_static_64.a
-Wl,--end-group)
target_include_directories(physx5 SYSTEM INTERFACE NIX_PATH_TO_PHYSX5/include>)
target_compile_definitions(physx5 INTERFACE PX_PHYSX_STATIC_LIB)
target_compile_definitions(physx5 INTERFACE PHYSX_VERSION="${PHYSX_VERSION}")

if (${SAPIEN_DEBUG_VIEWER})
    add_definitions(_DEBUG_VIEWER)
endif ()

if (${SAPIEN_PROFILE})
    set(SVULKAN2_PROFILE ON CACHE BOOL "" FORCE)
else ()
    set(SVULKAN2_PROFILE OFF CACHE BOOL "" FORCE)
endif ()

if (${SAPIEN_CUDA})
    set(CUDA_TOOLKIT_ROOT_DIR $ENV{CUDA_PATH})
    set(CMAKE_CUDA_STANDARD 17)
    set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -O3 -lineinfo -ftemplate-depth=1024")
    file(GLOB_RECURSE SAPIEN_CUDA_SRC "src/*.cu")

    find_package(CUDA REQUIRED)
    set(SVULKAN2_CUDA_INTEROP ON CACHE BOOL "" FORCE)
else()
    set(SVULKAN2_CUDA_INTEROP OFF CACHE BOOL "" FORCE)
endif()

if (${SAPIEN_CUDA})
    add_subdirectory("3rd_party/simsense")
    set_target_properties(simsense PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/lib")
    target_compile_definitions(simsense PUBLIC SAPIEN_SIMSENSE)
    target_include_directories(simsense PRIVATE "3rd_party/dlpack/include" "$ENV{CUDA_PATH}/include")
endif ()

file(GLOB_RECURSE SAPIEN_SRC "src/*.h" "src/*.cpp" "src/*.cc")
add_library(sapien SHARED ${SAPIEN_SRC} ${SAPIEN_CUDA_SRC})
if (${SAPIEN_CUDA})
    set_target_properties(sapien PROPERTIES CUDA_ARCHITECTURES "60;61;70;75;80;86")

    if (MSVC)
        target_link_libraries(svulkan2 PRIVATE "$ENV{CUDA_PATH}/lib/x64/cudart_static.lib")
    endif()
    target_include_directories(sapien PRIVATE "3rd_party/dlpack/include" "$ENV{CUDA_PATH}/include")
endif ()

target_link_libraries(sapien PUBLIC Eigen3::Eigen svulkan2::svulkan2)
target_link_libraries(sapien PRIVATE physx5 spdlog::spdlog ${CMAKE_DL_LIBS} assimp::assimp)

if (UNIX)
    target_link_libraries(sapien PRIVATE stdc++fs)
endif ()

if (${SAPIEN_CUDA})
    target_compile_definitions(sapien PUBLIC SAPIEN_CUDA SAPIEN_CUDA SVULKAN2_CUDA_INTEROP)
    target_include_directories(sapien PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/3rd_party/dlpack/include>)
endif()

target_include_directories(sapien PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
target_include_directories(sapien PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

set_target_properties(sapien PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
set_target_properties(sapien PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/lib")

if (${SAPIEN_PROFILE})
    target_compile_definitions(sapien PUBLIC SAPIEN_PROFILE)
else ()
    target_compile_definitions(sapien PUBLIC NVTX_DISABLE=1)
endif()

target_include_directories(sapien INTERFACE
    $<INSTALL_INTERFACE:include>
    $<INSTALL_INTERFACE:include/physx/include>
)

if (${SAPIEN_CUDA})
    add_dependencies(sapien OpenImageDenoise)
    # ExternalProject_Get_property(OpenImageDenoise_device_cuda binary_dir)

    message(---- ${binary_dir}/../preinstall/lib)
    install(DIRECTORY ${binary_dir}/../preinstall/lib DESTINATION "." OPTIONAL)
    install(DIRECTORY ${binary_dir}/../preinstall/lib64 DESTINATION "." OPTIONAL)

    install(
        TARGETS sapien simsense physx5
        EXPORT sapienTargets
    )
else()
    install(
        TARGETS sapien
        EXPORT sapienTargets
    )
endif()

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/sapien" DESTINATION "include")
install(DIRECTORY "NIX_PATH_TO_PHYSX5/include" DESTINATION "include/physx")
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/3rd_party/dlpack/include/dlpack" DESTINATION "include")

if (${SAPIEN_CUDA})
    install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/3rd_party/simsense/include/simsense" DESTINATION "include")
endif()

include(CMakePackageConfigHelpers)
configure_package_config_file(
    cmake/sapienConfig.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/sapienConfig.cmake"
    INSTALL_DESTINATION "lib/cmake/sapien"
)
install(
    EXPORT sapienTargets
    FILE sapienTargets.cmake
    DESTINATION "lib/cmake/sapien"
    NAMESPACE sapien::
)
install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/sapienConfig.cmake"
    DESTINATION "lib/cmake/sapien"
)

if (SAPIEN_BUILD_PYTHON)
    find_package(pybind11 REQUIRED)
    file(GLOB_RECURSE PYBIND_SRC "python/pybind/*.cpp")
    pybind11_add_module(pysapien ${PYBIND_SRC} NO_EXTRAS)
    target_link_libraries(pysapien PRIVATE sapien Eigen3::Eigen physx5 Vulkan::Headers glm::glm svulkan2::svulkan2)
    if (TARGET simsense)
        target_link_libraries(pysapien PRIVATE simsense)
    endif()
    target_compile_definitions(pysapien PRIVATE PYBIND11_USE_SMART_HOLDER_AS_DEFAULT)
endif()

if (${SAPIEN_BUILD_TEST})
    include(googletest)
    file(GLOB_RECURSE SAPIEN_TEST_SRC "test/*.cpp")
    add_executable(sapien_test EXCLUDE_FROM_ALL ${SAPIEN_TEST_SRC})
    target_link_libraries(sapien_test sapien GTest::gtest_main physx5
        # -fsanitize=address
    )
    target_include_directories(sapien_test PRIVATE "test")

    add_executable(manual_test EXCLUDE_FROM_ALL "manualtest/main.cpp")
    target_link_libraries(manual_test sapien physx5)
endif()
