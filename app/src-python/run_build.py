"""
Using PyInstaller packager to build executable of the Twin Model Explorer.
"""

import os
import platform
import shutil
import sys
from subprocess import Popen

try:
    import PyInstaller
except ImportError:
    PyInstaller = None
    raise SystemExit("Error: PyInstaller package missing. "
                     "To install type: pip install --upgrade pyinstaller")

EXEC_NAME = 'FBapp_backend'
BUILD_SPEC_FILE = "build.spec"
DIST_FOLDER = 'dist'

EXE_EXT = ""
if platform.system() == "Windows":
    EXE_EXT = ".exe"
    # DIST_FOLDER += '_win'
elif platform.system() == "Darwin":
    EXE_EXT = ".app"
    # DIST_FOLDER += '_mac'
elif platform.system() == "Linux":
    EXE_EXT = ""
    # DIST_FOLDER += '_linux'

DIST_FOLDER = DIST_FOLDER.rstrip('/') + '/'


def main():
    # Platforms supported
    if platform.system() not in ["Windows", "Darwin", "Linux"]:
        raise SystemExit("Error: Only Windows, Linux and Darwin platforms are "
                         "currently supported. See Issue #135 for details.")

    # Make sure nothing is cached from previous build.
    # Delete the build/ and dist/ directories.
    if os.path.exists("build/"):
        # ignore_errors=True for deleting the Read-only file
        shutil.rmtree("build/", ignore_errors=True)
    if os.path.exists(DIST_FOLDER):
        shutil.rmtree(DIST_FOLDER, ignore_errors=True)

    # Execute pyinstaller.
    # Note: the "--clean" flag passed to PyInstaller will delete
    #       global global cache and temporary files from previous
    #       runs. For example on Windows this will delete the
    #       "%appdata%/roaming/pyinstaller/bincache00_py27_32bit"
    #       directory.
    env = os.environ
    if "--debug" in sys.argv:
        env["CEFPYTHON_PYINSTALLER_DEBUG"] = "1"
    sub = Popen(["pyinstaller", "--clean", BUILD_SPEC_FILE], env=env)
    sub.communicate()
    rcode = sub.returncode
    if rcode != 0:
        print("Error: PyInstaller failed, code=%s" % rcode)
        # Delete distribution directory if created
        if os.path.exists(DIST_FOLDER):
            shutil.rmtree(DIST_FOLDER)
        sys.exit(1)

    # Make sure everything went fine
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(curr_dir, DIST_FOLDER, EXEC_NAME)
    executable = os.path.join(dist_dir, EXEC_NAME+EXE_EXT)
    if not os.path.exists(executable):
        print("Error: PyInstaller failed, main executable is missing: %s"
              % executable)
        sys.exit(1)

    # Done
    print("OK. Created {} directory.".format(DIST_FOLDER))

    # On Windows open folder in explorer or when --debug is passed
    # run the result binary using "cmd.exe /k cefapp.exe", so that
    # console window doesn't close.
    if platform.system() == "Windows":
        if "--debug" in sys.argv:
            os.system("start cmd /k \"%s\"" % executable)
        else:
            # SYSTEMROOT = C:/Windows
            os.system("%s/explorer.exe /n,/e,%s" % (
                os.environ["SYSTEMROOT"], dist_dir))


if __name__ == "__main__":
    main()
