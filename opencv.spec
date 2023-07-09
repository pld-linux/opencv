# TODO:
# - contrib subpackage(s)
# - contrib BRs:
#   opencv_contrib-3.1.0/modules/cnn_3dobj/CMakeLists.txt:find_package(Caffe)
#   opencv_contrib-3.1.0/modules/sfm/CMakeLists.txt:find_package(Ceres QUIET)
# unpackaged (4.5.5)
#/usr/share/OpenCV/3rdparty/usr/lib64/libcorrespondence.a
#/usr/share/OpenCV/3rdparty/usr/lib64/libmultiview.a
#/usr/share/OpenCV/3rdparty/usr/lib64/libnumeric.a
#/usr/share/OpenCV/valgrind.supp
#/usr/share/OpenCV/valgrind_3rdparty.supp

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
Version:	4.5.5
Release:	1
Epoch:		1
%if %{with unicap} || %{with xine}
License:	GPL (enforced by used libraries), BSD (opencv itself)
%else
License:	BSD
%endif
Group:		Libraries
Source0:	https://github.com/Itseez/opencv/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a9782f01883fcf51451a183d05bda33d
Source1:	https://github.com/Itseez/opencv_contrib/archive/%{version}/%{name}_contrib-%{version}.tar.gz
# Source1-md5:	073793e8085ec2490b3386e04ee20fbc
# See opencv_contrib-3.4.1/modules/xfeatures2d/cmake/download_boostdesc.cmake
Source10:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_bgm.i
# Source10-md5:	0ea90e7a8f3f7876d450e4149c97c74f
Source11:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_bgm_bi.i
# Source11-md5:	232c966b13651bd0e46a1497b0852191
Source12:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_bgm_hd.i
# Source12-md5:	324426a24fa56ad9c5b8e3e0b3e5303e
Source13:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_binboost_064.i
# Source13-md5:	202e1b3e9fec871b04da31f7f016679f
Source14:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_binboost_128.i
# Source14-md5:	98ea99d399965c03d555cef3ea502a0b
Source15:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_binboost_256.i
# Source15-md5:	e6dcfa9f647779eb1ce446a8d759b6ea
Source16:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/34e4206aef44d50e6bbcd0ab06354b52e7466d26/boostdesc_lbgm.i
# Source16-md5:	0ae0675534aa318d9668f2a179c2a052
# See opencv_contrib-3.4.1/modules/xfeatures2d/cmake/download_vgg.cmake
Source20:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/fccf7cd6a4b12079f73bbfb21745f9babcd4eb1d/vgg_generated_48.i
# Source20-md5:	e8d0dcd54d1bcfdc29203d011a797179
Source21:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/fccf7cd6a4b12079f73bbfb21745f9babcd4eb1d/vgg_generated_64.i
# Source21-md5:	7126a5d9a8884ebca5aea5d63d677225
Source22:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/fccf7cd6a4b12079f73bbfb21745f9babcd4eb1d/vgg_generated_80.i
# Source22-md5:	7cd47228edec52b6d82f46511af325c5
Source23:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/fccf7cd6a4b12079f73bbfb21745f9babcd4eb1d/vgg_generated_120.i
# Source23-md5:	151805e03568c9f490a5e3a872777b75
# See opencv_contrib-3.4.1/modules/face/CMakeLists.txt
Source30:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/8afa57abc8229d611c4937165d20e2a2d9fc5a12/face_landmark_model.dat
# Source30-md5:	7505c44ca4eb54b4ab1e4777cb96ac05
# See opencv-4.5.1/modules/gapi/cmake/DownloadADE.cmake
Source40:	https://github.com/opencv/ade/archive/v0.1.2a/ade-0.1.2a.zip
# Source40-md5:	fa4b3e25167319cb0fa9432ef8281945
# See opencv_contrib-4.5.5/modules/wechat_qrcode/CMakeLists.txt
Source50:	https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/a8b69ccc738421293254aec5ddb38bd523503252/detect.caffemodel
# Source50-md5:	238e2b2d6f3c18d6c3a30de0c31e23cf
Source51:	https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/a8b69ccc738421293254aec5ddb38bd523503252/detect.prototxt
# Source51-md5:	6fb4976b32695f9f5c6305c19f12537d
Source52:	https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/a8b69ccc738421293254aec5ddb38bd523503252/sr.caffemodel
# Source52-md5:	cbfcd60361a73beb8c583eea7e8e6664
Source53:	https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/a8b69ccc738421293254aec5ddb38bd523503252/sr.prototxt
# Source53-md5:	69db99927a70df953b471daaba03fbef
Patch0:		%{name}-ximea.patch
Patch1:		python-install.patch
Patch2:		pkgconfig-paths.patch
Patch3:		no-cxx-in-c-header.patch
Patch4:		gcc11.patch
Patch5:		%{name}-ade.patch
URL:		http://www.opencv.org/
%{?with_pvapi:BuildRequires:	AVT_GigE_SDK-devel}
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	OpenEXR-devel
%{?with_opengl:BuildRequires:	OpenGL-GLU-devel}
%if %{with opengl}
BuildRequires:	OpenGL-devel
BuildRequires:	libglvnd-libGL-devel
%endif
# as of OpenCV 2.3.1-2.4.3 there is also check for OpenNI-sensor-PrimeSense, but the result is not used
%{?with_openni:BuildRequires:	OpenNI-devel}
%{?with_ximea:BuildRequires:	XIMEA-devel >= 4}
%{?with_java:BuildRequires:	ant}
BuildRequires:	boost-devel
%{?with_opencl_amdblas:BuildRequires:	clAmdBlas-devel}
%{?with_opencl_amdfft:BuildRequires:	clAmdFft-devel}
BuildRequires:	cmake >= 3.5.1
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
%if %{with java}
BuildRequires:	java-xerces
BuildRequires:	jdk
# jawt for installed jdk
BuildRequires:	jre-X11
%endif
BuildRequires:	khrplatform-devel
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
BuildRequires:	ogre-devel
BuildRequires:	pkgconfig
BuildRequires:	hdf5-devel
BuildRequires:	protobuf-devel
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-numpy-devel
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.606
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg
BuildRequires:	swig-python
%{?with_tbb:BuildRequires:	tbb-devel}
BuildRequires:	tesseract-devel
%if %{with vtk}
BuildRequires:	vtk-devel >= 5.8.0
BuildRequires:	vtk-java >= 5.8.0
BuildRequires:	vtk-python3-devel >= 5.8.0
%endif
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel >= 1.2.3
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
%define		sover	405

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
Obsoletes:	opencv-static < 1:2

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
BuildArch:	noarch

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
Summary(pl.UTF-8):	Przykłady kodu OpenCV
Group:		Documentation
BuildArch:	noarch

