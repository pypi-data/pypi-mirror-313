from ast import keyword
from ensurepip import version
from multiprocessing import AuthenticationError
from nturl2path import url2pathname
from random import sample
from ssl import Options

# ------- using numpy's distutils --------
import setuptools # this is not used but needs to be here for everythng else working correctly
from numpy.distutils.core import Extension, setup
# from numpy.distutils.command.build_ext import build_ext as numpy_build_ext



# ------- using setuptools distutils --------
# TODO later for distutils from setuptools instead from numpy
# from setuptools import Extension, setup

# from setuptools.command.build_ext import build_ext as numpy_build_ext
# ------- using setuptools distutils --------

import os

# ----- Below is added for distutils to find MSVC compiler

os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["MSSdk"] = "1"
# ------------------------------------------------------

from pathlib import Path

# set in calling batch script - local.bat
build_type = os.getenv('EMAPS_BTYPE')
DOCKER_BUILD = os.getenv('DOCKER_BUILD')

# set in system's environment settings
LG_PATH = os.getenv("LG_PATH")
EMAPS_FOLDER = os.getenv("EMAPS_FOLDER")

emaps_debug = 0
bLicCheck = False # real full package build - full build but not docker build

if DOCKER_BUILD is not None:
    # when build for docker container, it is always 
    # this is always set inside the Dockefile build file
    build_type = 'full'
else:
    if build_type is None:
        print(f'#################build type is not set, default to free')
        build_type = 'free'
    else:
        print(f'#################build type is set at {build_type}')
        if build_type != 'full' and \
           build_type != 'uiuc' and \
           build_type != 'free':
            
            print(f'#################build type is set incorrectly at {build_type}, set to free')
            build_type = 'free'
        if build_type == 'full' and DOCKER_BUILD is None:
            bLicCheck = True

    if os.getenv('EMAPS_DEBUG') is None:
        emaps_debug = 0
        print(f'#################build is not debug')
    else:
        emaps_debug = int(os.getenv('EMAPS_DEBUG'))
        print(f'#################build debug is set {emaps_debug}')

mod_name = "emaps"

MKLROOT = os.getenv('MKLROOT')
IFORTROOT = os.getenv('IFORTROOT')
# VS2022INSTALLDIR = os.getenv('VS2022INSTALLDIR')

MSVCRUNTIME_VERSION='14.36.32532' #msvc runtime version builing this package

dpgen_cobj = 'write_dpbin.o'

compile_args_debug=['-Qm64',
                    '-Od',
              '-WB',
              '-heap-arrays:1024',
            #   '-Qopenmp',
              '-Qmkl',
            #   '-Qopenmp-simd',
            #   '-GS:partial', 
              '-fpp',
              '-warn:all',
            #   '-O2', #this option does not work with -fast
            #   '-libs:static',
            #   '-MT',
            #   '-assume:buffered_io',
            #   '-traceback',
            #   '-check:all',
            #   '-align:array32byte',
            #   '-Qparallel',
            #   '-Qopt-report:2',
              '-c']
# --------------- production options--------------
compile_args=['-Qm64',
              '-WB',
              '-heap-arrays:1024',
            #   '-Qopenmp',
              '-Qopenmp-',
              '-Qmkl',
              '-GS:partial', 
              '-fpp',
              '-warn:all',
              '-O2', #this option does not work with -fast
            #   '-lib
            # s:static',
            #   '-module:'+os.path.join(MKLROOT, 'include', 'intel64', 'lp64'),
              '-MT',
              '-assume:buffered_io',
              '-NODEFAULTLIB:libcmt',
              '-c']

# --------debugging options-----------
# compile_args=['-Qm64',
#               '-WB',
#               '-heap-arrays:1024',
#               '-check:all',
#               'Qfp-stack-check',
#               '-Qopenmp',
#               '-GS:partial', 
#               '-fpp',
#               '-warn:nointerfaces',
#             #   '-O2', #this option does not work with -fast
#             #   '-libs:static',
#               '-MT',
#               '-assume:buffered_io',
#               '-traceback',
#               '-c']
              
compile_args_lin= ['-m64',
                   '-fpic',
                   '-WB', 
                #    '-qopenmp', 
                   '-qmkl', 
                   '-heap-arrays 1024', 
	            #    '-r8', 
                   '-fpp', 
                #    '-warn nointerfaces',
                    '-warn all',
                   '-O3',
                #    '-MT',
                #    'fp-stack-check',
                   '-c']

