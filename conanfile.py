import os
from conans import CMake, ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.tools import Version

required_conan_version = ">=1.43.0"

class QMdnsEnginConan(ConanFile):
    name = "qmdnsengine"
    description = "This library provides an implementation of multicast DNS as per RFC 6762."
    url = "https://github.com/ashley-b/conan_qmdnsengine"
    homepage = "https://github.com/nitroshare/qmdnsengine"
    topics = ("mdns", "Qt")
    license = "MIT"
    generators = "cmake", "cmake_find_package", "cmake_find_package_multi"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination="qmdnsengine", strip_root=True)

    def _cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder="qmdnsengine")
        return cmake;

    def build(self):
        cmake = self._cmake()
        cmake.build()
#        cmake.test()

    def package(self):
        cmake = self._cmake()
        cmake.install()

    def test(self):
        cmake = self._cmake()
        cmake.build()
        cmake.test()

    def package_info(self):
        self.cpp_info.libs = ["qmdnsengine"]
