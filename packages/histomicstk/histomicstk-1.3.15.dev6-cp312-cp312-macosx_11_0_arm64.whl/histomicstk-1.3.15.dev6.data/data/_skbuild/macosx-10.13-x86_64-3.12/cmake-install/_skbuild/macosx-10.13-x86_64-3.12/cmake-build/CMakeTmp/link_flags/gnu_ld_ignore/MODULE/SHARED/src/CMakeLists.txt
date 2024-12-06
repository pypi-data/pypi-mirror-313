
      cmake_minimum_required(VERSION 3.31.1)
      project(link_flags C)

      include_directories(/Users/runner/work/HistomicsTK/HistomicsTK/_skbuild/macosx-10.13-x86_64-3.12/cmake-build/CMakeTmp/link_flags/gnu_ld_ignore/MODULE/SHARED/src)

      add_library(number SHARED number.c)
      add_library(counter MODULE counter.c)
    
        set_target_properties(counter PROPERTIES PREFIX "")
      
        set_target_properties(counter PROPERTIES LINK_FLAGS "-Wl,--unresolved-symbols=ignore-all")
      
      add_executable(main main.c)
    
        target_link_libraries(main  number)
      
        target_link_libraries(main  "")
      