# intel_libs = ['mkl_intel_lp64',
#               'mkl_intel_thread',
#               'mkl_core', 
#               'libiomp5md']

# intel_libs = ['mkl_intel_lp64',
#               'mkl_intel_thread',
#               'mkl_core']

c_compile_args = ["-std=c11", "-stack_size 2000000"]

# intel_libs_lin = ['mkl_rt', 
#               'iomp5',
#               'pthread',
#               'm',
#               'dl']

intel_libs_lin = ['iomp5',
                'pthread',
                'm',
                'dl']
# intel_libs_lin = ['mkl_rt',
#                 'iomp5',
#                 'pthread',
#                 'm',
#                 'dl']

lapack_lib = 'mkl_lapack95_lp64'

# intel_static_libs_lin = [
#                 'lib' + lapack_lib+'.a',
#                 'libmkl_intel_lp64.a',
#                 'libmkl_intel_thread.a',
#                 'libmkl_core.a'
#                 ]
intel_static_libs_lin = ['libmkl_intel_lp64.a',
                         'libmkl_intel_thread.a',
                         'libmkl_core.a']
lapack_static_lib = 'lib' + lapack_lib +'.a'

intel_libs_win = [lapack_lib,
                'mkl_intel_lp64',
                'mkl_intel_thread',
                'mkl_core',
                'libiomp5md']

# intel_static_libs_win = [lapack_lib+'.lib',
#                 'mkl_intel_lp64.lib',
#                 'mkl_intel_thread.lib',
#                 'mkl_core.lib',
#                 'libiomp5md.lib']
install_requires_common = [
            # 'numpy >= 1.21.2',
            # 'matplotlib >= 3.2.1',
            ]

dif_source = [
            'diff_types.f90', 
            'diff_memalloc.f90',
            'diffract.f90',
            'scattering.f90', 
            'spgra.f90',
            'crystal_mem.f90', 
            'emaps_consts.f90',
            'xtal0.f90', 
            'helper.f90', 
            'asf.f90', 
            'atom.f',
            'metric.f', 
            'readutils.f',
            'sfsub.f90', 
            'spgroup.f90', 
            'lafit.f90'
            ]

bloch_files = ['zg.f90',
               'cbloch.f90',
               'bloch_mem.f90',
               'bloch.f90'
              ]
stereo_files = ['stereo.f90']

mxtal_files = ['mxtal_mem.f90',
               'mxtal.f90']

dpgen_files =['cdpgen.f90',
              'dp_types.f90',
			  'dp_gen.f90'
             ]

csf_files =['csf_types.f90',
			  'csf.f90'
            ]

powder_files =['powder_types.f90',
			  'powder.f90',
              'pkprof.f90'
              ]

spgra_files =['spgra.f90']

c_objs_free_win = ['blochimgs.obj']
c_objs_free_lin = ['blochimgs.o']


sct_files =['scattering_sct.pyf', 'scattering.f90']  

spgra_files =['spg_spgseek.pyf', 'spgseek.f90', 'spgra.f90']    

# ------------- stem4d -----------------
stem4dSRCFiles = ['imgutil_sub.cpp', 
            'DPIndex.cpp', 
            'nrutil.cpp', 
            'refine.cpp',
            'peak.cpp',
            'StackDP.cpp', 
            'simplxc.cpp',
            'symmetry.cpp',
            'stem4d.i']

# ------------- stem4d license checking files -----------------
stem4dLicFiles = ['EMAPSLicConfig.cpp', 
            'EMAPSLicense.cpp', 
            'EMAPSLicenseBase.cpp', 
            'EMAPSLicFileStorage.cpp',
            'KeyBasedEMAPSLicense.cpp']

if bLicCheck:
    stem4dSRCFiles.append('lic_check.cpp')
# ------------- stem4d -----------------   

def isWindowsOS():
    import platform, os

    osname = platform.platform().lower()
    if osname is None or 'windows' not in osname:
        return False
    return True

def isLinuxOS():
    import platform, os

    osname = platform.platform().lower()
    if osname is None or 'linux' not in osname:
        return False
    return True

def isUnsupportedOS():
    return not isWindowsOS() and not isLinuxOS()

