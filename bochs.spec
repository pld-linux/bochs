# TODO:
#	- more subpackages (plugins)

# Conditional build:
%bcond_without  svga    # without svgalib support
#
%ifnarch %{ix86} alpha
%undefine with_svga
%endif
Summary:	Portable x86 PC Emulator
Summary(pl):	Przeno¶ny emulator x86 PC
Name:		bochs
Version:	2.1.1
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	7b21efbe2b56cc15d110993234259b33
Patch0:		%{name}-ncurses.patch
URL:		http://bochs.sourceforge.net/
BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	gtk+-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	wxGTK2-devel
BuildRequires:	zlib-devel
Requires:	XFree86-fonts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%description -l pl
Bochs jest przeno¶nym emulatorem x86 PC emuluj±cym wystarczaj±co du¿o
architektury procesora x86 oraz hardware'u AT i BIOS-u ¿eby uruchomiæ
DOS-a, Windows 95, Minix 2.0 i inne systemu operacyjne, wszystkie na
Twoim komputerze.

%prep
%setup -q
%patch0	-p1

%build
%{__autoconf}
# --enable-x86-64 (not supported together with --enable-sep)
# --enable-debugger --enable-iodebug --enable-x86-debugger (slowdowns emulation)
# --enable-apic (no need to specify, configure will choose best depending on nr cpus)
%configure \
	WX_CONFIG=wxgtk2-2.4-config \
	--enable-config-interface \
	--enable-new-pit \
	--enable-plugins \
	--enable-cpu-level=6 \
	--enable-compressed-hd \
	--enable-ne2000 \
	--enable-pci \
	--enable-usb \
	--enable-4meg-pages \
	--enable-pae \
	--enable-guest2host-tlb \
	--enable-repeat-speedups \
	--enable-icache \
%ifarch %{ix86}
	--enable-fast-function-calls \
%endif
	--enable-global-pages \
	--enable-host-specific-asms \
	--enable-ignore-bad-msr \
	--enable-disasm \
	--enable-all-optimizations \
	--enable-readline \
	--enable-instrumentation \
	--enable-vbe \
	--enable-fpu \
	--enable-mmx \
	--enable-3dnow \
	--enable-sse=2 \
	--enable-sep \
	--enable-cdrom \
	--enable-sb16=linux \
	--enable-gameport \
	--with-x \
	--with-wx \
	--with-rfb \
	--with-sdl \
	%{?with_svga:-with-svga} \
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

#rm -f $RPM_BUILD_ROOT%{_datadir}/bochs/*fonts
#rm -f $RPM_BUILD_ROOT%{_datadir}/bochs/*pcf

#find $RPM_BUILD_ROOT -type d -name CVS | xargs rm -rf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so.*
%{_libdir}/%{name}/plugins/*.la
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/keymaps
%attr(755,root,root) %{_datadir}/%{name}/keymaps/convertmap.pl
%{_datadir}/%{name}/keymaps/*.map
%{_datadir}/%{name}/*BIOS*
%{_mandir}/man[15]/*
%{_docdir}/%{name}-%{version}