%description examples
OpenCV code examples.

%description examples -l pl.UTF-8
Przykłady kodu OpenCV.

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
Requires:	python-libs >= 1:2.7

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
%patch5 -p1

cache_file() {
	f="$1"
	d="$2"
	md5="$(md5sum "$f" | awk '{print $1}')"
	file="$(basename "$f")"
	mkdir -p ".cache/$d"
	ln -s --relative "$f" ".cache/$d/$md5-$file"
}
for f in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16}; do
	cache_file $f xfeatures2d/boostdesc
done
for f in %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}; do
	cache_file $f xfeatures2d/vgg
done
cache_file %{SOURCE30} data
cache_file %{SOURCE40} ade
for f in %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53}; do
	cache_file $f wechat_qrcode
done

cd opencv_contrib-%{version}

# both files use Glog_FOUND variable, but set different variables for LIBS; unify them so they won't disturb each other
cp -f modules/sfm/cmake/FindGlog.cmake modules/cnn_3dobj/FindGlog.cmake
%{__sed} -i -e 's/Glog_LIBS/GLOG_LIBRARIES/' modules/cnn_3dobj/CMakeLists.txt

%build
mkdir -p build
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

# WITH_GTK_2_X=ON: force gtk+2 instead of gtk+3
# (as of 4.5.5, OpenGL is not supported with gtk+3, leading to highgui linking errors)
%cmake .. \
	$ccache \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DENABLE_PRECOMPILED_HEADERS=OFF \
	-DOPENCV_LIB_INSTALL_PATH=%{_libdir} \
	-DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
	-DENABLE_AVX=%{?with_avx:ON}%{!?with_avx:OFF} \
	-DENABLE_SSE=%{?with_sse:ON}%{!?with_sse:OFF} \
	-DENABLE_SSE2=%{?with_sse2:ON}%{!?with_sse2:OFF} \
	-DENABLE_SSE3=%{?with_sse3:ON}%{!?with_sse3:OFF} \
	-DENABLE_SSSE3=%{?with_ssse3:ON}%{!?with_ssse3:OFF} \
	-DENABLE_SSE41=%{?with_sse41:ON}%{!?with_sse41:OFF} \
	-DENABLE_SSE42=%{?with_sse42:ON}%{!?with_sse42:OFF} \
	-DBUILD_NEW_PYTHON_SUPPORT=ON \
	-DOPENCV_GENERATE_PKGCONFIG:BOOL=ON \
