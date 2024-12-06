#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dspsim::dspsim-core" for configuration "Release"
set_property(TARGET dspsim::dspsim-core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dspsim::dspsim-core PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/dspsim/lib64/libdspsim-core.so"
  IMPORTED_SONAME_RELEASE "libdspsim-core.so"
  )

list(APPEND _cmake_import_check_targets dspsim::dspsim-core )
list(APPEND _cmake_import_check_files_for_dspsim::dspsim-core "${_IMPORT_PREFIX}/dspsim/lib64/libdspsim-core.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
