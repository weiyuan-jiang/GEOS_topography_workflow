#--------------------
# Copy include files that are used by other libraries.
# We could leave these in the source directory, and just broaden the search path
# in the other libaries, but this make it explicit which aspects are externally
# used.

ecbuild_add_executable (TARGET generate_scrip_cube.x SOURCES generate_scrip_cube.F90 geompack.F90)
target_link_libraries (generate_scrip_cube.x PRIVATE MPI::MPI_Fortran esmf)
# CMake has an OpenMP issue with NAG Fortran: https://gitlab.kitware.com/cmake/cmake/-/issues/21280
if (NOT CMAKE_Fortran_COMPILER_ID MATCHES "NAG")
  target_link_libraries(generate_scrip_cube.x PRIVATE OpenMP::OpenMP_Fortran)
endif ()

ecbuild_add_executable (TARGET convert_bin_to_netcdf.x SOURCES convert_bin_to_netcdf.F90)
target_link_libraries (convert_bin_to_netcdf.x PRIVATE MPI::MPI_Fortran NetCDF::NetCDF_Fortran)
# CMake has an OpenMP issue with NAG Fortran: https://gitlab.kitware.com/cmake/cmake/-/issues/21280
if (NOT CMAKE_Fortran_COMPILER_ID MATCHES "NAG")
  target_link_libraries(convert_bin_to_netcdf.x PRIVATE OpenMP::OpenMP_Fortran)
endif ()

ecbuild_add_executable (TARGET convert_to_gmao_output.x SOURCES convert_to_gmao_output.F90)
target_link_libraries (convert_to_gmao_output.x PRIVATE MPI::MPI_Fortran NetCDF::NetCDF_Fortran)
# CMake has an OpenMP issue with NAG Fortran: https://gitlab.kitware.com/cmake/cmake/-/issues/21280
if (NOT CMAKE_Fortran_COMPILER_ID MATCHES "NAG")
  target_link_libraries(convert_to_gmao_output.x PRIVATE OpenMP::OpenMP_Fortran)
endif ()

install(PROGRAMS scrip_to_cube.py DESTINATION bin)
install(PROGRAMS scrip_to_restart.py DESTINATION bin)
install(PROGRAMS generate_topo.sh DESTINATION bin)