# def get_emaps_location():
#     current_file_path = ""
#     try:
#         current_working_dir = os.getcwd()
#         print(f'get the current working directory: {current_working_dir}')
#         current_file_path = os.path.abspath(current_working_dir)
#     except Exception as e:
#         current_file_path = os.path.abspath(__file__)
#         print(f'Failed in extract setup.py file path {e} and {current_file_path}')
#     else:
#         print(f'$$$$$$$$$current file path: {current_file_path} for {__file__}')

#     emaps_folder = os.path.dirname(current_file_path)
#     return emaps_folder

def get_stem4d_srcdir():
    # emaps_loc = get_emaps_location()
    print(f'------emaps folder: {EMAPS_FOLDER}')
    return os.path.join(EMAPS_FOLDER, 'stem4d')


def get_license_srcdir():
    # emaps_loc = get_emaps_location()
    return os.path.join(EMAPS_FOLDER, 'license')

def get_stem4d_sources():

    stem4d_dir = get_stem4d_srcdir()
    # print(f'original stem4d source file list: {stem4dSRCFiles}')
    print(f'stem4d source dir: {stem4d_dir}')
    src_list = []
    for sf in stem4dSRCFiles:
        src_list.append(os.path.join(stem4d_dir, sf))

    # ----- adding license features -----
    for sf in stem4dLicFiles:
        src_list.append(os.path.join(os.path.dirname(stem4d_dir), 'license', sf))
        
    # for dsf in src_list:
    #     print(f'stem4d source file list: {dsf}')
    print(f'stem4d source file list: {src_list}')
    # exit()
    return src_list   

def get_license_sources():

    lic_dir = get_license_srcdir()
    print(f'license source directory: {lic_dir}')
    src_list = []
    for sf in stem4dLicFiles:
        src_list.append(os.path.join(lic_dir, sf))

    src_list.append(os.path.join(lic_dir, 'license.i'))
        
    for dsf in src_list:
        print(f'stem4d source file list: {dsf}')
    exit()
    return src_list   
   
def get_stem4d_includes():
    #  for ccompiler cl arguement too long issue
    # see https://github.com/pypa/setuptools/pull/3775/commits/dd03b731045d5bb0b47648554f9a1a7429ef306a
    # temporary fix
    import numpy as np
    from sysconfig import get_paths
    
    includeDirs=[np.get_include()]
    # python's include
    includeDirs.append(get_paths()['include'])
    includeDirs.append(get_stem4d_srcdir())

    if bLicCheck:
        includeDirs.append(os.path.join(LG_PATH, "include"))

    print(f'include dirs with license: {includeDirs}')
    return includeDirs 
   
def get_license_includes():
    #  for ccompiler cl arguement too long issue
    # see https://github.com/pypa/setuptools/pull/3775/commits/dd03b731045d5bb0b47648554f9a1a7429ef306a
    # temporary fix
    import numpy as np
    from sysconfig import get_paths
    
    includeDirs=[np.get_include()]
    # python's include
    includeDirs.append(get_paths()['include'])
    includeDirs.append(get_license_srcdir())

    if bLicCheck:
        includeDirs.append(os.path.join(LG_PATH, "include"))

    print(f'include dirs with license: {includeDirs}')
    return includeDirs

def get_stem4d_libs():
    from sysconfig import get_paths
    libDirs = [os.path.join(get_paths()['data'], 'libs'),]
    if bLicCheck:
        libDirs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic"))
    return libDirs

def get_license_libs():
    from sysconfig import get_paths
    libDirs = [os.path.join(get_paths()['data'], 'libs'),]
    if bLicCheck:
        libDirs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic"))
    return libDirs

def get_emaps_srcdir():

    current_path = Path(os.path.abspath(__file__))

    parent_path = current_path.parent.absolute()

    return os.path.join(parent_path, 'diff-module')

