#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Porter2::Porter2" for configuration "Release"
set_property(TARGET Porter2::Porter2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Porter2::Porter2 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libPorter2.a"
  )

list(APPEND _cmake_import_check_targets Porter2::Porter2 )
list(APPEND _cmake_import_check_files_for_Porter2::Porter2 "${_IMPORT_PREFIX}/lib/libPorter2.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
