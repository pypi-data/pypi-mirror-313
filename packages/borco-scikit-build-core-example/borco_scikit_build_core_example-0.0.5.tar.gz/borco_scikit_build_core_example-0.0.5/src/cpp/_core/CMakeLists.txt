set(MODULE_NAME _core)

pybind11_add_module(
    ${MODULE_NAME} MODULE
    main.cpp
)

target_link_libraries(
    ${MODULE_NAME} PRIVATE
    _core_lib
)

install(TARGETS ${MODULE_NAME} LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME})
