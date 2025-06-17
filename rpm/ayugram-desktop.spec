%ifarch aarch64
    %global _lto_cflags %nil
%endif

# Telegram Desktop's constants...
%global appname AyuGramDesktop

%global td_commit 51743dfd01dff6179e2d8f7095729caa4e2222e9

# Reducing debuginfo verbosity...
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

Name: ayugram-desktop
Version: 5.14.3
Release: 2%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * Ayugram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * tg_owt - BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain -- static dependency;
# * rlottie - LGPL-2.1-or-later AND AND FTL AND BSD-3-Clause -- static dependency;
# * cld3  - Apache-2.0 -- static dependency;
# * qt_functions.cpp - LGPL-3.0-only -- build-time dependency;
# * open-sans-fonts  - Apache-2.0 -- bundled font;
# * vazirmatn-fonts - OFL-1.1 -- bundled font.
License: GPL-3.0-or-later AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain AND LGPL-2.1-or-later AND FTL AND MPL-1.1 AND LGPL-3.0-only AND OFL-1.1
URL: https://github.com/XWOKU/AyuGramBuilding
Summary: Ayugram Desktop, messaging app
Source0: %{url}/releases/download/v%{version}/%{appname}-v%{version}-full.tar.gz

Patch0: findprotobuf_fix.patch

# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64 aarch64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(fmt)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: cmake(ada)

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.68) >= 2.76.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
%if 0%{?fedora} < 41
BuildRequires: pkgconfig(openssl)
%endif
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(webkitgtk-6.0)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-devel
BuildRequires: gcc
BuildRequires: git
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libdispatch-devel
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static
BuildRequires: gperftools-devel
BuildRequires: gperf
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: gcc-c++
BuildRequires: pkgconfig(openh264)
BuildRequires: cmake(KF6CoreAddons)

Requires: hicolor-icon-theme
Requires: qt6-qtimageformats%{?_isa}
Requires: webkitgtk6.0%{?_isa}

# Short alias for the main package...
Provides: ayugram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: ayugram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Virtual provides for bundled libraries...
Provides: bundled(cld3) = 3.0.13~gitb48dc46
Provides: bundled(kf5-kcoreaddons) = 5.106.0
Provides: bundled(libtgvoip) = 2.4.4~git7c46f4c
Provides: bundled(open-sans-fonts) = 1.10
Provides: bundled(plasma-wayland-protocols) = 1.6.0
Provides: bundled(rlottie) = 0~git8c69fc2
Provides: bundled(vazirmatn-fonts) = 27.2.2
Provides: bundled(cppgir) = 0~git69ef481c
Provides: bundled(minizip) = 1.2.13

%description
Desktop Telegram client with good customization and Ghost mode.

%prep
git clone https://github.com/tdlib/td.git %{_builddir}/tdlib && cd %{_builddir}/tdlib && git reset --hard %{td_commit}
cmake -S %{_builddir}/tdlib -B %{_builddir}/tdlib/build \
	-DCMAKE_BUILD_TYPE=None \
	-DCMAKE_INSTALL_PREFIX="%{_builddir}/tdlib/install" \
	-Wno-dev \
	-DTD_E2E_ONLY=ON
cmake --build %{_builddir}/tdlib/build
cmake --install %{_builddir}/tdlib/build

# Unpacking Telegram Desktop source archive...
%autosetup -n %{appname}-v%{version}-full -p1

# Unbundling libraries... except minizip
rm -rf Telegram/ThirdParty/{QR,dispatch,expected,fcitx-qt5,fcitx5-qt,hime,hunspell,jemalloc,kimageformats,lz4,nimf,range-v3,xxHash}

# Fix minizip requrement
# sed -i 's|2.0.0|4.0.0|' cmake/external/minizip/CMakeLists.txt

%if 0%{?fedora} >= 41
sed -i "/#include <openssl\/engine.h>/d" Telegram/SourceFiles/core/utils.cpp
%endif

%build
# Building Telegram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_ID=2040 \
    -Dtde2e_DIR="%{_builddir}/tdlib/install/lib/cmake/tde2e" \
    -DTDESKTOP_API_HASH=b18441a1ff607e10a989891a5462e627 \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/dbus-1/services/com.ayugram.desktop.service
%{_metainfodir}/*.metainfo.xml

%changelog
* Mon Jun 17 2025 Oleg XWOKU <136835599+XWOKU@users.noreply.github.com> - 5.14.3-2
- Rebuild (openh264)

* Mon Jun 16 2025 Oleg XWOKU <136835599+XWOKU@users.noreply.github.com> - 5.14.3
- Initial build
