cmake_minimum_required(VERSION 3.10)

project(callback_example LANGUAGES C)

# Specify the C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED True)

# Add the library target
add_library(quote_module SHARED quote_module/pcap_file_offline_reader.c quote_module/quote_parser.c quote_module/utils.c )
target_compile_options(quote_module PRIVATE -ggdb -O6 -Wall -Wno-unused-variable -Wno-unused-but-set-variable)

find_package(PkgConfig REQUIRED)
pkg_search_module(PCAP REQUIRED libpcap jansson event)
# Link pthread library
find_package(Threads REQUIRED)
target_link_libraries(quote_module PRIVATE Threads::Threads ${PCAP_LIBRARIES} jansson event)

# Specify output directory
set_target_properties(quote_module PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/quote_module
)
