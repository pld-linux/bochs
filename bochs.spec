# TODO:
#	- more subpackages (plugins)

Summary:	Portable x86 PC Emulator
Summary(pl):	Przeno¶ny emulator x86 PC
Name:		bochs
Version:	2.0.2
Release:	2
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	11bb4e7804f9fef3cda3822f03641b55
Patch0:		%{name}-cpu.patch
Patch1:		%{name}-ncurses.patch
Patch2:		%{name}-wxGTK.patch
URL:		http://bochs.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	libstdc++-devel
BuildRequires:	wxGTK-devel
BuildRequires:	SDL-devel
BuildRequires:	svgalib-devel
BuildRequires:	autoconf
#vga.pcf.gz
Requires:	XFree86-fonts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%description -l pl
Bochs jest przeno¶nym emulatorem x86 PC emuluj±cym wystarczaj±co du¿o
architektury procesora x86 oraz hardware'u AT i BIOS-u ¿eby uruchomiæ
DOS-a, Windows'95, Minix 2.0 i inne systemu operacyjne, wszystkie na
Twoim komputerze.

%prep
%setup -q
%patch0	-p1
%patch1	-p1
%patch2	-p1

%build
%{__autoconf}
%configure \
	--enable-cdrom \
	--enable-cpu-level=5 \
	--enable-vbe \
	--enable-sb16=linux \
	--enable-configure-interface \
	--enable-new-pit \
	--enable-ne2000 \
	--enable-plugins \
	--enable-repeat-speedups \
	--enable-icache \
	--enable-host-specific-asms \
	--enable-all-optimizations \
	--enable-mmx \
	--enable-sse=2 \
	--with-x \
	--with-wx \
	--with-rfb \
	--with-sdl \
	--with-svga \
	--with-x11 \
	--with-term \
	--with-rfb

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT \
    docdir=%{_docdir}/%{name}-%{version}

mv -f $RPM_BUILD_ROOT%{_datadir}/bochs/VGABIOS*{LICENSE,README,latest} \
    $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

cp -f TESTFORM.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{_datadir}/bochs/*fonts
rm -f $RPM_BUILD_ROOT%{_datadir}/bochs/*pcf

DIRS=`find $RPM_BUILD_ROOT -type d -name CVS`
for DIR in $DIRS
do
    rm -rf $DIR
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/keymaps
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/%{name}/keymaps/convertmap.pl
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so.*
%{_libdir}/%{name}/plugins/*.la
%{_datadir}/%{name}/keymaps/*.map
%{_datadir}/%{name}/*BIOS*
%{_mandir}/man[15]/*
%{_docdir}/%{name}-%{version}
