# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Alpaqa(CMakePackage):
    """Augmented Lagrangian and PANOC solvers for nonconvex numerical optimization"""

    homepage = "https://github.com/kul-optec/alpaqa"
    url = "https://github.com/kul-optec/alpaqa/archive/refs/tags/1.0.0a17.zip"
    git = "https://github.com/kul-optec/alpaqa.git"

    maintainers("tttapa")
    license("LGPL-3.0-or-later")

    version("develop", branch="develop")
    version("1.0.0a17", sha256="ebaf36f5b5325c71708d8192c6405da783b3735ec4f5f8b624dd0cd343c22555")
    version("1.0.0a16", sha256="89938f6c2e3f56d7852fd596746693e986f9d740100ec1a941703ae2d16ccaa8")
    version("1.0.0a15", sha256="f5ddda7f72336ce6b3055375eda9c1ec4ada2a8ce92be5db64ddd03422523640")
    version("1.0.0a14", sha256="b5101afad6c6b7d3747c8149e5d7ff7c679e7c86a239ccea65d8408a5e9c9528")
    version("1.0.0a13", sha256="53b0cb700659659f99001efc9e78d6c009b0f353e6e1e8eb35c8b644bcdf35f7")
    version("1.0.0a12", sha256="cdb3eb70121c3f03bb7800ba0744b3fa154e2af543ca8331ef3b87304efa79ac")
    version("1.0.0a11", sha256="03daf95b34331dab1f745fb9fd3d670b840fd47891b64652dbcd3aebed7191e3")
    version("1.0.0a10", sha256="27e18d5bb846595d96b5548dea3a471e28442c2cca07ca27d758a10f13d9cbf8")
    version("1.0.0a9", sha256="69c98752b319f6158c2ee667e80d0e4fda4dfa445074f7e45fd92ff655f17e7a")
    version("1.0.0a8", sha256="524855a8103be3d66f96797beb8caa6bc602720223860a925f396669c126e4bc")
    version("1.0.0a7", sha256="7deb7efcf99ca14b5bcd489fd30077b253b12aa7523fa0441d3250af9a94f02d")

    variant("shared", default=True)
    variant("examples", default=False)
    variant("python", default=False)
    variant("matlab", default=False, when="@1.0.0a16:")
    variant("drivers", default=True)
    variant("gradient_checker", default=False, when="@1.0.0a16:")
    variant("casadi", default=False)
    variant("cutest", default=False, when="@1.0.0a16:")
    variant("qpalm", default=False, when="@1.0.0a16:")
    variant("json", default=True, when="@1.0.0a16:")
    variant("lbfgsb", default=False, when="@1.0.0a16:")
    variant("ocp", default=False, when="@1.0.0a16:")
    variant("casadi_ocp", default=False, when="@1.0.0a16:")
    variant("openmp", default=False, when="@1.0.0a16:")
    variant("quad_precision", default=False)
    variant("single_precision", default=False, when="@1.0.0a16:")
    variant("long_double", default=False, when="@1.0.0a16:")
    variant("debug_checks_eigen", default=False, when="@1.0.0a16:")
    variant("dont_parallelize_eigen", default=True, when="@1.0.0a16:")
    variant("no_dlclose", default=False, when="@1.0.0a16:")
    variant("blas", default=False, when="@1.0.0a16:")
    conflicts("-json", when="+matlab")
    conflicts("-casadi", when="+matlab")

    generator("ninja")
    depends_on("cmake@3.24:", type="build")
    depends_on("ninja", type="build")

    depends_on("eigen@3.4.0:")
    depends_on("googletest@1.10.0: +gmock -pthreads", type="test")
    depends_on("casadi@3.6.4:", when="+casadi")
    depends_on("nlohmann-json@3.11.2:", when="+json")
    depends_on("py-pybind11@2.10.1:", when="+python")
    depends_on("utfcpp@2.10.1:", when="+matlab")
    depends_on("blas", when="+blas")

    def cmake_args(self):
        bool_options = [
            "with_python",
            "with_matlab",
            "with_drivers",
            "with_gradient_checker",
            "with_casadi",
            "with_cutest",
            "with_qpalm",
            "with_json",
            "with_lbfgsb",
            "with_ocp",
            "with_casadi_ocp",
            "with_openmp",
            "with_quad_precision",
            "with_single_precision",
            "with_long_double",
            "debug_checks_eigen",
            "dont_parallelize_eigen",
            "no_dlclose",
            "with_blas",
        ]
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        for o in bool_options:
            variant = o.removeprefix("with_")
            define = "ALPAQA_" + o.upper()
            args.append(self.define_from_variant(define, variant))
        if self.spec.satisfies("+blas"):
            args += [
                self.define("BLAS_LIBRARIES", self.spec["blas"].libs.joined(";")),
                self.define("LAPACK_LIBRARIES", self.spec["lapack"].libs.joined(";")),
            ]
            if "^netlib-lapack" in self.spec:
                args += [self.define("BLA_VENDOR", "Generic")]
            elif "^openblas" in self.spec:
                args += [self.define("BLA_VENDOR", "OpenBLAS")]
        return args
