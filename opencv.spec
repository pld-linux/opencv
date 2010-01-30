%bcond_with	xine
%define	snap	pre1
Summary:	A library of programming functions mainly aimed at real time computer vision
Name:		opencv
Version:	1.1
Release:	0.%{snap}.6
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/opencvlibrary/%{name}-%{version}%{snap}.tar.gz
# Source0-md5:	b147b7cd3c059831c415c5a2bcecdf95
Patch0:		%{name}-ffmpeg.patch
Patch1:		%{name}-am.patch
Patch2:		%{name}-build.patch
URL:		http://opencv.willowgarage.com
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
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
%setup -q -n %{name}-%{version}.0
%patch0 -p0
%patch1 -p1
%patch2 -p1

sed -i -e 's#ACLOCAL_AMFLAGS.*##g' Makefile.am
sed -i -e 's#pkgpython#pkgpyexec#g' interfaces/swig/python/Makefile.am
sed -i -e 's#-L$(SWIG_PYTHON_LIBS)#$(NOTING_NOT_EMPTY_LINE)#g' interfaces/swig/python/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I autotools/aclocal
%{__autoconf}
%{__automake}
%configure \
%ifarch i686 pentium4 athlon %{x8664}
	--enable-sse2 \
%else
	--disable-sse2 \
%endif
	--with-python \
	--with%{!?with_xine:out}-xine \
	--with-ffmpeg \
	--with-1394libs \
	--with-v4l \
	--with-gtk \
	--without-gstreamer \
	--without-quicktime
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog THANKS TODO
%doc docs/*.{htm,rtf,png,txt} docs/papers docs/ref
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/opencv
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-opencv
%defattr(644,root,root,755)
%dir %{py_sitedir}/opencv
%attr(755,root,root) %{py_sitedir}/opencv/*.so
%{py_sitedir}/opencv/*.py[co]
