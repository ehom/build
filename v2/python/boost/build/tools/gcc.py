#  Copyright (c) 2001 David Abrahams.
#  Copyright (c) 2002-2003 Rene Rivera.
#  Copyright (c) 2002-2003 Vladimir Prus.
#
#  Use, modification and distribution is subject to the Boost Software
#  License Version 1.0. (See accompanying file LICENSE_1_0.txt or
#  http://www.boost.org/LICENSE_1_0.txt)

import unix, builtin, common
from boost.build.build import feature, toolset, type, action
from boost.build.util.utility import *

feature.extend_feature ('toolset', ['gcc'])

toolset.inherit_generators ('gcc', [], 'unix', ['unix.link', 'unix.link.dll'])
toolset.inherit_flags ('gcc', 'unix')

# TODO: (PF) I think we no longer need this.
#toolset.inherit-rules gcc : unix ;

# Make the "o" suffix used for gcc toolset on all
# platforms
type.set_generated_target_suffix ('OBJ', ['<toolset>gcc'], 'o')
type.set_generated_target_suffix ('STATIC_LIB', ['<toolset>gcc'], 'a')


def init (version = None, command = None, options = None):
    """ Initializes the gcc toolset for the given version.
        If necessary, command may be used to specify where the compiler
        is located.
        The parameter 'options' is a space-delimited list of options, each
        one being specified as <option-name>option-value. Valid option names
        are: cxxflags, linkflags and linker-type. Accepted values for linker-type
        are gnu and sun, gnu being the default.
        Example:
          using gcc : 3.4 : : <cxxflags>foo <linkflags>bar <linker-type>sun ;
    """
    options = to_seq (options)

    condition = common.check_init_parameters ('gcc', ('version', version))
    
    command = common.get_invocation_command ('gcc', 'g++', command)

    common.handle_options ('gcc', condition, command, options)
    
    linker = feature.get_values ('<linker-type>', options)
    if not linker:
        linker = 'gnu'

    init_link_flags ('gcc', linker, condition)




###################################################################
# Still to port.
# Original lines are prefixed with "### "
#
### if [ os.name ] = NT
### {
###     # This causes single-line command invocation to not go through
###     # .bat files, thus avoiding command-line length limitations
###     JAMSHELL = % ;  
### }


def gcc_compile_cpp (target, sources, properties):
    # Some extensions are compiled as C++ by default. For others, we need
    # to pass -x c++.
    # We could always pass -x c++ but distcc does not work with it.
    # TODO: implement this
#    if ! $(>:S) in .cc .cp .cxx .cpp .c++ .C
#    {
#        LANG on $(<) = "-x c++" ;
#    }
    pass

action.action (gcc_compile_cpp, ['"$(CONFIG_COMMAND)" $(LANG) -Wall -ftemplate-depth-100 $(OPTIONS) -D$(DEFINES) -I"$(INCLUDES)" -c -o "$(<)" "$(>)"'])

builtin.register_c_compiler ('gcc.compile.c++', gcc_compile_cpp, ['CPP'], ['OBJ'], ['<toolset>gcc'])


def gcc_compile_c (target, sources, properties):
    # If we use the name g++ then default file suffix -> language mapping
    # does not work. So have to pass -x option. Maybe, we can work around this
    # by allowing the user to specify both C and C++ compiler names.
    # TODO: implement this
    # LANG on $(<) = "-x c" ;
    pass

action.action (gcc_compile_c, ['"$(CONFIG_COMMAND)" $(LANG) -Wall $(OPTIONS) -D$(DEFINES) -I"$(INCLUDES)" -c -o "$(<)" "$(>)"'])

builtin.register_c_compiler ('gcc.compile.c', gcc_compile_c, ['C'], ['OBJ'], ['<toolset>gcc'])