def get_extra_objects():
    '''
    extra objects such as those from c code
    # '''
    if isUnsupportedOS():
        raise Exception('Unsupported OS. Only Windows and Linux OSs are supported')

    objs = []
    if isWindowsOS():
        objs = c_objs_free_win
        objs.append('write_dpbin.obj') 
    else:
        objs = c_objs_free_lin
        objs.append('write_dpbin.o')

    emaps_dir = get_emaps_srcdir()
    objlist = [os.path.join(emaps_dir, o) for o in objs]

    if isWindowsOS():
        for sl in intel_libs_win:
            objlist.append(sl+'.lib')
        return objlist
    
    if isLinuxOS():
        # lp = os.path.join(MKLROOT, 'lib','intel64','lib'+lapack_lib+'.a')
        # objlist.append(lp)
        # return objlist #on Linux, all dynamic, except lapacks
        if intel_static_libs_lin is None or len(intel_static_libs_lin) == 0:
            return objlist

        sl = []

        if 'DOCKER_BUILD' in os.environ:
            sl.append(os.path.join(MKLROOT, 'lib', lapack_static_lib))
            for l in intel_static_libs_lin:
                sl.append(os.path.join(MKLROOT, 'lib', l))
        else:
            sl.append(os.path.join(MKLROOT, 'lib', 'intel64', lapack_static_lib))
            for l in intel_static_libs_lin:
                sl.append(os.path.join(MKLROOT, 'lib', 'intel64', l))

        slen = len(sl)
        objlist.append(sl[0]) #lapack lib
        if slen > 2:
            objlist.append('-Wl,--start-group')
            for i in range(1,slen):
                objlist.append(os.path.join(MKLROOT, 'lib', 'intel64', sl[i]))
            objlist.append('-Wl,--end-group')
        return objlist
    # else:
    #     for sl in intel_libs_win:
    #         objlist.append(sl)
    #     return objlist

    raise ValueError('Error composing extra objects: unsopported OS')

def get_scattering_sources():

    emaps_dir = get_emaps_srcdir()

    src_list = []
    for sf in sct_files:
        src_list.append(os.path.join(emaps_dir, sf))
    
    return src_list        


def get_spg_sources():

    emaps_dir = get_emaps_srcdir()

    src_list = []
    for sf in spgra_files:
        src_list.append(os.path.join(emaps_dir, sf))
    
    return src_list

def get_diffract_sources(comp=None):

    src_list = []
    emaps_dir = get_emaps_srcdir()

    pyfname = mod_name
    # if build_type == 'full':
    # pyfname += '_dpgen'

    pyf = ".".join([pyfname,'pyf'])
    src_list.append(pyf)
    src_list.extend(dif_source)
    src_list.extend(csf_files)
    src_list.extend(powder_files)
    src_list.extend(bloch_files)
    src_list.extend(stereo_files)
    src_list.extend(mxtal_files)
    # if build_type == 'full':
    src_list.extend(dpgen_files)
    
    
    print(f'source code list: {src_list}')
    return [os.path.join(emaps_dir, srcfn) for srcfn in src_list]

# def get_cifreader_source():
#     current_path = Path(os.path.abspath(__file__))
#     emaps_parent_path = current_path.parent.absolute()
#     cifreader_path = os.path.join(emaps_parent_path, 'CifFile')

#     print(f'-----------CifReader Source path: {cifreader_path}')

#     src_files = ["src/lib/lex.yy.c","src/lib/py_star_scan.c"]
#     return [os.path.join(cifreader_path, s) for s in src_files]

# def get_comp():
#     '''
#     Get emaps component to be built from comp.json file
#     '''
    
#     import json, os
#     from pathlib import Path

#     json_cfg = os.getenv('PYEMAPS_JSON')

#     if not json_cfg:
#         json_cfg = "comp.json" # default

#     emapsdir = get_emaps_srcdir()
#     comp = 'dif'

#     comp_cfg = os.path.join(emapsdir,json_cfg)
#     try:
#         with open(comp_cfg, 'r') as jf:
#             comp = json.load(jf)['component']

#     except IOError as e:
#         raise ValueError(f"Error reading component configure file: {e}")
   
#     return comp

# class build_dp_ext(numpy_build_ext):
#     def finalize_options(self):
#         numpy_build_ext.finalize_options(self)
#         emapsdir = get_emaps_srcdir()
#         cobj = os.path.join(emapsdir, dpgen_cobj)
#         self.link_objects = [cobj]

# def get_samples(sdn = 'samples'):
#     '''
#     input: sdn = sample directory name under emaps
#     '''

#     import os, glob
#     base_dir = os.path.realpath(__file__)
#     samples_base_dir = os.path.join(os.path.dirname(base_dir), sdn)
#     sbase_files = os.path.join(samples_base_dir, '*.py')
#     sfile_list = glob.glob(sbase_files)
#     # sfile_list.append('al_db.bin')
#     sfile_list.append('al.img')

#     return [os.path.join(sdn, os.path.basename(name)) for name in sfile_list]

