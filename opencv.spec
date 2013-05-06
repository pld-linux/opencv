#
# TODO:
# - Smartek GigEVisionSDK (http://www.smartekvision.com/ but I can't see SDK with Linux library?)
# - CUDA support (on bcond)
# - ipp (libippi): http://software.intel.com/en-us/articles/intel-ipp/ (proprietary)
#
# Conditional build:
# - general options:
%bcond_with	tbb		# Threading Building Blocks support (everywhere)
%bcond_with	sse		# use SSE instructions
%bcond_with	sse2		# use SSE2 instructions
%bcond_without	opencl		# OpenCL support
%bcond_with	opencl_amdblas	# AMD OpenCL BLAS routines
%bcond_with	opencl_amdfft	# AMD OpenCL FFT routines
%bcond_without	opengl		# OpenGL support
# - highgui options:
%bcond_without	ffmpeg		# FFMpeg support in highgui
%bcond_without	gstreamer	# GStreamer support in highgui
%bcond_with	openni		# OpenNI (Natural Interaction) support in highgui
%bcond_with	pvapi		# PvAPI (AVT GigE cameras) support in highgui (proprietary)
%bcond_with	qt		# Qt backend instead of GTK+ in highgui
%bcond_with	unicap		# Unicap support in highgui (GPL)
%bcond_with	v4l		# Video4Linux in highgui (even V4L2 support currently relies on V4L1 API)
%bcond_with	ximea		# m3API (XIMEA cameras) support in highgui (proprietary)
%bcond_with	xine		# XINE support in highgui (GPL)
#
%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664}
%define		with_sse2	1
%endif
Summary:	A library of programming functions mainly aimed at real time computer vision
Summary(pl.UTF-8):	Biblioteka funkcji do grafiki komputerowej w czasie rzeczywistym
Name:		opencv
Version:	2.4.5
Release:	1
Epoch:		1
%if %{with unicap} || %{with xine}
License:	GPL (enforced by used libraries), BSD (opencv itself)
%else
License:	BSD
%endif
Group:		Libraries
Source0:	http://downloads.sourceforge.net/opencvlibrary/opencv-unix/%{version}/opencv-%{version}.tar.gz
# Source0-md5:	8eac87462c7bec8b89021b723207c623
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-unicap-c++.patch
Patch3:		%{name}-c.patch
Patch4:		%{name}-gcc.patch
Patch5:		%{name}-ximea.patch
Patch6:		%{name}-ocl-fft.patch
URL:		http://opencv.willowgarage.com/
%{?with_pvapi:BuildRequires:	AVT_GigE_SDK-devel}
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	OpenEXR-devel
%{?with_opengl:BuildRequires:	OpenGL-devel}
%{?with_opengl:BuildRequires:	OpenGL-GLU-devel}
# as of OpenCV 2.3.1-2.4.3 there is also check for OpenNI-sensor-PrimeSense, but the result is not used
%{?with_openni:BuildRequires:	OpenNI-devel}
%{?with_ximea:BuildRequires:	XIMEA-devel}
%{?with_opencl_amdblas:BuildRequires:	clAmdBlas-devel}
%{?with_opencl_amdfft:BuildRequires:	clAmdFft-devel}
BuildRequires:	cmake >= 2.4
BuildRequires:	doxygen
BuildRequires:	eigen3 >= 3
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.7}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
%endif
BuildRequires:	jasper-devel
BuildRequires:	libdc1394-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libraw1394-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
%if %{with unicap}
BuildRequires:	libucil-devel
BuildRequires:	libunicap-devel
%endif
BuildRequires:	libv4l-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-numpy-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.606
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
%{?with_tbb:BuildRequires:	tbb-devel}
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRequires:	zlib-devel
%if %{with qt}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
%{?with_opengl:BuildRequires:	QtOpenGL-devel >= 4}
BuildRequires:	qt4-qmake >= 4
%else
BuildRequires:	gtk+2-devel >= 2.0
%{?with_opengl:BuildRequires:	gtkglext-devel >= 1.0}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q

%undos CMakeLists.txt
%undos modules/gpu/CMakeLists.txt

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
install -d build
cd build
%cmake .. \
	-DENABLE_SSE=%{?with_sse:ON}%{!?with_sse:OFF} \
	-DENABLE_SSE2=%{?with_sse2:ON}%{!?with_sse2:OFF} \
	-DBUILD_NEW_PYTHON_SUPPORT=ON \
	-DUSE_O3=OFF \
	%{?with_ffmpeg:-DWITH_FFMPEG=ON} \
	%{!?with_gstreamer:-DWITH_GSTREAMER=OFF} \
	%{?with_opencl:-DWITH_OPENCL=ON} \
	%{?with_opencl_amdblas:-DWITH_OPENCLAMDBLAS=ON} \
	%{?with_opencl_amdfft:-DWITH_OPENCLAMDFFT=ON} \
	%{?with_opengl:-DWITH_OPENGL=ON} \
	%{?with_openni:-DWITH_OPENNI=ON} \
	%{?with_pvapi:-DPVAPI_LIBRARY=%{_libdir}/libPvAPI.so}%{!?with_pvapi:-DWITH_PVAPI=OFF} \
	%{?with_qt:-DWITH_QT=ON %{?with_opengl:-DWITH_QT_OPENGL=ON} -DQT_QMAKE_EXECUTABLE=/usr/bin/qmake-qt4} \
	%{?with_tbb:-DWITH_TBB=ON} \
	%{?with_unicap:-DWITH_UNICAP=ON} \
	%{!?with_v4l:-DWITH_V4L=OFF} \
	%{?with_ximea:-DWITH_XIMEA=ON} \
	%{?with_xine:-DWITH_XINE=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
install build/unix-install/opencv.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opencv_*
%attr(755,root,root) %{_libdir}/libopencv_*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_*.so.2.4
%dir %{_datadir}/OpenCV
%doc %{_datadir}/OpenCV/doc
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_*.so
%{_includedir}/opencv
%{_includedir}/opencv2
%{_datadir}/OpenCV/OpenCVConfig*.cmake
%{_pkgconfigdir}/opencv.pc

%files -n python-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cv2.so
%{py_sitedir}/cv.py[co]
