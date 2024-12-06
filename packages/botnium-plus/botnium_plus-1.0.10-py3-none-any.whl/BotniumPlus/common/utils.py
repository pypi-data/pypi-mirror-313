import os, sys
from platform import python_version

class Utils:

    PythonVersion = python_version()

    @staticmethod
    def get_libfolder():
        src_path = os.path.realpath(__file__).split('common')[0]
        lib_path = os.path.join(src_path, "lib")
        return lib_path

  
    @staticmethod
    def get_import_dlls(dir_path):
        files = os.listdir(dir_path)
        import_files = []
        for file in files:
            if file and file.endswith(".dll"):
                import_files.append(file)
        return import_files