# def get_cdata(sdn = 'cdata'):
#     '''
#     input: sdn = sample directory name under emaps
#     '''
#     import glob


#     free_xtl_remove = []
#     if build_type == 'free':
#         free_xtl_remove = ['SiAlONa.xtl']

#     base_dir = os.path.realpath(__file__)
#     samples_base_dir = os.path.join(os.path.dirname(base_dir), sdn)
#     sbase_files = os.path.join(samples_base_dir, '*.xtl')
#     sfile_list = glob.glob(sbase_files)
#     res = [os.path.join(sdn, os.path.basename(name)) for name in sfile_list]
   
#     out =[]
    
#     for rf in res:
#         _, rfn = os.path.split(rf)
#         if rfn not in free_xtl_remove:
#             out.append(rf)
        
#     return out

def get_library_dirs():
    
    # import platform

    if isUnsupportedOS():
        raise ValueError("Unsupported OS!")

    lib_folder = ''
    mkl_folder = 'intel64'

    # osname = platform.platform().lower()
    # print(f'OS found: {osname}')
    libdir = []
    if isWindowsOS():
        lib_folder = 'intel64_win'
        # libdir.append(os.path.join(VS2022INSTALLDIR, 'VC', 'Tools', 'MSVC', 'lib', 'x64'))
    else:
        lib_folder = 'intel64_lin'
    
    libdir.append(os.path.join(IFORTROOT, 'compiler', 'lib', lib_folder)) #intel openmp libdir
    libdir.append(os.path.join(MKLROOT, 'lib', mkl_folder))
    
    return libdir

def get_include_dirs():
    # pass
    incl = []
    incl.append(get_emaps_srcdir())
    if isLinuxOS():
        incl.append(os.path.join(MKLROOT, 'include', 'intel64', 'lp64'))

    # TODO check on Windows side intel mkl advisor to add:  /module:"%MKLROOT%\include\intel64\lp64" 
    incl.append(os.path.join(MKLROOT, 'include'))
    return incl

def get_libraries():
    # import sys, os

    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing libraries list")

    if isWindowsOS(): 
        # libs = [lapack_lib]
        # libs = intel_libs_win.copy()
        libs=[]
        libs.append('msvcrt')
        return libs
     
    #  otherwise it is linux
    libs = intel_libs_lin.copy()
     
        # for l in libs:
        #     libs.append(l)
        
        # libs[0] = libs[0]+'.a'
        # print(f'*****linux static libs: {libs}')
        # for i in range(4):
        #     libs[i] = os.path.join(MKLROOT, 'lib', 'intel64', 'lib'+libs[i])
        # #     libs[i] = 'lib'+libs[i]
        
        # print(f'*****linux static libs after: {libs}')
      
    # else:
    #     raise Exception('The OS is not supported')

    # libs.insert(0, lapack_lib)
    return libs

def get_compiler_args():
    # import sys
    
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing compiler arguements list")

    if isWindowsOS(): 
        return compile_args if emaps_debug == 0 else compile_args_debug

    return compile_args_lin

def get_install_requires():
    # import sys
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing install re list")

    install_reqs = install_requires_common.copy()
    # return install_reqs
    if isWindowsOS(): 
        install_reqs += [
                        # 'msvc-runtime == 14.36.32532', for working with 2022 MSVC
                        'msvc-runtime == 14.29.30133'
                        # 'intel-fortran-rt == 2022.1.0',
                        # 'mkl == 2022.1.0'
                        ]
        return install_reqs
    # install_reqs += []
    # for linux
    if 'DOCKER_BUILD' in os.environ:
        # for docker build. need the latest oneAPI components
        print(f'For docker build')
        # this vesion should change with docker base image Intel oneAPI version
        install_reqs += ['intel-fortran-rt==2024.0.0']
    else:
        # for local build
        print(f'For local build')
        # install_reqs += ['intel-fortran-rt == 2022.1.0',
        #              'mkl == 2022.1.0']
    # install_reqs += ['intel-fortran-rt',
    #                  'mkl']

    return install_reqs
    
    
