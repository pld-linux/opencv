# TODO:
# - Smartek GigEVisionSDK (http://www.smartekvision.com/ but I can't see SDK with Linux library?)
# - CUDA, CUFFT, CUBLAS, NVCUVID support (on bcond)
# - ipp (libippi): http://software.intel.com/en-us/articles/intel-ipp/ (proprietary)
#
# Conditional build:
# - general options:
%bcond_with	tbb		# Threading Building Blocks support (everywhere)
%bcond_with	sse		# use SSE instructions
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions
%bcond_with	ssse3		# use SSSE3 instructions
%bcond_with	sse41		# use SSE4.1 instructions
%bcond_with	sse42		# use SSE4.2 instructions
%bcond_with	avx		# use AVX instructions
%bcond_without	opencl		# OpenCL support
%bcond_with	opencl_amdblas	# AMD OpenCL BLAS routines
%bcond_with	opencl_amdfft	# AMD OpenCL FFT routines
%bcond_without	opengl		# OpenGL support
%bcond_without	gomp		# OpenMP support (available when not using tbb)
%bcond_without	examples	# Install examples
# - bindings
%bcond_without	java		# Java binding
# - highgui options:
%bcond_without	ffmpeg		# FFMpeg support in highgui
%bcond_without	gstreamer	# GStreamer support in highgui
%bcond_with	openni		# OpenNI (Natural Interaction) support in highgui
%bcond_with	pvapi		# PvAPI (AVT GigE cameras) support in highgui (proprietary)
%bcond_with	qt		# Qt backend instead of GTK+ in highgui
%bcond_with	unicap		# Unicap support in highgui (GPL)
%bcond_without	v4l		# Video4Linux in highgui
%bcond_with	ximea		# m3API (XIMEA cameras) support in highgui (proprietary)
%bcond_with	xine		# XINE support in highgui (GPL)
# - other modules
%bcond_without	vtk		# VTK library support (opencv_viz module)

%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664}
%define		with_sse2	1
%endif
Summary:	A library of programming functions mainly aimed at real time computer vision
Summary(pl.UTF-8):	Biblioteka funkcji do grafiki komputerowej w czasie rzeczywistym
Name:		opencv
Version:	2.4.10.1
Release:	1
Epoch:		1
%if %{with unicap} || %{with xine}
License:	GPL (enforced by used libraries), BSD (opencv itself)
%else
License:	BSD
%endif
Group:		Libraries
Source0:	https://github.com/Itseez/opencv/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f84af999f45edc829bfda60a13fedbaa
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-x86.patch
Patch2:		%{name}-unicap-c++.patch
Patch3:		%{name}-c.patch
Patch4:		%{name}-gcc.patch
Patch5:		%{name}-ximea.patch
Patch6:		%{name}-ocl-fft.patch
Patch7:		java-ant-sourcelevel.patch
Patch8:		%{name}-shared.patch
Patch9:		no-sysctl.patch
URL:		http://www.opencv.org/
%{?with_pvapi:BuildRequires:	AVT_GigE_SDK-devel}
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	OpenEXR-devel
%{?with_opengl:BuildRequires:	OpenGL-GLU-devel}
%{?with_opengl:BuildRequires:	OpenGL-devel}
# as of OpenCV 2.3.1-2.4.3 there is also check for OpenNI-sensor-PrimeSense, but the result is not used
%{?with_openni:BuildRequires:	OpenNI-devel}
%{?with_ximea:BuildRequires:	XIMEA-devel >= 4}
%{?with_java:BuildRequires:	ant}
%{?with_opencl_amdblas:BuildRequires:	clAmdBlas-devel}
%{?with_opencl_amdfft:BuildRequires:	clAmdFft-devel}
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen
BuildRequires:	eigen3 >= 3
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.7}
%{?with_gomp:BuildRequires:	gcc-c++ >= 6:4.2}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
BuildRequires:	jasper-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libdc1394-devel >= 2
%{?with_gomp:BuildRequires:	libgomp-devel}
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
BuildRequires:	python >= 2.0
BuildRequires:	python-devel >= 2.0
BuildRequires:	python-numpy-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.606
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg
BuildRequires:	swig-python
%{?with_tbb:BuildRequires:	tbb-devel}
%if %{with vtk}
BuildRequires:	vtk-devel >= 5.8.0
BuildRequires:	vtk-java >= 5.8.0
BuildRequires:	vtk-tcl >= 5.8.0
%endif
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRequires:	xorg-lib-libX11-devel
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
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		jver	%(echo %{version} | cut -d. -f1-3 | tr -d .)

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

%package core
Summary:	OpenCV core libraries
Summary(pl.UTF-8):	Podstawowe biblioteki OpenCV
Group:		Libraries
Conflicts:	opencv < 2.4.6.2-1