%if %{with examples}
	-DINSTALL_C_EXAMPLES=ON \
	-DINSTALL_PYTHON_EXAMPLES=ON \
%endif
	%{?with_ffmpeg:-DWITH_FFMPEG=ON} \
	%{!?with_gstreamer:-DWITH_GSTREAMER=OFF} \
	-DWITH_GTK_2_X=ON \
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
mv $RPM_BUILD_ROOT%{_datadir}/opencv4/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d' $RPM_BUILD_ROOT%{_libdir}/cmake/opencv4/OpenCVModules.cmake

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%if %{with java}
# move to proper directories, create symlink
install -d $RPM_BUILD_ROOT%{_javadir}
%{__mv} $RPM_BUILD_ROOT%{_javadir}/opencv4/libopencv_java*.so $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's#/share/java/opencv4/libopencv_java%{jver}\.so#/%{_lib}/libopencv_java%{jver}.so#g' \
	$RPM_BUILD_ROOT%{_libdir}/cmake/opencv4/OpenCVModules-pld.cmake
%{__mv} $RPM_BUILD_ROOT%{_javadir}/opencv4/opencv-*.jar $RPM_BUILD_ROOT%{_javadir}
rmdir $RPM_BUILD_ROOT%{_javadir}/opencv4
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
%attr(755,root,root) %{_bindir}/opencv_interactive-calibration
%attr(755,root,root) %{_bindir}/opencv_model_diagnostics
%attr(755,root,root) %{_bindir}/opencv_version
%attr(755,root,root) %{_bindir}/opencv_visualisation
%attr(755,root,root) %{_bindir}/setup_vars_opencv4.sh
%attr(755,root,root) %{_libdir}/libopencv_calib3d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_calib3d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dnn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dnn.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_features2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_features2d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_gapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_gapi.so.%{sover}
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
%attr(755,root,root) %ghost %{_libdir}/libopencv_alphamat.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_alphamat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_aruco.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_aruco.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_barcode.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_barcode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_bgsegm.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_bgsegm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_bioinspired.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_bioinspired.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ccalib.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ccalib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_datasets.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_datasets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dnn_objdetect.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dnn_objdetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dnn_superres.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dnn_superres.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_dpm.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_dpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_face.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_face.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_freetype.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_freetype.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_fuzzy.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_fuzzy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_hdf.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_hdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_hfs.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_hfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_img_hash.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_img_hash.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_intensity_transform.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_intensity_transform.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_line_descriptor.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_line_descriptor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_mcc.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_mcc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ovis.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ovis.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_optflow.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_optflow.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_phase_unwrapping.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_phase_unwrapping.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_plot.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_plot.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_quality.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_quality.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_rapid.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_rapid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_reg.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_reg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_rgbd.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_rgbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_saliency.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_saliency.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_shape.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_shape.so.*.*.*
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
%attr(755,root,root) %ghost %{_libdir}/libopencv_wechat_qrcode.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_wechat_qrcode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xfeatures2d.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xfeatures2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ximgproc.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ximgproc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xobjdetect.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xobjdetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_xphoto.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_xphoto.so.*.*.*

%dir %{_datadir}/opencv4
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades
%{_datadir}/opencv4/quality