def get_emaps_macros():
    
    if build_type != 'uiuc' and build_type != 'full' and build_type != 'free':
        raise ValueError("Error: build type not specified")

    def_list = [('NPY_NO_DEPRECATED_API','NPY_1_7_API_VERSION')]
    
    undef_list = []

    if build_type == 'full':
        # full version
        undef_list.append('__BFREE__')
        undef_list.append('__BUIUC__')
        if bLicCheck:
            def_list.append(('__LIC_CHECK__', 1))

    if build_type == 'free':
        # limited free version
        def_list.append(('__BFREE__', 1))
        undef_list.append('__BUIUC__')
        undef_list.append('__LIC_CHECK__')

    if build_type == 'uiuc':
        # less limited free version
        def_list.append(('__BUIUC__', 1))
        undef_list.append('__BFREE__')
        def_list.append(('__LIC_CHECK__', 1))

    if emaps_debug != 0:
        # print(f'Build is debug build: {emaps_debug}-- for debugging only')
        def_list.append(('__BDEBUG__', 1))
    else:
        # print(f'Build is not a debug build: {emaps_debug}') -- for debugging only
        undef_list.append('__BDEBUG__')
        undef_list.append('__INIT0__')
    
    # print(f'defundef list: {def_list}, {undef_list}') -- for debugging only
    # exit() -- for debugging only
    return [def_list, undef_list]
    
# ------------------- must set this before build -------------------
def get_extra_link_args():
    '''
    place all of the static libraries in this list
    '''
    
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing extra link options list")

    args = []
    if isLinuxOS():
        # sl = []
        # for l in intel_static_libs_lin:
        #     sl.append(os.path.join(MKLROOT, 'lib', 'intel64', l))

        # args.append(os.path.join(MKLROOT, 'lib', 'intel64', sl[0]))
        # args.append('-Wl,')
        # # args.append('--start-group')
        # args.append(os.path.join(MKLROOT, 'lib', 'intel64', sl[1]))
        # args.append(os.path.join(MKLROOT, 'lib', 'intel64', sl[2]))
        # args.append(os.path.join(MKLROOT, 'lib', 'intel64', sl[3]))
        # args.append('-Wl,')
        # args.append('--end-group')
        for sl in intel_static_libs_lin:
            args.append(os.path.join(MKLROOT, 'lib', 'intel64', sl))
        print(f'##########link options: {args}')
        return args
    
    return intel_libs_win
    
emaps_build_defs, emaps_build_undefs= get_emaps_macros()

emaps_dif = Extension("emaps.diffract.emaps_sims",
        sources                     = get_diffract_sources(),
        extra_f90_compile_args      = get_compiler_args(),
        define_macros               = emaps_build_defs,
        undef_macros                = emaps_build_undefs,
        # extra_link_args             = get_extra_link_args(),
        extra_link_args             = [],
        libraries                   = get_libraries(),
        library_dirs                = get_library_dirs(),
        include_dirs                = get_include_dirs(),
        extra_objects               = get_extra_objects(),
        f2py_options                = ["--quiet",]
)

emaps_scattering = Extension("emaps.scattering.scattering",
        sources                     = get_scattering_sources(),
        extra_f90_compile_args      = get_compiler_args(),
        extra_link_args             = [],
        define_macros               = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
                                      ],
        f2py_options           = ["--quiet",]
)

emaps_spg = Extension("emaps.spg.spg",
        sources                     = get_spg_sources(),
        extra_f90_compile_args      = get_compiler_args(),
        extra_link_args             = [],
        define_macros               = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
        f2py_options                = ["--quiet",]
)

emaps_stem4d =  Extension(
            'emaps.stem4d._stem4d',
            sources                 =get_stem4d_sources(),
            extra_objects           =[],
            include_dirs            =get_stem4d_includes(),
            library_dirs            =get_stem4d_libs(),
            libraries               =["LicenseSpring"] if bLicCheck else [],
            define_macros           = emaps_build_defs,
            undef_macros            = emaps_build_undefs,
            extra_compile_args      =['-O2'],
            extra_link_args         =['-Wl,-v'],
            swig_opts               =['-keyword', '-O', '-macroerrors']
)

# emaps_license =  Extension(
#             'emaps.license._license',
#             sources                 =get_license_sources(),
#             extra_objects           =[],
#             include_dirs            =get_license_includes(),
#             library_dirs            =get_license_libs(),
#             libraries               =["LicenseSpring"] if bLicCheck else [],
#             define_macros           = emaps_build_defs,
#             undef_macros            = emaps_build_undefs,
#             extra_compile_args      =['-O2'],
#             extra_link_args         =[],
#             swig_opts               =['-keyword', '-O', '-macroerrors']
# )

