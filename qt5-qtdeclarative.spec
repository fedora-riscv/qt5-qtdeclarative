
%global qt_module qtdeclarative

Summary: Qt5 - QtDeclarative component
Name:    qt5-%{qt_module}
Version: 5.0.2
Release: 4%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://releases.qt-project.org/qt5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# qt5-qtjsbackend supports only ix86, x86_64 and arm , and so do we here
ExclusiveArch: %{ix86} x86_64 %{arm}

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtjsbackend-devel >= %{version}

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}

make %{?_smp_mflags}


%install

make install INSTALL_ROOT=%{buildroot}

# put non-conflicting binaries with -qt5 postfix in %{_bindir}
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    qmlplugindump|qmlprofiler)
      mv $i ../../../bin/${i}-qt5
      ln -s ../../../bin/${i}-qt5 .
      ln -s ../../../bin/${i}-qt5 $i
      ;;
   *)
      mv $i ../../../bin/
      ln -s ../../../bin/$i .
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt
%doc dist/changes*
%{_qt5_libdir}/libQt5Qml.so.5*
%{_qt5_libdir}/libQt5Quick.so.5*
%{_qt5_libdir}/libQt5QuickParticles.so.5*
%{_qt5_libdir}/libQt5QuickTest.so.5*
%{_qt5_plugindir}/accessible/libqtaccessiblequick.so
%{_qt5_plugindir}/qmltooling/
%{_qt5_archdatadir}/qml/

%files devel
%{_bindir}/qml*
%{_qt5_bindir}/qml*
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5Qml.so
%{_qt5_libdir}/libQt5Qml.prl
%{_qt5_libdir}/libQt5Quick*.so
%{_qt5_libdir}/libQt5Quick*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files static
%{_qt5_libdir}/libQt5QmlDevTools.*a
%{_qt5_libdir}/libQt5QmlDevTools.prl


%changelog
* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- qt5-qtjsbackend only supports ix86, x86_64 and arm

* Tue May 14 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- fix qmlprofiler conflict with qt-creator

* Fri Apr 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- fix qmlplugindump conflict with qt4-devel
- include license files, dist/changes*

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

