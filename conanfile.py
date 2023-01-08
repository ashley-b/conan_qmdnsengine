from conan import ConanFile, Version
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.files.patches import apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, get, rmdir
import os

required_conan_version = ">=1.52.0"

class QMdnsEnginConan(ConanFile):
    name = "qmdnsengine"
    description = "This library provides an implementation of multicast DNS as per RFC 6762."
    url = "https://github.com/ashley-b/conan_qmdnsengine"
    homepage = "https://github.com/nitroshare/qmdnsengine"
    topics = ("mdns", "qt")
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    @property
    def _minimum_cpp_standard(self):
        return 11

    @property
    def _minimum_qt_version(self):
        return "5.7.0"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def export_sources(self):
        export_conandata_patches(self)

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._minimum_cpp_standard)

        qt_version = Version(self.dependencies["qt"].ref.version)
        if qt_version < Version(self._minimum_qt_version):
            raise ConanInvalidConfiguration("{} requires qt version > {}".format(self.ref, self._minimum_qt_version))

        if qt_version.major == 6 and self.version < "0.2.0-2022-01-15":
            raise ConanInvalidConfiguration("{} requires qt 5".format(self.ref))

    def requirements(self):
        self.requires("qt/5.15.5")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
                  destination=self.source_folder, strip_root=True)

    def generate(self):
        apply_conandata_patches(self)
        tc = CMakeToolchain(self)
        # Honor BUILD_SHARED_LIBS from conan_toolchain (see https://github.com/conan-io/conan/issues/11840)
        tc.cache_variables["CMAKE_POLICY_DEFAULT_CMP0077"] = "NEW"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["qmdnsengine"]
        self.cpp_info.requires = ["qt::qtCore","qt::qtNetwork"]