def get_version(f):
    version = {}
    with open(f + ".py") as fp:
        exec(fp.read(), version)
    
    return version[f]

def get_long_description():
    from codecs import open
    from os import path
        
    here = path.abspath(path.dirname(__file__))
        
    # Get the long description from the README file
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    
    return long_description

def get_dylibs():
    
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing dynamic libs list")

    dylibs=[]
    if isLinuxOS():
        dlibs = [
                # 'libiomp5.so', 
                # 'libifport.so.5', 
                # 'libifcoremt.so.5',
                # 'libimf.so',
                # 'libsvml.so'
                ]
        if 'DOCKER_BUILD' in os.environ: 
            for l in dlibs:
                dylibs.append(os.path.join(IFORTROOT, 'lib', l))
        else: 
            for l in dlibs:
                dylibs.append(os.path.join(IFORTROOT, 'lib', 'intel64_lin', l))
        return dylibs
    
    
    # iomp_dlibname = 'libiomp5.so'
    
    # if isLinuxOS():
    #     iomp_dlib_path = os.path.join(IFORTROOT, 
    #                                   'compiler', 
    #                                   'lib',
    #                                   'intel64_lin', 
    #                                   iomp_dlibname)
    # else:    
    iomp_dlibname = 'libiomp5md.dll'

    iomp_dlib_path = os.path.join(IFORTROOT, 
                                    'redist', 
                                    'intel64_win', 
                                    'compiler',
                                    iomp_dlibname)
    
    if not os.path.exists(iomp_dlib_path):
        print(f'#################Error finding iomp lib')
        raise ValueError('Could not find dynamic openmp library')
    # exit()
    dylibs.append(iomp_dlib_path)

    return dylibs

def get_lic_dylibs():
    
    if not bLicCheck:
        return []
     
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing license dynamic libs list")

    dylibs=[]
    if isLinuxOS():
        return dylibs # TODO need to fill this in for linux license libraries
    #     dlibs = [
    #             # 'libiomp5.so', 
    #             # 'libifport.so.5', 
    #             # 'libifcoremt.so.5',
    #             # 'libimf.so',
    #             # 'libsvml.so'
    #             ]
    #     if 'DOCKER_BUILD' in os.environ: 
    #         for l in dlibs:
    #             dylibs.append(os.path.join(IFORTROOT, 'lib', l))
    #     else: 
    #         for l in dlibs:
    #             dylibs.append(os.path.join(IFORTROOT, 'lib', 'intel64_lin', l))
    #     return dylibs
    
    
    # # iomp_dlibname = 'libiomp5.so'
    
    # # if isLinuxOS():
    # #     iomp_dlib_path = os.path.join(IFORTROOT, 
    # #                                   'compiler', 
    # #                                   'lib',
    # #                                   'intel64_lin', 
    # #                                   iomp_dlibname)
    # # else:    
    # lic_dlibname = 'LicenseSpring.dll'
    
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "LicenseSpring.dll"))
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "libcrypto-3-x64.dll"))
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "libcurl.dll"))
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "libssl-3-x64.dll"))
    
    return dylibs

def get_license_dylibs():
    
    if not bLicCheck:
        return []
     
    if isUnsupportedOS():
        raise ValueError("Unsupported OS in composing license dynamic libs list")

    dylibs=[]
    if isLinuxOS():
        return dylibs # TODO need to fill this in for linux license libraries
    #     dlibs = [
    #             # 'libiomp5.so', 
    #             # 'libifport.so.5', 
    #             # 'libifcoremt.so.5',
    #             # 'libimf.so',
    #             # 'libsvml.so'
    #             ]
    #     if 'DOCKER_BUILD' in os.environ: 
    #         for l in dlibs:
    #             dylibs.append(os.path.join(IFORTROOT, 'lib', l))
    #     else: 
    #         for l in dlibs:
    #             dylibs.append(os.path.join(IFORTROOT, 'lib', 'intel64_lin', l))
    #     return dylibs
    
    
    # # iomp_dlibname = 'libiomp5.so'
    
    # # if isLinuxOS():
    # #     iomp_dlib_path = os.path.join(IFORTROOT, 
    # #                                   'compiler', 
    # #                                   'lib',
    # #                                   'intel64_lin', 
    # #                                   iomp_dlibname)
    # # else:    
    # lic_dlibname = 'LicenseSpring.dll'
    
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "LicenseSpring.dll"))
    dylibs.append(os.path.join(LG_PATH, "bin", "x64", "dynamic", "libcrypto-3-x64.dll"))
    
    return dylibs

