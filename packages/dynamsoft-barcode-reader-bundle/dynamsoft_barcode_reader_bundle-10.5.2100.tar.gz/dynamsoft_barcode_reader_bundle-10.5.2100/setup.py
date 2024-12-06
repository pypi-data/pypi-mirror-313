from setuptools.command import build_ext
from setuptools import setup, Extension
import sys
import os
import io
from setuptools.command.install import install
import platform
import shutil
from pathlib import Path

lib_dir = ''
core_lib_name = 'DynamsoftCore'
cvr_lib_name = 'DynamsoftCaptureVisionRouter'
dbr_lib_name = 'DynamsoftBarcodeReader'
dip_lib_name = 'DynamsoftImageProcessing'
license_lib_name = 'DynamsoftLicense'
utility_lib_name = 'DynamsoftUtility'
resource_dir = 'resource'
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        if platform.uname()[4] == 'AMD64' or platform.uname()[4] == 'x86_64':
                lib_dir = 'lib/linux/x64'
        elif platform.uname()[4] == 'aarch64':
                lib_dir = 'lib/linux/arm64'
        else:
                lib_dir = 'lib/linux/arm32'
elif sys.platform == "darwin":
    # OS X
    if sys.version_info < (3, 8):
        lib_dir = 'lib/mac/x64'
    elif sys.version_info >= (3, 8):
        lib_dir = 'lib/mac/universal2'

elif sys.platform == "win32":
    # Windows
    core_lib_name = 'DynamsoftCorex64'
    cvr_lib_name = 'DynamsoftCaptureVisionRouterx64'
    dbr_lib_name = 'DynamsoftBarcodeReaderx64'
    dip_lib_name = 'DynamsoftImageProcessingx64'
    license_lib_name = 'DynamsoftLicensex64'
    utility_lib_name = 'DynamsoftUtilityx64'
    lib_dir = 'lib/win'

if sys.platform == "linux" or sys.platform == "linux2":
    ext_args = dict(
        library_dirs = [lib_dir],
        extra_compile_args = ['-std=c++11','-DBUILD_BUNDLE=1'],
        extra_link_args = ["-Wl,-rpath=$ORIGIN"],
        include_dirs=['include']
    )
elif sys.platform == "darwin":
    ext_args = dict(
        library_dirs = [lib_dir],
        extra_compile_args = ['-std=c++11','-DBUILD_BUNDLE=1'],
        extra_link_args = ["-Wl,-rpath,@loader_path"],
        include_dirs=['include']
    )

long_description = io.open("README.rst", encoding="utf-8").read()

if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    module_core = Extension('_DynamsoftCore', ['src/DynamsoftCore_wrap.cxx'],libraries = [core_lib_name, dip_lib_name], **ext_args)
    module_cvr = Extension('_DynamsoftCaptureVisionRouter', ['src/DynamsoftCaptureVisionRouter_wrap.cxx'], libraries = [cvr_lib_name,core_lib_name], **ext_args)
    module_dbr = Extension('_DynamsoftBarcodeReader', ['src/DynamsoftBarcodeReader_wrap.cxx'], libraries = [dbr_lib_name,core_lib_name], **ext_args)
    module_dip = Extension('_DynamsoftImageProcessing', ['src/DynamsoftImageProcessing_wrap.cxx'], libraries = [dip_lib_name], **ext_args)
    module_license = Extension('_DynamsoftLicense', ['src/DynamsoftLicense_wrap.cxx'], libraries = [license_lib_name,core_lib_name], **ext_args)
    module_utility = Extension('_DynamsoftUtility', ['src/DynamsoftUtility_wrap.cxx'], libraries = [utility_lib_name,core_lib_name], **ext_args)

else:      
	module_core = Extension('_DynamsoftCore', sources=['src/DynamsoftCore_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[core_lib_name, dip_lib_name])
	module_cvr = Extension('_DynamsoftCaptureVisionRouter', sources=['src/DynamsoftCaptureVisionRouter_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[cvr_lib_name,core_lib_name])
	module_dbr = Extension('_DynamsoftBarcodeReader', sources=['src/DynamsoftBarcodeReader_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[dbr_lib_name,core_lib_name])
	module_dip = Extension('_DynamsoftImageProcessing', sources=['src/DynamsoftImageProcessing_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[dip_lib_name])
	module_license = Extension('_DynamsoftLicense', sources=['src/DynamsoftLicense_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[license_lib_name,core_lib_name],extra_compile_args=['-DBUILD_BUNDLE=1'])
	module_utility = Extension('_DynamsoftUtility', sources=['src/DynamsoftUtility_wrap.cxx'], include_dirs=['include'], library_dirs=[lib_dir],libraries=[utility_lib_name,core_lib_name])
    
def copylibs(src, dst):
        if os.path.isdir(src):
                filelist = os.listdir(src)
                for file in filelist:
                        libpath = os.path.join(src, file)
                        shutil.copy2(libpath, dst)
        else:
                shutil.copy2(src, dst)
def copy_directory(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)
    
    for item in src_path.iterdir():
        target = dst_path / item.name
        if item.is_dir():
            copy_directory(item, target)
        else:
            shutil.copy2(item, target)
class CustomBuildExt(build_ext.build_ext):
        def run(self):
                build_ext.build_ext.run(self)
                dst =  os.path.join(self.build_lib, "dynamsoft_barcode_reader_bundle")
                copylibs(lib_dir, dst)
                copy_directory(resource_dir, dst)
                filelist = os.listdir(self.build_lib)
                for file in filelist:
                    filePath = os.path.join(self.build_lib, file)
                    if not os.path.isdir(file):
                        copylibs(filePath, dst)
                        # delete file for wheel package
                        os.remove(filePath)

class CustomBuildExtDev(build_ext.build_ext):
        def run(self):
                build_ext.build_ext.run(self)
                dev_folder = os.path.join(Path(__file__).parent, 'dynamsoft_barcode_reader_bundle')
                copylibs(lib_dir, dev_folder)
                copy_directory(resource_dir, dev_folder)
                filelist = os.listdir(self.build_lib)
                for file in filelist:
                    filePath = os.path.join(self.build_lib, file)
                    if not os.path.isdir(file):
                        copylibs(filePath, dev_folder)

class CustomInstall(install):
    def run(self):
        install.run(self)

setup (name = 'dynamsoft_barcode_reader_bundle',
            version = '10.5.2100',
            description = 'Dynamsoft Barcode Reader SDK for Python',
            long_description=long_description,
            long_description_content_type="text/x-rst",
            author='Dynamsoft',
            url='https://www.dynamsoft.com/barcode-reader/overview/?utm_source=pypi',
            packages=['dynamsoft_barcode_reader_bundle'],
        ext_modules = [module_core,module_cvr,module_dbr,module_dip,module_license,module_utility],
        # options={'build':{'build_lib':'./dbr'}},
        classifiers=[
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "Intended Audience :: Education",
                "Intended Audience :: Information Technology",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: MIT License",
                "Operating System :: Microsoft :: Windows",
                "Operating System :: MacOS",
                "Operating System :: POSIX :: Linux",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3 :: Only",             
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
                "Programming Language :: Python :: 3.12",
                "Programming Language :: Python :: 3.13",
                "Programming Language :: C++",
                "Programming Language :: Python :: Implementation :: CPython",
                "Topic :: Scientific/Engineering",
                "Topic :: Software Development",
            ],
            cmdclass={
                    'install': CustomInstall,
                    'build_ext': CustomBuildExt,
                    'develop': CustomBuildExtDev},
        )