%description core
This package contains the OpenCV C/C++ core libraries.

%description core -l pl.UTF-8
Ten pakiet zawiera podstawowe biblioteki C/C++ OpenCV.

%package viz
Summary:	OpenCV viz library (VTK support)
Summary(pl.UTF-8):	Biblioteka OpenCV viz (obsługa VTK)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description viz
OpenCV viz library (VTK support).

%description viz -l pl.UTF-8
Biblioteka OpenCV viz (obsługa VTK).

%package devel
Summary:	Header files for OpenCV library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenCV
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%if %{with vtk}
Requires:	%{name}-viz = %{epoch}:%{version}-%{release}
%endif
Obsoletes:	opencv-static

%description devel
Header files for OpenCV library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenCV.

%package doc
Summary:	Manual for OpenCV
Summary(fr.UTF-8):	Documentation pour OpenCV
Summary(it.UTF-8):	Documentazione di OpenCV
Summary(pl.UTF-8):	Podręcznik dla OpenCV
Group:		Documentation
# noarch subpackages only when building with rpm5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for OpenCV.

%description doc -l fr.UTF-8
Documentation pour OpenCV.

%description doc -l it.UTF-8
Documentazione di OpenCV.

%description doc -l pl.UTF-8
Dokumentacja do OpenCV.

%package examples
Summary:	OpenCV code examples
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
OpenCV code examples.

%package -n java-opencv
Summary:	OpenCV Java bindings
Summary(pl.UTF-8):	Wiązania Javy do OpenCV
Group:		Libraries/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	jre

%description -n java-opencv
OpenCV Java bindings.

%description -n java-opencv -l pl.UTF-8
Wiązania Javy do OpenCV.

%package -n python-opencv
Summary:	OpenCV Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do OpenCV
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-libs

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
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
install -d build
cd build

# handle cmake & ccache
# http://stackoverflow.com/questions/1815688/how-to-use-ccache-with-cmakec
if [[ "%{__cc}" = *ccache* ]]; then
	cc="%{__cc}"
	cxx="%{__cxx}"
	ccache="
	-DCMAKE_C_COMPILER="ccache" -DCMAKE_C_COMPILER_ARG1="${cc#ccache }" \
	-DCMAKE_CXX_COMPILER="ccache" -DCMAKE_CXX_COMPILER_ARG1="${cxx#ccache }" \
	"
fi

%cmake .. \
	$ccache \
	-DENABLE_AVX=%{?with_avx:ON}%{!?with_avx:OFF} \
	-DENABLE_SSE=%{?with_sse:ON}%{!?with_sse:OFF} \
	-DENABLE_SSE2=%{?with_sse2:ON}%{!?with_sse2:OFF} \
	-DENABLE_SSE3=%{?with_sse3:ON}%{!?with_sse3:OFF} \
	-DENABLE_SSSE3=%{?with_ssse3:ON}%{!?with_ssse3:OFF} \
	-DENABLE_SSE41=%{?with_sse41:ON}%{!?with_sse41:OFF} \
	-DENABLE_SSE42=%{?with_sse42:ON}%{!?with_sse42:OFF} \
	-DBUILD_NEW_PYTHON_SUPPORT=ON \
%if %{with examples}
	-DINSTALL_C_EXAMPLES=ON \
	-DINSTALL_PYTHON_EXAMPLES=ON \