def get_package_list():
    base_package_list = ['emaps.scattering', 'emaps.scattering', 'emaps.spg']
    if build_type == 'free':
        return base_package_list
    
    return base_package_list.append('emaps.stem4d')

def get_data_files_list():
    base_list = [('emaps', 
                  ['__config__.py',
                   '__init__.py',
                   '__version__.py',
                   'README.md',
                   'COPYING',
                   'license.txt']
                  ),
                  ('emaps/diffract',get_dylibs())
                ]
    if build_type == 'free':
        return base_list

    return base_list.append(('emaps/stem4d', get_lic_dylibs()))
    
setup(name                              ="emaps",
      version                           = get_version('__version__'),
      long_description_content_type     ='text/markdown',
      long_description                  = get_long_description(),

      ext_modules                       = [emaps_dif, emaps_scattering, emaps_spg] if build_type == "free" else [emaps_dif, emaps_scattering, emaps_spg, emaps_stem4d],
      packages                          = ['emaps.diffract', 'emaps.scattering', 'emaps.spg'] if build_type == "free" else ['emaps.diffract', 'emaps.scattering', 'emaps.spg', 'emaps.stem4d'],
                                        # get_package_list(),
                                        # 
                                        #    'emaps.scattering', 
                                        #    'emaps.spg',
                                        #    'emaps.stem4d',
                                        # #    'emaps.license'
                                        #    ],
      
      package_dir                       = {'emaps':''},
      install_requires                  = get_install_requires(),
      
      data_files                        = 
                                        # get_data_files_list(),
                                          [('emaps', 
                                            ['__config__.py',
                                            '__init__.py',
                                            '__version__.py',
                                            'README.md',
                                            'COPYING',
                                            'license.txt']
                                            ),
                                            ('emaps/diffract',get_dylibs()),
                                            ('emaps/stem4d', get_lic_dylibs()),
                                            # ('emaps/license', get_license_dylibs())
                                          ],
      exclude_package_data              = {'emaps':['*.i', 
                                                '*.cpp', 
                                                '*.f90',
                                                '*.pyd', 
                                                '*.toml', 
                                                '*.in', 
                                                '__pycache__',
                                                '*.egg-info'
                                                ],
                                            'emaps/stem4d':['*.i', 
                                                    '*.cpp',
                                                    '*.h',
                                                    '__pycache__'
                                                    ],
                                            # 'emaps/license':['*.i', 
                                            #         '*.cpp',
                                            #         '*.h',
                                            #         '__pycache__'
                                            #         ],
                                            'emaps/diffract':[
                                                    '__pycache__'
                                                    ],
                                            'emaps/scattering':[
                                                    '__pycache__'
                                                    ],
                                            'emaps/spg':[
                                                    '__pycache__'
                                                    ]
                                            }
)

# if emaps_debug:
#     print(f'#######################Build is a debug build')
# else:
#     print(f'#######################Build is not a debug build')
# ------------- using intel compiler------------------------- 
# from setuptools import setup, Extension
# import os

# # Set the path to the Intel C Compiler executable
# os.environ['CC'] = 'C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\bin\\intel64\\icl.exe'

# # Set the necessary environment variables for the Intel C Compiler
# os.environ['INTEL_LICENSE_FILE'] = 'C:\\Program Files (x86)\\Intel\\Licenses\\use.lic'
# os.environ['INTEL_DEV_REDIST'] = 'C:\\Program Files (x86)\\Intel\\oneAPI\\redist\\intel64\\compiler'
# os.environ['LIB'] = 'C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\compiler\\lib\\intel64;C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29333\\ATLMFC\\lib\\x64;C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29333\\lib\\x64;C:\\Windows\\System32;C:\\Windows\\SysWOW64'
# os.environ['INCLUDE'] = 'C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\compiler\\include;C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29333\\ATLMFC\\include;C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.28.29333\\include'

# example_module = Extension('_example',
#                            sources=['example.i', 'example.c'],
#                            extra_compile_args=['/Qstd=c11', '/Wall', '/Wextra', '/QxHost', '/Qmarch=native', '/Qopenmp'],
#                            swig_opts=['-py3'],
#                            )