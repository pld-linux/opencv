#
# Conditional build:
%bcond_with	gstreamer	# GStreamer support
%bcond_with	xine		# XINE support (GPL)
#
Summary:	A library of programming functions mainly aimed at real time computer vision
Summary(pl.UTF-8):	Biblioteka funkcji do grafiki komputerowej w czasie rzeczywistym
Name:		opencv
Version:	2.2.0
Release:	6
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opencvlibrary/OpenCV-%{version}.tar.bz2
# Source0-md5:	122c9ac793a46854ef2819fedbbd6b1b
Patch0:		%{name}-multilib.patch
Patch1:		%{name}-cflags.patch
Patch2:		%{name}-link.patch
URL:		http://opencv.willowgarage.com/
BuildRequires:	OpenEXR-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	doxygen
BuildRequires:	ffmpeg-devel
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
%endif
BuildRequires:	jasper-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libdc1394-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libraw1394-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libv4l-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-numpy-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
BuildRequires:	zlib-devel
%{?with_xine:BuildRequires:	xine-lib-devel}
# TODO:
# - unicap (libunicap, libucil)
# - gstreamer
# - pvapi (PvApi.h)
# - Qt (bcond replacing GTK+?)
# - tbb (tbb.pc)
# - cuda (on bcond)
# - eigen2/eigen3 (Eigen/Core headers)
# - ipp (libippi)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libhighgui.so.%{version}

%description
OpenCV (Open Source Computer Vision) is a library of programming
functions mainly aimed at real time computer vision.

Example applications of the OpenCV library are:
- Human-Computer Interaction (HCI)
- Object Identification, Segmentation and Recognition
- Face Recognition
- Gesture Recognition
- Motion Tracking
- Ego Motion, Motion Understanding
- Structure From Motion (SFM)
- Stereo and Multi-Camera Calibration and Depth Computation
- Mobile Robotics.

%description -l pl.UTF-8
OpenCV (Open Source Computer Vision) to biblioteka funkcji
przeznaczonych głównie do grafiki komputerowej w czasie rzeczywistym.

Przykładowe zastosowania biblioteki OpenCV to
- interakcje człowiek-komputer (HCI)
- identyfikacja, segmentacja i rozpoznawanie obiektów
- rozpoznawanie twarzy
- rozpoznawanie gestów
- śledzenie ruchu
- rozumienie ruchu
- SFM (Structure From Motion)
- kalibracja dwu- i wielokamerowa, obliczanie głębi
- robotyka ruchu.

%package devel
Summary:	Header files for OpenCV library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenCV
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	opencv-static

%description devel
Header files for OpenCV library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenCV.

%package -n python-opencv
Summary:	OpenCV Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do OpenCV
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-opencv
OpenCV Python bindings.

%description -n python-opencv -l pl.UTF-8
Wiązania Pythona do OpenCV.

%prep
%setup -q -n OpenCV-%{version}

%undos CMakeLists.txt
%undos modules/gpu/CMakeLists.txt

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
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
	-DWITH_V4L=ON

%{__make} \
	VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
install build/unix-install/opencv.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%if "%{_lib}" == "lib64"
# upstream has no lib64 support
mv $RPM_BUILD_ROOT%{_prefix}/lib/lib*.so* $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opencv_*
%attr(755,root,root) %{_libdir}/libopencv_*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_*.so.2.2
%dir %{_datadir}/opencv
%doc %{_datadir}/opencv/doc
%{_datadir}/opencv/haarcascades
%{_datadir}/opencv/lbpcascades

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_*.so
%{_includedir}/opencv
%{_includedir}/opencv2
%{_datadir}/opencv/OpenCVConfig.cmake
%{_pkgconfigdir}/opencv.pc

%files -n python-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cv.so
