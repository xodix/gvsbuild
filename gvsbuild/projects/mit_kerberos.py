#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Kerberos(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "mit-kerberos",
            archive_url="https://github.com/krb5/krb5/archive/refs/tags/krb5-1.19.3-final.tar.gz",
            hash="131890da54fff2ac339e93facf9d8067f7db53b15181f38104c0b56a6f2acdee",
            dependencies=[
                "perl",
            ],
        )

    def build(self):
        configuration = (
            "Debug" if self.builder.opts.configuration == "debug" else "Release"
        )
        add_path = os.path.join(self.builder.opts.msys_dir, "usr", "bin")

        self.push_location("src")
        self.exec_vs(
            r"nmake -f Makefile.in prep-windows NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ",
            add_path=add_path,
        )
        self.exec_vs(
            r"nmake NODEBUG="
            + str(1 if configuration == "Release" else 0)
            + " NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ",
            add_path=add_path,
        )
        self.exec_vs(
            r"nmake install NODEBUG="
            + str(1 if configuration == "Release" else 0)
            + " NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ",
            add_path=add_path,
        )
        self.pop_location()

        self.install(r".\NOTICE share\doc\mit-kerberos")
