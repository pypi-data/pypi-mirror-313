#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tevclient::tevclient" for configuration "Release"
set_property(TARGET tevclient::tevclient APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(tevclient::tevclient PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/sgl/tevclient.lib"
  )

list(APPEND _cmake_import_check_targets tevclient::tevclient )
list(APPEND _cmake_import_check_files_for_tevclient::tevclient "${_IMPORT_PREFIX}/sgl/tevclient.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