%endif
	%{?with_ffmpeg:-DWITH_FFMPEG=ON} \
	%{!?with_gstreamer:-DWITH_GSTREAMER=OFF} \
	%{?with_opencl:-DWITH_OPENCL=ON} \
	%{!?with_opencl_amdblas:-DWITH_OPENCLAMDBLAS=OFF} \
	%{!?with_opencl_amdfft:-DWITH_OPENCLAMDFFT=OFF} \
	%{?with_opengl:-DWITH_OPENGL=ON} \
	%{?with_gomp:-DWITH_OPENMP=ON} \
	%{?with_openni:-DWITH_OPENNI=ON} \
	%{?with_pvapi:-DPVAPI_LIBRARY=%{_libdir}/libPvAPI.so}%{!?with_pvapi:-DWITH_PVAPI=OFF} \
	%{?with_qt:-DWITH_QT=ON %{?with_opengl:-DWITH_QT_OPENGL=ON} -DQT_QMAKE_EXECUTABLE=/usr/bin/qmake-qt4} \
	%{?with_tbb:-DWITH_TBB=ON} \
	%{?with_unicap:-DWITH_UNICAP=ON} \
	%{!?with_v4l:-DWITH_V4L=OFF} \
	%{?with_vtk:-DWITH_VTK=ON} \
	%{?with_ximea:-DWITH_XIMEA=ON} \
	%{?with_xine:-DWITH_XINE=ON}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# see -doc package
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/OpenCV/doc
%if %{with examples}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -p build/unix-install/opencv.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d' $RPM_BUILD_ROOT%{_datadir}/OpenCV/OpenCVModules.cmake

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%if %{with java}
# move to proper directories, create symlink
install -d $RPM_BUILD_ROOT%{_javadir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/OpenCV/java/libopencv_java*.so $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's#/share/OpenCV/java/libopencv_java%{jver}\.so#/%{_lib}/libopencv_java%{jver}.so#g' \
	$RPM_BUILD_ROOT%{_datadir}/OpenCV/OpenCVModules-pld.cmake
%{__mv} $RPM_BUILD_ROOT%{_datadir}/OpenCV/java/opencv-*.jar $RPM_BUILD_ROOT%{_javadir}
rmdir $RPM_BUILD_ROOT%{_datadir}/OpenCV/java
ln -sf $(basename $RPM_BUILD_ROOT%{_javadir}/opencv-*.jar) $RPM_BUILD_ROOT%{_javadir}/opencv.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post   viz -p /sbin/ldconfig
%postun viz -p /sbin/ldconfig

%post   -n java-opencv -p /sbin/ldconfig
%postun -n java-opencv -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opencv_createsamples
%attr(755,root,root) %{_bindir}/opencv_haartraining
%attr(755,root,root) %{_bindir}/opencv_performance
%attr(755,root,root) %{_bindir}/opencv_traincascade
%attr(755,root,root) %{_libdir}/libopencv_calib3d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_calib3d.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_contrib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_contrib.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_features2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_features2d.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_gpu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_gpu.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_highgui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_highgui.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_legacy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_legacy.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_nonfree.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_nonfree.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_objdetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_objdetect.so.2.4
%if %{with opencl}
%attr(755,root,root) %{_libdir}/libopencv_ocl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ocl.so.2.4
%endif
%attr(755,root,root) %{_libdir}/libopencv_stitching.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_stitching.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_superres.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_superres.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_ts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ts.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_videostab.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_videostab.so.2.4
%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files core
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_core.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_flann.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_flann.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_imgproc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_imgproc.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_ml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ml.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_photo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_photo.so.2.4
%attr(755,root,root) %{_libdir}/libopencv_video.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_video.so.2.4

%if %{with vtk}
%files viz
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_viz.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_viz.so.2.4
%endif

%files devel
%defattr(644,root,root,755)
# core
%attr(755,root,root) %{_libdir}/libopencv_core.so
%attr(755,root,root) %{_libdir}/libopencv_flann.so
%attr(755,root,root) %{_libdir}/libopencv_imgproc.so
%attr(755,root,root) %{_libdir}/libopencv_ml.so
%attr(755,root,root) %{_libdir}/libopencv_photo.so
%attr(755,root,root) %{_libdir}/libopencv_video.so
# GUI/extensions (base package)
%attr(755,root,root) %{_libdir}/libopencv_calib3d.so
%attr(755,root,root) %{_libdir}/libopencv_contrib.so
%attr(755,root,root) %{_libdir}/libopencv_features2d.so
%attr(755,root,root) %{_libdir}/libopencv_gpu.so
%attr(755,root,root) %{_libdir}/libopencv_highgui.so
%attr(755,root,root) %{_libdir}/libopencv_legacy.so
%attr(755,root,root) %{_libdir}/libopencv_nonfree.so
%attr(755,root,root) %{_libdir}/libopencv_objdetect.so
%if %{with opencl}
%attr(755,root,root) %{_libdir}/libopencv_ocl.so
%endif
%attr(755,root,root) %{_libdir}/libopencv_stitching.so
%attr(755,root,root) %{_libdir}/libopencv_superres.so
%attr(755,root,root) %{_libdir}/libopencv_ts.so
%attr(755,root,root) %{_libdir}/libopencv_videostab.so
# viz
%if %{with vtk}
%attr(755,root,root) %{_libdir}/libopencv_viz.so
%endif
%{_includedir}/opencv
%{_includedir}/opencv2
%{_datadir}/OpenCV/OpenCV*.cmake
%{_pkgconfigdir}/opencv.pc

%files doc
%defattr(644,root,root,755)
# TODO: probably could rebuild them and package via make install
%doc doc/*

%if %{with examples}
%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with java}
%files -n java-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_java%{jver}.so
%{_javadir}/opencv-%{jver}.jar
%{_javadir}/opencv.jar
%endif

%files -n python-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cv2.so
%{py_sitedir}/cv.py[co]
