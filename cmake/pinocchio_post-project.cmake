# Restore version information that might have been overriden by project() call
SET(PROJECT_VERSION "${SAVED_PROJECT_VERSION}")
SET(PROJECT_VERSION_MAJOR "${SAVED_PROJECT_VERSION_MAJOR}")
SET(PROJECT_VERSION_MINOR "${SAVED_PROJECT_VERSION_MINOR}")
SET(PROJECT_VERSION_PATCH "${SAVED_PROJECT_VERSION_PATCH}")

INCLUDE(${CMAKE_CURRENT_LIST_DIR}/GNUInstallDirs.cmake)
SET(CMAKE_INSTALL_FULL_PKGLIBDIR ${CMAKE_INSTALL_FULL_LIBDIR}/${PROJECT_NAME})
SET(CMAKE_INSTALL_PKGLIBDIR ${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME})

INCLUDE(${CMAKE_CURRENT_LIST_DIR}/pkg-config.cmake)
IF(DEFINED PROJECT_DEBUG_POSTFIX)
  SET(CMAKE_DEBUG_POSTFIX ${PROJECT_DEBUG_POSTFIX})
  STRING(TOLOWER "${CMAKE_BUILD_TYPE}" cmake_build_type)
  IF(${cmake_build_type} MATCHES debug)
    SET(PKGCONFIG_POSTFIX ${PROJECT_DEBUG_POSTFIX})
  ELSE()
    SET(PKGCONFIG_POSTFIX "")
  ENDIF()
  IF(DEFINED CMAKE_CONFIGURATION_TYPES)
    SET(PKGCONFIG_POSTFIX ${PROJECT_DEBUG_POSTFIX})
  ENDIF()
ENDIF()

IF(NOT DEFINED PROJECT_USE_KEYWORD_LINK_LIBRARIES)
  SET(PROJECT_USE_KEYWORD_LINK_LIBRARIES FALSE)
ENDIF()
IF(PROJECT_USE_KEYWORD_LINK_LIBRARIES)
  SET(PUBLIC_KEYWORD PUBLIC)
ELSE()
  SET(PUBLIC_KEYWORD "")
ENDIF()

IF(${ARGC})
  SET(CMAKE_VERBOSE_MAKEFILE ${ARGV0})
ELSE(${ARGC})
  # Be verbose by default.
  SET(CMAKE_VERBOSE_MAKEFILE TRUE)
ENDIF(${ARGC})

OPTION(INSTALL_DOCUMENTATION "Generate and install the documentation" ON)
OPTION(INSTALL_GENERATED_HEADERS "Generate and install standard headers" ON)
OPTION(INSTALL_PKG_CONFIG_FILE "Generate and install standard .pc file" ON)

INCLUDE(CTest)
ENABLE_TESTING()

LOGGING_INITIALIZE()

#FIXME: normalize naming to <MODULE>_SETUP()
_SETUP_PROJECT_WARNINGS()
_SETUP_PROJECT_HEADER()
_SETUP_PROJECT_DIST()
DISTCHECK_SETUP()
RELEASE_SETUP()
_SETUP_PROJECT_DEB()
# _SETUP_PROJECT_UNINSTALL()
_SETUP_PROJECT_PKG_CONFIG()
_SETUP_PROJECT_DOCUMENTATION()
_SETUP_PROJECT_PACKAGE_INIT()
