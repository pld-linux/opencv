#
# TODO: re-enable static libs
#
%bcond_with	xine
Summary:	A library of programming functions mainly aimed at real time computer vision
Name:		opencv
Version:	2.1.0
Release:	2
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opencvlibrary/OpenCV-%{version}.tar.bz2
# Source0-md5:	1d71584fb4e04214c0085108f95e24c8
Patch0:		%{name}-2.0.0-libpng14.patch
Patch1:		%{name}-2.1.0-mmap.patch
Patch2:		%{name}-2.1.0-multilib.patch
Patch3:		%{name}-cflags.patch
URL:		http://opencv.willowgarage.com
BuildRequires:	cmake
BuildRequires:	ffmpeg-devel
BuildRequires:	jasper-devel
BuildRequires:	libdc1394-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libraw1394-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
BuildRequires:	zlib-devel
%pyrequires_eq	python-libs
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libhighgui.so.%{version}

%description
OpenCV (Open Source Computer Vision) is a library of programming
functions mainly aimed at real time computer vision.

Example applications of the OpenCV library are Human-Computer
Interaction (HCI); Object Identification, Segmentation and
Recognition; Face Recognition; Gesture Recognition; Motion Tracking,
Ego Motion, Motion Understanding; Structure From Motion (SFM); Stereo
and Multi-Camera Calibration and Depth Computation; Mobile Robotics.

%package devel
Summary:	Header files and develpment documentation for opencv
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and opencv documentation.

%package static
Summary:	Static opencv library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains the static library used for development.

%package -n python-opencv
Summary:	OpenCV Python bindings
Group:		Development/Languages/Python
%pyrequires_eq  python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-opencv
OpenCV Python bindings.

%prep
%setup -q -n OpenCV-%{version}

%undos src/ml/CMakeLists.txt
%undos CMakeLists.txt
%undos src/cv/CMakeLists.txt
%undos src/cxcore/CMakeLists.txt

%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%ifarch i686 pentium4 athlon %{x8664}
	-DENABLE_SSE2=ON \
%endif
	-DBUILD_NEW_PYTHON_SUPPORT=ON \
%if %{with xine}
	-DWITH_XINE=ON \
%endif
	-DWITH_GSTREAMER=OFF \
	-DWITH_1394=ON \
	-DWITH_FFMPEG=ON \
	-DWITH_GTK=ON \
	-DWITH_V4L=ON \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make} \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
install build/unix-install/opencv.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.2.1
%dir %{_datadir}/opencv
%{_datadir}/opencv/doc
%{_datadir}/opencv/haarcascades
%{_datadir}/opencv/lbpcascades

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/opencv
%{_datadir}/opencv/OpenCVConfig.cmake
%{_pkgconfigdir}/*.pc

#%files static
#%defattr(644,root,root,755)
#%{_libdir}/lib*.a

%files -n python-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cv.so