### # Declare flags and action for compilation
### flags gcc.compile OPTIONS <optimization>off : -O0 ;
### flags gcc.compile OPTIONS <optimization>speed : -O3 ;
### flags gcc.compile OPTIONS <optimization>space : -Os ;
### 
### flags gcc.compile OPTIONS <inlining>off : -fno-inline ;
### flags gcc.compile OPTIONS <inlining>on : -Wno-inline ;
### flags gcc.compile OPTIONS <inlining>full : -finline-functions -Wno-inline ;
### 
### flags gcc.compile OPTIONS <debug-symbols>on : -g ;
### flags gcc.compile OPTIONS <profiling>on : -pg ;
### # On cygwin and mingw, gcc generates position independent code by default,
### # and warns if -fPIC is specified. This might not be the right way
### # of checking if we're using cygwin. For example, it's possible 
### # to run cygwin gcc from NT shell, or using crosscompiling.
### # But we'll solve that problem when it's time. In that case
### # we'll just add another parameter to 'init' and move this login
### # inside 'init'.
### if [ os.name ] != CYGWIN && [ os.name ] != NT
### {        
###     flags gcc.compile OPTIONS <link>shared/<main-target-type>LIB : -fPIC ;
### }    
### if [ os.name ] != NT
### {
###     HAVE_SONAME = "" ;
### }
### 
### 
### 
### flags gcc.compile OPTIONS <cflags> ;
### flags gcc.compile.c++ OPTIONS <cxxflags> ;
### flags gcc.compile DEFINES <define> ;
### flags gcc.compile INCLUDES <include> ;
### 
### # The class which check that we don't try to use
### # the <link-runtime>static property while creating or using shared library,
### # since it's not supported by gcc/libc.
### class gcc-linking-generator : UnixLinkingGenerator
### {
###     rule generated-targets ( sources + : property-set : project name ? )
###     {
###         if <link-runtime>static in [ $(property-set).raw ] 
###         {
###             local m ;
###             if [ id ] = "gcc.link.dll"
###             {
###                 m = "on gcc, DLL can't be build with <link-runtime>static" ;
###             }         
###             if ! $(m) {                
###                 for local s in $(sources)
###                 {
###                     local type = [ $(s).type ] ;
###                     if $(type) &&  [ type.is-derived $(type) SHARED_LIB ] 
###                     {
###                         m = "on gcc, using DLLS together with the <link-runtime>static options is not possible " ;
###                     }                
###                 }                
###             }
###             if $(m)
###             {
###                 errors.user-error $(m) :
###                   "it's suggested to use <link-runtime>static together with the <link>static" ;
###             }
###             
###         }
###                         
###         return [ UnixLinkingGenerator.generated-targets 
###             $(sources) : $(property-set) : $(project) $(name) ] ;
###     }    
### }
### 
### generators.register [ new gcc-linking-generator gcc.link : LIB OBJ : EXE 
###     : <toolset>gcc ] ;
### 
### generators.register [ new gcc-linking-generator gcc.link.dll : LIB OBJ : SHARED_LIB 
###     : <toolset>gcc ] ;
### 
### generators.override gcc.prebuilt : builtin.prebuilt ;
### generators.override gcc.searched-lib-generator : searched-lib-generator ;
### 
### 
### 
### # Declare flags for linking
### # First, the common flags
### flags gcc.link OPTIONS <debug-symbols>on : -g ;
### flags gcc.link OPTIONS <profiling>on : -pg ;
### flags gcc.link OPTIONS <linkflags> ;
### flags gcc.link LINKPATH <library-path> ;
### flags gcc.link FINDLIBS-ST <find-static-library> ;
### flags gcc.link FINDLIBS-SA <find-shared-library> ;
### flags gcc.link LIBRARIES <library-file> ;
### 
### # For <link-runtime>static we made sure there are no dynamic libraries 
### # in the link
### flags gcc.link OPTIONS <link-runtime>static : -static ;

