import os
import random
import uuid
from typing import List

from chomper.exceptions import EmulatorCrashedException
from chomper.loader import MachoLoader
from chomper.os import BaseOs
from chomper.types import Module

from .fixup import SystemModuleFixup
from .hooks import get_hooks
from .syscall import get_syscall_handlers


# Environment variables
ENVIRON_VARS = r"""SHELL=/bin/sh
PWD=/var/root
LOGNAME=root
HOME=/var/root
LS_COLORS=rs=0:di=01
CLICOLOR=
SSH_CONNECTION=127.0.0.1 59540 127.0.0.1 22
TERM=xterm
USER=root
SHLVL=1
PS1=\h:\w \u\$
SSH_CLIENT=127.0.0.1 59540 22
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/X11:/usr/games
MAIL=/var/mail/root
SSH_TTY=/dev/ttys000
_=/usr/bin/env
SBUS_INSERT_LIBRARIES=/usr/lib/substitute-inserter.dylib
__CF_USER_TEXT_ENCODING=0x0:0:0
CFN_USE_HTTP3=0
CFStringDisableROM=1"""


class IosOs(BaseOs):
    """Provide iOS runtime environment."""

    def __init__(self, emu, **kwargs):
        super().__init__(emu, **kwargs)

        self.loader = MachoLoader(emu)

        self.preferences = self._default_preferences.copy()
        self.device_info = self._default_device_info.copy()

        self.proc_info = self._init_proc_info()

        working_dir = os.path.dirname(self.proc_info["path"])
        self.emu.file_manager.set_working_dir(working_dir)

        self.executable_path = None

    @property
    def _default_preferences(self) -> dict:
        """Define default preferences."""
        return {
            "AppleLanguages": [
                "zh-Hans",
                "en",
            ],
            "AppleLocale": "zh-Hans",
        }

    @property
    def _default_device_info(self) -> dict:
        """Define default device info."""
        return {
            "UserAssignedDeviceName": "iPhone",
            "DeviceName": "iPhone13,1",
            "ProductVersion": "14.4.0",
        }

    @staticmethod
    def _init_proc_info() -> dict:
        """Initialize process info."""
        application_path = (
            f"/private/var/containers/Bundle/Application/{str(uuid.uuid4()).upper()}"
        )
        bundle_identifier = "com.yourcompany.ProductName"
        bundle_executable = "ProductName"

        return {
            "pid": random.randint(10000, 20000),
            "path": f"{application_path}/{bundle_identifier}/{bundle_executable}",
        }

    def _setup_hooks(self):
        """Initialize hooks."""
        self.emu.hooks.update(get_hooks())

    def _setup_syscall_handlers(self):
        """Initialize system call handlers."""
        self.emu.syscall_handlers.update(get_syscall_handlers())

    def _init_magic_vars(self):
        """Set flags meaning the arch type and others, which will be read by functions
        such as `_os_unfair_recursive_lock_lock_with_options`."""
        self.emu.uc.mem_map(0xFFFFFC000, 1024)

        # arch type
        self.emu.write_u64(0xFFFFFC023, 2)

        self.emu.write_u64(0xFFFFFC104, 0x100)

    def _construct_environ(self) -> int:
        """Construct a structure that contains environment variables."""
        lines = ENVIRON_VARS.split("\n")

        size = self.emu.arch.addr_size * (len(lines) + 1)
        buffer = self.emu.create_buffer(size)

        for index, line in enumerate(lines):
            address = buffer + self.emu.arch.addr_size * index
            self.emu.write_pointer(address, self.emu.create_string(line))

        self.emu.write_pointer(buffer + size - self.emu.arch.addr_size, 0)

        return buffer

    def _init_program_vars(self):
        """Initialize program variables, works like `__program_vars_init`."""
        argc = self.emu.create_buffer(8)
        self.emu.write_int(argc, 0, 8)

        nx_argc_pointer = self.emu.find_symbol("_NXArgc_pointer")
        self.emu.write_pointer(nx_argc_pointer.address, argc)

        nx_argv_pointer = self.emu.find_symbol("_NXArgv_pointer")
        self.emu.write_pointer(nx_argv_pointer.address, self.emu.create_string(""))

        environ = self.emu.create_buffer(8)
        self.emu.write_pointer(environ, self._construct_environ())

        environ_pointer = self.emu.find_symbol("_environ_pointer")
        self.emu.write_pointer(environ_pointer.address, environ)

        progname_pointer = self.emu.find_symbol("___progname_pointer")
        self.emu.write_pointer(progname_pointer.address, self.emu.create_string(""))

    def _init_dyld_vars(self):
        """Initialize global variables in `libdyld.dylib`."""
        g_use_dyld3 = self.emu.find_symbol("_gUseDyld3")
        self.emu.write_u8(g_use_dyld3.address, 1)

        dyld_all_images = self.emu.find_symbol("__ZN5dyld310gAllImagesE")

        # dyld3::closure::ContainerTypedBytes::findAttributePayload
        attribute_payload_ptr = self.emu.create_buffer(8)

        self.emu.write_u32(attribute_payload_ptr, 2**10)
        self.emu.write_u8(attribute_payload_ptr + 4, 0x20)

        self.emu.write_pointer(dyld_all_images.address, attribute_payload_ptr)

        # dyld3::AllImages::platform
        platform_ptr = self.emu.create_buffer(0x144)
        self.emu.write_u32(platform_ptr + 0x140, 2)

        self.emu.write_pointer(dyld_all_images.address + 0x50, platform_ptr)

    def _init_objc_vars(self):
        """Initialize global variables in `libobjc.A.dylib while
        calling `__objc_init`."""
        prototypes = self.emu.find_symbol("__ZL10prototypes")
        self.emu.write_u64(prototypes.address, 0)

        gdb_objc_realized_classes = self.emu.find_symbol("_gdb_objc_realized_classes")
        protocolsv_ret = self.emu.call_symbol("__ZL9protocolsv")

        self.emu.write_pointer(gdb_objc_realized_classes.address, protocolsv_ret)

        opt = self.emu.find_symbol("__ZL3opt")
        self.emu.write_pointer(opt.address, 0)

        # Disable pre-optimization
        disable_preopt = self.emu.find_symbol("_DisablePreopt")
        self.emu.write_u8(disable_preopt.address, 1)

        self.emu.call_symbol("__objc_init")

    def init_objc(self, module: Module):
        """Initialize Objective-C for the module.

        Calling `map_images` and `load_images` of `libobjc.A.dylib`.
        """
        if not module.binary or module.image_base is None:
            return

        if not self.emu.find_module("libobjc.A.dylib"):
            return

        initialized = self.emu.find_symbol("__ZZ10_objc_initE11initialized")
        if not self.emu.read_u8(initialized.address):
            # As the initialization timing before program execution
            self._init_magic_vars()
            self._init_program_vars()
            self._init_dyld_vars()
            self._init_objc_vars()

        text_segment = module.binary.get_segment("__TEXT")

        mach_header_ptr = module.base - module.image_base + text_segment.virtual_address
        mach_header_ptrs = self.emu.create_buffer(self.emu.arch.addr_size)

        self.emu.write_pointer(mach_header_ptrs, mach_header_ptr)

        try:
            self.emu.call_symbol("_map_images", 1, 0, mach_header_ptrs)
            self.emu.call_symbol("_load_images", 0, mach_header_ptr)
        except EmulatorCrashedException:
            self.emu.logger.warning("Initialize Objective-C failed.")
        finally:
            module.binary = None

    def search_module_binary(self, module_name: str) -> str:
        """Search system module binary in rootfs directory.

        raises:
            FileNotFoundError: If module not found.
        """
        lib_dirs = [
            "usr/lib/system",
            "usr/lib",
            "System/Library/Frameworks",
            "System/Library/PrivateFrameworks",
        ]

        for lib_dir in lib_dirs:
            path = os.path.join(self.rootfs_path or ".", lib_dir)

            lib_path = os.path.join(path, module_name)
            if os.path.exists(lib_path):
                return lib_path

            framework_path = os.path.join(path, f"{module_name}.framework")
            if os.path.exists(framework_path):
                return os.path.join(framework_path, module_name)

        raise FileNotFoundError("Module '%s' not found" % module_name)

    def resolve_modules(self, module_names: List[str]):
        """Load system modules if don't loaded."""
        fixup = SystemModuleFixup(self.emu)

        for module_name in module_names:
            if self.emu.find_module(module_name):
                continue

            module_file = self.search_module_binary(module_name)
            module = self.emu.load_module(
                module_file=module_file,
                exec_objc_init=False,
            )

            # Fixup must be executed before initializing Objective-C.
            fixup.install(module)

            self.init_objc(module)

    def _enable_objc(self):
        """Enable Objective-C support."""
        dependencies = [
            "libsystem_platform.dylib",
            "libsystem_kernel.dylib",
            "libsystem_c.dylib",
            "libsystem_pthread.dylib",
            "libsystem_info.dylib",
            "libsystem_darwin.dylib",
            "libsystem_featureflags.dylib",
            "libcorecrypto.dylib",
            "libcommonCrypto.dylib",
            "libc++abi.dylib",
            "libc++.1.dylib",
            "libmacho.dylib",
            "libdyld.dylib",
            "libobjc.A.dylib",
            "libdispatch.dylib",
            "libsystem_blocks.dylib",
            "libsystem_trace.dylib",
            "libsystem_sandbox.dylib",
            "libnetwork.dylib",
            "CoreFoundation",
            "CFNetwork",
            "Foundation",
            "Security",
        ]

        self.resolve_modules(dependencies)

        # Call initialize function of `CoreFoundation`
        self.emu.call_symbol("___CFInitialize")

        # Call initialize function of `Foundation`
        self.emu.call_symbol("__NSInitializePlatform")

    def _enable_ui_kit(self):
        """Enable UIKit support.

        Mainly used to load `UIDevice` class, which is used to get device info.
        """
        dependencies = [
            "QuartzCore",
            "BaseBoard",
            "FrontBoardServices",
            "PrototypeTools",
            "TextInput",
            "PhysicsKit",
            "CoreAutoLayout",
            "UIFoundation",
            "UIKitServices",
            "UIKitCore",
        ]

        self.resolve_modules(dependencies)

    def initialize(self):
        """Initialize environment."""
        self._setup_hooks()
        self._setup_syscall_handlers()

        if self.emu.enable_objc:
            self._enable_objc()

        if self.emu.enable_ui_kit:
            self._enable_ui_kit()
