solution "meshio"
configurations { "Debug", "Release" }

configuration { "windows*" }
do
    defines {
        'WIN32',
        '_WIN32',
        '_WINDOWS',
    }
end

configuration { "vs*" }
do
    buildoptions {
        "/wd4996",
    }
end

configuration { "gmake" }
do
    buildoptions {
        "-std=c++0x",
    }
end

configuration "Debug gmake"
do
    buildoptions { "-g", "-Wall" }
    linkoptions { "-g" }
end

configuration "Debug"
do
    targetdir "../debug"
    flags { "Symbols" }
    defines { "DEBUG" }
end

configuration "Release"
do
    targetdir "../release"
    flags { "Optimize" }
    defines { "NDEBUG" }
end

-- A project defines one build target
project "meshio"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"

language "C++"
files { "*.h", "*.cpp" }
flags {
    "StaticRuntime",
}
includedirs {
}
defines {}
linkoptions {}
libdirs {}
links {}