def init_link_flags (tool, linker, condition):
    """ Sets the vendor specific flags.
    """
    if linker == 'gnu':
        # Strip the binary when no debugging is needed.
        # We use --strip-all flag as opposed to -s since icc
        # (intel's compiler) is generally option-compatible with
        # and inherits from gcc toolset, but does not support -s
        toolset.flags (tool + '.link', 'OPTIONS', condition + '/<debug-symbols>off', ['-Wl,--strip-all'])
        toolset.flags (tool + '.link', 'RPATH', condition, ['<dll-path>'])
        toolset.flags (tool + '.link', 'RPATH_LINK', condition, ['<xdll-path>'])

    elif linker == 'darwin':
        # we can't pass -s to ld unless we also pass -static
        # so we removed -s completly from OPTIONS and add it
        # to ST_OPTIONS            
        toolset.flags (tool + '.link', 'ST_OPTIONS', condition + '/<debug-symbols>off', ['-s'])
        toolset.flags (tool + '.link', 'RPATH', condition, ['<dll-path>'])
        toolset.flags (tool + '.link', 'RPATH_LINK', condition, ['<xdll-path>'])

    elif linker == 'sun':
        toolset.flags (tool + '.link', 'OPTIONS', condition + '/<debug-symbols>off', ['-Wl,-s'])
        toolset.flags (tool + '.link', 'RPATH', condition, ['<dll-path>'])
        # Solaris linker does not have a separate -rpath-link, but
        # allows to use -L for the same purpose.
        toolset.flags (tool + '.link', 'LINKPATH', condition, ['<xdll-path>'])

        # This permits shared libraries with non-PIC code on Solaris
        # VP, 2004/09/07: Now that we have -fPIC hardcode in link.dll,
        # the following is not needed. Whether -fPIC should be hardcoded,
        # is a separate question.
        # AH, 2004/10/16: it is still necessary because some tests link
        # against static libraries that were compiled without PIC.
        toolset.flags (tool + '.link', 'OPTIONS', condition + '/<link>shared', ['-mimpure-text'])

    else:
            raise UserError ("'%s' initialization: invalid linker '%s'\n" \
                "The value '%s' specified for <linker> is not recognized.\n" \
                "Possible values are: 'darwin', 'sun', 'gnu'" % (toolset, linker, linker))

### # Declare actions for linking
### rule link ( targets * : sources * : properties * )
### {
###     SPACE on $(targets) = " " ;    
### }
### 
### actions link bind LIBRARIES
### {
###     "$(CONFIG_COMMAND)" -L"$(LINKPATH)" -Wl,-R$(SPACE)-Wl,"$(RPATH)" -Wl,-rpath-link$(SPACE)-Wl,"$(RPATH_LINK)" -o "$(<)" "$(>)" "$(LIBRARIES)" -l$(FINDLIBS-ST) -l$(FINDLIBS-SA) $(OPTIONS) 
### }
### 
### # Declare action for creating static libraries
### # The 'r' letter means to replace files in the archive
### # The 'u' letter means only outdated files in the archive
### #   should be replaced.
### # The 'c' letter means suppresses warning in case the archive
### #   does not exists yet. That warning is produced only on
### #   some platforms, for whatever reasons.
### actions piecemeal archive 
### {
###     ar ruc "$(<)" "$(>)"
### }
### 
### 
### rule link.dll ( targets * : sources * : properties * )
### {
###     SPACE on $(targets) = " " ;    
### }
### 
### # Differ from 'link' above only by -shared.
### actions link.dll bind LIBRARIES
### {
###     "$(CONFIG_COMMAND)" -L"$(LINKPATH)" -Wl,-R$(SPACE)-Wl,"$(RPATH)" -o "$(<)" $(HAVE_SONAME)-Wl,-h$(SPACE)-Wl,$(<[1]:D=) -shared "$(>)"  "$(LIBRARIES)" -l$(FINDLIBS-ST) -l$(FINDLIBS-SA) $(OPTIONS)  
### }
### 
### # Set up threading support. It's somewhat contrived, so perform it at the end,
### # to avoid cluttering other code.
### 
### if [ os.on-windows ] 
### {
###     flags gcc OPTIONS <threading>multi : -mthreads ;
### }
### else if [ modules.peek : UNIX ] 
### {
###     switch [ modules.peek : JAMUNAME ]
###     {
###     case SunOS* :
###         {
###         flags gcc OPTIONS <threading>multi : -pthreads ;
###         flags gcc FINDLIBS-SA <threading>multi : rt ;
###         }
###     case BeOS :
###         {
###         # BeOS has no threading options, don't set anything here.
###         }
###     case *BSD :
###         {
###         flags gcc OPTIONS <threading>multi : -pthread ;
###         # there is no -lrt on BSD
###         }
###     case DragonFly :
###         {
###         flags gcc OPTIONS <threading>multi : -pthread ;
###         # there is no -lrt on BSD - DragonFly is a FreeBSD variant,
###         # which anoyingly doesn't say it's a *BSD.
###         }
###     case IRIX :
###         {
###         # gcc on IRIX does not support multi-threading, don't set anything here.
###         }
###     case HP_UX :
###         {
###         # gcc on HP-UX does not support multi-threading, don't set anything here
###         }
###     case Darwin :
###         {
###         # Darwin has no threading options, don't set anything here.
###         }
###     case * :
###         {
###         flags gcc OPTIONS <threading>multi : -pthread ;
###         flags gcc FINDLIBS-SA <threading>multi : rt ;
###         }
###     }
### }
