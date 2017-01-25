# TODO:
# - contrib subpackage(s)
# - contrib BRs:
#   opencv_contrib-3.1.0/modules/cnn_3dobj/CMakeLists.txt:find_package(Caffe)
#   opencv_contrib-3.1.0/modules/cnn_3dobj/CMakeLists.txt:find_package(Protobuf)
#   opencv_contrib-3.1.0/modules/cnn_3dobj/CMakeLists.txt:find_package(Glog)
#   opencv_contrib-3.1.0/modules/hdf/CMakeLists.txt:find_package(HDF5)
#   opencv_contrib-3.1.0/modules/sfm/CMakeLists.txt:find_package(Ceres QUIET)
#   opencv_contrib-3.1.0/modules/text/CMakeLists.txt:find_package(Tesseract)
#
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
%bcond_without	openmp		# OpenMP support (available when not using tbb)
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

%ifarch pentium3 pentium4 %{x8664} x32
%define		with_sse	1
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif
Summary:	A library of programming functions mainly aimed at real time computer vision
Summary(pl.UTF-8):	Biblioteka funkcji do grafiki komputerowej w czasie rzeczywistym
Name:		opencv
Version:	3.1.0
Release:	4
Epoch:		1
%if %{with unicap} || %{with xine}
License:	GPL (enforced by used libraries), BSD (opencv itself)
%else
License:	BSD
%endif
Group:		Libraries
Source0:	https://github.com/Itseez/opencv/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	70e1dd07f0aa06606f1bc0e3fa15abd3
Source1:	https://github.com/Itseez/opencv_contrib/archive/%{version}/%{name}_contrib-%{version}.tar.gz
# Source1-md5:	a822839ad3ab79ff837c16785ea9dd10
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-ximea.patch
Patch2:		java-ant-sourcelevel.patch
Patch3:		cmake-install-path.patch
Patch4:		vtk7.patch
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
%{?with_openmp:BuildRequires:	gcc-c++ >= 6:4.2}
BuildRequires:	gflags-devel
BuildRequires:	gl2ps-devel
BuildRequires:	glog-devel
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
BuildRequires:	jasper-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libdc1394-devel >= 2
%{?with_openmp:BuildRequires:	libgomp-devel}
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
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
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
%define		sover	%(echo %{version} | cut -d. -f1-2)

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
Summary:	OpenCV Python 2 bindings
Summary(pl.UTF-8):	Wiązania Pythona 2 do OpenCV
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-libs

%description -n python-opencv
OpenCV Python 2 bindings.

%description -n python-opencv -l pl.UTF-8
Wiązania Pythona 2 do OpenCV.

%package -n python3-opencv
Summary:	OpenCV Python 3 bindings
Summary(pl.UTF-8):	Wiązania Pythona 3 do OpenCV
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3-libs

%description -n python3-opencv
OpenCV Python 3 bindings.

%description -n python3-opencv -l pl.UTF-8
Wiązania Pythona 3 do OpenCV.

%prep
%setup -q -a1

%undos CMakeLists.txt

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
	-DENABLE_PRECOMPILED_HEADERS=OFF \
	-DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
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
	%{?with_openmp:-DWITH_OPENMP=ON} \
	%{?with_openni:-DWITH_OPENNI=ON} \
	%{?with_pvapi:-DPVAPI_LIBRARY=%{_libdir}/libPvAPI.so}%{!?with_pvapi:-DWITH_PVAPI=OFF} \
	%{?with_qt:-DWITH_QT=ON %{?with_opengl:-DWITH_QT_OPENGL=ON} -DQT_QMAKE_EXECUTABLE=/usr/bin/qmake-qt4} \
	%{?with_tbb:-DWITH_TBB=ON} \
	%{?with_unicap:-DWITH_UNICAP=ON} \
	%{!?with_v4l:-DWITH_V4L=OFF} \
	%{?with_vtk:-DWITH_VTK=ON} \
	%{?with_ximea:-DWITH_XIMEA=ON} \
	%{?with_xine:-DWITH_XINE=ON} \
	-DWITH_IPP=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_bindir}/opencv_annotation