%files core
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencv_core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_core.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_flann.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_flann.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_imgcodecs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_imgcodecs.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_imgproc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_imgproc.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_ml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_ml.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_photo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_photo.so.%{sover}
%attr(755,root,root) %{_libdir}/libopencv_video.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencv_video.so.%{sover}
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
%{_libdir}/libopencv_core.so
%{_libdir}/libopencv_dnn.so
%{_libdir}/libopencv_flann.so
%{_libdir}/libopencv_imgcodecs.so
%{_libdir}/libopencv_imgproc.so
%{_libdir}/libopencv_ml.so
%{_libdir}/libopencv_photo.so
%{_libdir}/libopencv_video.so
%{_libdir}/libopencv_videoio.so
# GUI/extensions (base package)
%{_libdir}/libopencv_calib3d.so
%{_libdir}/libopencv_features2d.so
%{_libdir}/libopencv_gapi.so
%{_libdir}/libopencv_highgui.so
%{_libdir}/libopencv_objdetect.so
%{_libdir}/libopencv_stitching.so
# contrib
%{_libdir}/libopencv_alphamat.so
%{_libdir}/libopencv_aruco.so
%{_libdir}/libopencv_barcode.so
%{_libdir}/libopencv_bgsegm.so
%{_libdir}/libopencv_bioinspired.so
%{_libdir}/libopencv_ccalib.so
%{_libdir}/libopencv_datasets.so
%{_libdir}/libopencv_dnn_objdetect.so
%{_libdir}/libopencv_dnn_superres.so
%{_libdir}/libopencv_dpm.so
%{_libdir}/libopencv_face.so
%{_libdir}/libopencv_freetype.so
%{_libdir}/libopencv_fuzzy.so
%{_libdir}/libopencv_hdf.so
%{_libdir}/libopencv_hfs.so
%{_libdir}/libopencv_img_hash.so
%{_libdir}/libopencv_intensity_transform.so
%{_libdir}/libopencv_line_descriptor.so
%{_libdir}/libopencv_mcc.so
%{_libdir}/libopencv_optflow.so
%{_libdir}/libopencv_ovis.so
%{_libdir}/libopencv_phase_unwrapping.so
%{_libdir}/libopencv_plot.so
%{_libdir}/libopencv_quality.so
%{_libdir}/libopencv_rapid.so
%{_libdir}/libopencv_reg.so
%{_libdir}/libopencv_rgbd.so
%{_libdir}/libopencv_saliency.so
%{_libdir}/libopencv_sfm.so
%{_libdir}/libopencv_shape.so
%{_libdir}/libopencv_stereo.so
%{_libdir}/libopencv_superres.so
%{_libdir}/libopencv_structured_light.so
%{_libdir}/libopencv_surface_matching.so
%{_libdir}/libopencv_text.so
%{_libdir}/libopencv_tracking.so
%{_libdir}/libopencv_videostab.so
%{_libdir}/libopencv_wechat_qrcode.so
%{_libdir}/libopencv_xfeatures2d.so
%{_libdir}/libopencv_ximgproc.so
%{_libdir}/libopencv_xobjdetect.so
%{_libdir}/libopencv_xphoto.so
# viz
%if %{with vtk}
%{_libdir}/libopencv_viz.so
%endif
%{_includedir}/opencv4
%dir %{_libdir}/cmake/opencv4
%{_libdir}/cmake/opencv4/OpenCV*.cmake
%{_pkgconfigdir}/opencv4.pc

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
%dir %{py_sitedir}/cv2
%dir %{py_sitedir}/cv2/python-*
%attr(755,root,root) %{py_sitedir}/cv2/python-*/cv2.so
%{py_sitedir}/cv2/*.py[co]
%{py_sitedir}/cv2/mat_wrapper
%{py_sitedir}/cv2/misc
%{py_sitedir}/cv2/utils

%files -n python3-opencv
%defattr(644,root,root,755)
%dir %{py3_sitedir}/cv2
%dir %{py3_sitedir}/cv2/python-*
%attr(755,root,root) %{py3_sitedir}/cv2/python-*/cv2.cpython-*.so
%{py3_sitedir}/cv2/*.py
%{py3_sitedir}/cv2/__pycache__
%{py3_sitedir}/cv2/gapi
%{py3_sitedir}/cv2/mat_wrapper
%{py3_sitedir}/cv2/misc
%{py3_sitedir}/cv2/utils
