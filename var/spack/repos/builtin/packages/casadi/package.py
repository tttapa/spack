# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Casadi(CMakePackage):
    """CasADi is a symbolic framework for numeric optimization implementing
    automatic differentiation in forward and reverse modes on sparse
    matrix-valued computational graphs. It supports self-contained C-code
    generation and interfaces state-of-the-art codes such as SUNDIALS, IPOPT
    etc. It can be used from C++, Python or Matlab/Octave."""

    homepage = "https://web.casadi.org/"
    url = "https://github.com/casadi/casadi/archive/refs/tags/3.6.5.zip"
    git = "https://github.com/casadi/casadi.git"

    license("LGPL-3.0-or-later")

    version("main", branch="main", submodules=True)
    version("3.6.5", sha256="50b7ab41007bfdc099150d6d301e65504bdd6eb16f1d65ad36a0eaa516b8f5ab")
    version("3.6.4", sha256="c80407ba4325fe643a1f468d9c53bbb347e5684f5d53fc4a9ab842bca9cb743b")

    variant("shared", default=True)
    variant("static", default=False)

    generator("ninja")
    depends_on("cmake@3.10.2:", type="build")
    depends_on("ninja", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SHARED", "shared"),
            self.define_from_variant("ENABLE_STATIC", "static"),
        ]
        return args