%attr(755,root,root) %{_bindir}/opencv_createsamples
%attr(755,root,root) %{_bindir}/opencv_traincascade
%attr(755,root,root) %{_libdir}/libopencv_calib3d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_calib3d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_features2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_features2d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_highgui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_highgui.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_objdetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_objdetect.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_stitching.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_stitching.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_superres.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_superres.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_videostab.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_videostab.so.%{sover}
# contrib modules
%attr(755,root,root) %{_bindir}/opencv_waldboost_detector
%attr(755,root,root) %ghost %{_libdir}/libopencv_aruco.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_aruco.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_bgsegm.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_bgsegm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_bioinspired.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_bioinspired.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ccalib.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ccalib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_datasets.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_datasets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dnn.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dnn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dpm.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_face.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_face.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_fuzzy.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_fuzzy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_hdf.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_hdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_line_descriptor.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_line_descriptor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_optflow.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_optflow.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_plot.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_plot.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_reg.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_reg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_rgbd.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_rgbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_saliency.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_saliency.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_sfm.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_sfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_stereo.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_stereo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_structured_light.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_structured_light.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_surface_matching.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_surface_matching.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_text.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_text.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_tracking.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_tracking.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xfeatures2d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xfeatures2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ximgproc.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ximgproc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xobjdetect.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xobjdetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xphoto.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xphoto.so.*.*.*
%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files core
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_core.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_flann.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_flann.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_imgproc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_imgproc.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ml.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_photo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_photo.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_video.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_video.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_imgcodecs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_imgcodecs.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_shape.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_shape.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_videoio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_videoio.so.%{sover}

%if %{with vtk}
%files viz
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_viz.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_viz.so.%{sover}
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
%attr(755,root,root) %{_libdir}/libopencv_features2d.so
%attr(755,root,root) %{_libdir}/libopencv_highgui.so
%attr(755,root,root) %{_libdir}/libopencv_objdetect.so
%attr(755,root,root) %{_libdir}/libopencv_stitching.so
%attr(755,root,root) %{_libdir}/libopencv_superres.so
%attr(755,root,root) %{_libdir}/libopencv_videostab.so
%attr(755,root,root) %{_libdir}/libopencv_imgcodecs.so
%attr(755,root,root) %{_libdir}/libopencv_shape.so
%attr(755,root,root) %{_libdir}/libopencv_videoio.so
# contrib
%attr(755,root,root) %{_libdir}/libopencv_aruco.so
%attr(755,root,root) %{_libdir}/libopencv_bgsegm.so
%attr(755,root,root) %{_libdir}/libopencv_bioinspired.so
%attr(755,root,root) %{_libdir}/libopencv_ccalib.so
%attr(755,root,root) %{_libdir}/libopencv_datasets.so
%attr(755,root,root) %{_libdir}/libopencv_dnn.so
%attr(755,root,root) %{_libdir}/libopencv_dpm.so
%attr(755,root,root) %{_libdir}/libopencv_face.so
%attr(755,root,root) %{_libdir}/libopencv_fuzzy.so
%attr(755,root,root) %{_libdir}/libopencv_hdf.so
%attr(755,root,root) %{_libdir}/libopencv_line_descriptor.so
%attr(755,root,root) %{_libdir}/libopencv_optflow.so
%attr(755,root,root) %{_libdir}/libopencv_plot.so
%attr(755,root,root) %{_libdir}/libopencv_reg.so
%attr(755,root,root) %{_libdir}/libopencv_rgbd.so
%attr(755,root,root) %{_libdir}/libopencv_saliency.so
%attr(755,root,root) %{_libdir}/libopencv_sfm.so
%attr(755,root,root) %{_libdir}/libopencv_stereo.so
%attr(755,root,root) %{_libdir}/libopencv_structured_light.so
%attr(755,root,root) %{_libdir}/libopencv_surface_matching.so
%attr(755,root,root) %{_libdir}/libopencv_text.so
%attr(755,root,root) %{_libdir}/libopencv_tracking.so
%attr(755,root,root) %{_libdir}/libopencv_xfeatures2d.so
%attr(755,root,root) %{_libdir}/libopencv_ximgproc.so
%attr(755,root,root) %{_libdir}/libopencv_xobjdetect.so
%attr(755,root,root) %{_libdir}/libopencv_xphoto.so
%{_libdir}/libopencv_ts.a
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

%files -n python3-opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/cv2.cpython-*.so
