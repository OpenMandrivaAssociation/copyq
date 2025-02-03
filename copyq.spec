%define source_name CopyQ
# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

# repack non-release git branches as .xz with the commit date
# in the following format <name>-<version>-<commit_date>.xz
# the short commit tag should be 7 characters long

Name:           copyq
Version:        9.1.0
Release:        %{?commit_date:~0.%{commit_date}.}1
Summary:        Clipboard manager with advanced features
Group:          Utilities
License:        GPLv3
URL:            https://github.com/hluk/CopyQ

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        https://github.com/<org_name>/<project_name>/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.xz
%else
Source0:        %url/archive/%{version}.tar.gz#/%{source_name}-%{version}.tar.gz
%endif

BuildSystem:   cmake
BuildOption:   -Wno-dev 
BuildOption:   -DWITH_QT6:BOOL=ON 
BuildOption:   -DWITH_TESTS:BOOL=ON
BuildOption:   -DPLUGIN_INSTALL_PREFIX=%{_libdir}/%{name}/plugins
BuildOption:   -DTRANSLATION_INSTALL_PREFIX:PATH=%{_datadir}/%{name}/locale

BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6StatusNotifierItem)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Tools)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(appstream-glib)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(Qt6Qwt6)
BuildRequires: desktop-file-utils
BuildRequires: git

%description
CopyQ is an advanced clipboard manager with powerful editing and scripting features.

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/com.github.hluk.%{name}.desktop

%files
%doc AUTHORS CHANGES.md HACKING README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/metainfo/com.github.hluk.%{name}.appdata.xml
%{_datadir}/applications/com.github.hluk.%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.png
%{_datadir}/icons/hicolor/*/apps/%{name}*.svg
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/locale/%{name}*.qm
%{_datadir}/%{name}/themes/
%{_mandir}/man1/%{name}.1.*

