#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "wapopp::wapopp" for configuration "Release"
set_property(TARGET wapopp::wapopp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(wapopp::wapopp PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libwapopp.a"
  )

list(APPEND _cmake_import_check_targets wapopp::wapopp )
list(APPEND _cmake_import_check_files_for_wapopp::wapopp "${_IMPORT_PREFIX}/lib/libwapopp.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
