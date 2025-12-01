%undefine _debugsource_packages
Name: qtile
Version: 0.34.0
Release: 1
Summary: A pure-Python tiling window manager
Group: Graphical desktop/Other
Source0: https://github.com/qtile/qtile/archive/v%{version}/qtile-%{version}.tar.gz
License: MIT AND GPL-3.0-or-later
Url: http://qtile.org

BuildRequires: pkgconfig(python3)
BuildRequires: desktop-file-utils
BuildRequires: xwayland
BuildRequires: python-pywayland
BuildRequires: python-pywlroots
BuildRequires: python-xkbcommon

# Test dependencies
#BuildRequires:  x11-server-xvfb
#BuildRequires:  x11-server-xephyr
BuildRequires:  librsvg
BuildRequires: (pkgconfig(wlroots) >= 0.19.0 with pkgconfig(wlroots) < 0.20)
# https://github.com/qtile/qtile/issues/4830
BuildRequires: python-isort

# Some dependencies are loaded with ffi.dlopen, and to declare them properly
# we'll need this suffix.
%if 0%{?__isa_bits} == 32
%global libsymbolsuffix %{nil}
%else
%global libsymbolsuffix ()(%{__isa_bits}bit)
%endif

BuildRequires: libgobject-2.0.so.0%{libsymbolsuffix}
BuildRequires: libpango-1.0.so.0%{libsymbolsuffix}
BuildRequires: libpangocairo-1.0.so.0%{libsymbolsuffix}
Requires: libgobject-2.0.so.0%{libsymbolsuffix}
Requires: libpango-1.0.so.0%{libsymbolsuffix}
Requires: libpangocairo-1.0.so.0%{libsymbolsuffix}

# Recommended packages for widgets
Recommends: python-psutil
Recommends: python-pyxdg
Recommends: python-dbus-next
Recommends: python-xmltodict
Recommends: python-dateutil
Recommends: python-mpd2
Recommends: python-pulsectl
Recommends: python-pulsectl-asyncio

Requires: python-libqtile = %{version}-%{release}


%description
A pure-Python tiling window manager.

Features
========

    * Simple, small and extensible. It's easy to write your own layouts,
      widgets and commands.
    * Configured in Python.
    * Command shell that allows all aspects of
      Qtile to be managed and inspected.
    * Complete remote scriptability - write scripts to set up workspaces,
      manipulate windows, update status bar widgets and more.
    * Qtile's remote scriptability makes it one of the most thoroughly
      unit-tested window mangers around.


%package -n python-libqtile
Summary: Qtile's python library


%description -n python-libqtile
%{summary}.


%package wayland
Summary: Qtile wayland session

BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(wayland-protocols)

Requires: qtile = %{version}-%{release}
Requires: python-libqtile = %{version}-%{release}

%description wayland
%{summary}.

%pyproject_extras_subpkg -n python-libqtile wayland


%prep
%autosetup -p1

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
#PYTHONPATH=${PWD} ./scripts/ffibuild
PYTHONPATH=${PWD} %{python3} ./libqtile/backend/wayland/cffi/build.py
%py_build

%install
%py_install

mkdir -p %{buildroot}%{_datadir}/xsessions/
desktop-file-install \
    --dir %{buildroot}%{_datadir}/xsessions/ \
    resources/qtile.desktop

mkdir -p %{buildroot}%{_datadir}/wayland-sessions/
desktop-file-install \
    --dir %{buildroot}%{_datadir}/wayland-sessions/ \
    resources/qtile-wayland.desktop

%files
%doc README.rst
%{_bindir}/qtile
%{_datadir}/xsessions/qtile.desktop

%files -n python-libqtile
%{python_sitelib}/libqtile/
%{python_sitelib}/qtile-*.*.*.dist-info

%files wayland
%{_datadir}/wayland-sessions/qtile-wayland.desktop
