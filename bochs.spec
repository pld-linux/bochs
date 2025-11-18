# TODO:
#	- more subpackages (plugins)
#
# Conditonal build:
%bcond_without	system_libslirp	# system libslirp instead of builtin

Summary:	Portable x86 PC Emulator
Summary(pl.UTF-8):	Przenośny emulator x86 PC
Name:		bochs
Version:	3.0
Release:	2
License:	LGPL v2+
Group:		Applications/Emulators
Source0:	https://downloads.sourceforge.net/bochs/%{name}-%{version}.tar.gz
# Source0-md5:	407a010ab5cdb78e8ca8795dafdc3323
URL:		https://bochs.sourceforge.net/
BuildRequires:	SDL2-devel >= 2.0.5
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.71
BuildRequires:	automake
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	libltdl-devel
# or soxr (libsamplerate is preferred)
BuildRequires:	libsamplerate-devel
%{?with_system_libslirp:BuildRequires:	libslirp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvncserver-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	wxGTK3-unicode-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXrandr-devel
#Requires:	xorg-font-???
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols from executable
%define		skip_post_check_so	libbx_.*

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%description -l pl.UTF-8
Bochs jest przenośnym emulatorem x86 PC emulującym wystarczająco dużo
architektury procesora x86 oraz hardware'u AT i BIOS-u żeby uruchomić
DOS-a, Windows 95, Minix 2.0 i inne systemy operacyjne, wszystkie na
Twoim komputerze.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoconf}
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	WX_CONFIG="wx-gtk3-unicode-config" \
	--enable-3dnow \
	--enable-all-optimizations \
	--enable-amx \
	--enable-avx \
	--enable-cdrom \
	--enable-cet \
	--enable-clgd54xx \
	--enable-cpu-level=6 \
	--enable-e1000 \
	--enable-es1370 \
	--enable-evex \
%ifarch %{ix86}
	--enable-fast-function-calls \
%endif
	--enable-fpu \
	--enable-gameport \
	--enable-instrumentation \
	--enable-memtype \
	--enable-monitor-mwait \
	--enable-ne2000 \
	--enable-pci \
	--enable-plugins \
	--enable-protection-keys \
	--enable-readline \
	--enable-repeat-speedups \
	--enable-sb16 \
	--enable-smp \
	--enable-svm \
	--enable-uintr \
	--enable-usb \
	--enable-usb-ehci \
	--enable-usb-xhci \
	%{?with_system_libslirp:--enable-using-libslirp} \
	--enable-vmx=2 \
	--enable-voodoo \
	--enable-x86-64 \
	--with-rfb \
	--with-sdl2 \
	--with-term \
	--with-vncsrv \
	--with-wx \
	--with-x11

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_docdir}/%{name}-%{version}

%{__mv} $RPM_BUILD_ROOT%{_datadir}/bochs/VGABIOS*-{LICENSE,README} \
	$RPM_BUILD_ROOT%{_datadir}/bochs/README-i440fx \
	$RPM_BUILD_ROOT%{_datadir}/bochs/Sea*BIOS-README \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

cp -pf TESTFORM.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# lt_dlopened by libbx_*.so names
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bochs
%attr(755,root,root) %{_bindir}/bxhub
%attr(755,root,root) %{_bindir}/bximage
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
# -- gui plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_rfb_gui.so*
# R: SDL2
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_sdl2_gui.so*
# R: ncurses
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_term_gui.so*
# R: libvncserver
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vncsrv_gui.so*
# R: wxGTK3-unicode
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_wx_gui.so*
# R: libX11 libXpm libXrandr
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_x_gui.so*
# -- img plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vbox_img.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vmware3_img.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vmware4_img.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vpc_img.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vvfat_img.so*
# -- eth plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_linux.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_null.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_slirp.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_socket.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_tuntap.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_vde.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_eth_vnet.so*
# -- sound plugins
# R: alsa-lib
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_soundalsa.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_sounddummy.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_soundfile.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_soundoss.so*
# R: pulseaudio-libs
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_soundpulse.so*
# R: SDL2
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_soundsdl.so*
# -- generic plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_acpi.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_biosdev.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_cmos.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_dma.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_e1000.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_es1370.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_extfpuirq.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_floppy.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_gameport.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_harddrv.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_hpet.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_ioapic.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_keyboard.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_ne2k.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_parallel.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_pci.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_pci2isa.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_pci_ide.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_pic.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_pit.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_sb16.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_serial.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_speaker.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_svga_cirrus.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_textconfig.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_unmapped.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_ehci.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_floppy.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_hid.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_hub.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_msd.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_printer.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_uhci.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_usb_xhci.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_vga.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/libbx_voodoo.so*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/keymaps
%{_datadir}/%{name}/BIOS-*
%{_datadir}/%{name}/VGABIOS-*
%{_datadir}/%{name}/bios.bin*
%{_datadir}/%{name}/i440fx.bin
%{_datadir}/%{name}/vgabios-*.bin*
%{_mandir}/man1/bochs.1*
%{_mandir}/man1/bochs-dlx.1*
%{_mandir}/man1/bximage.1*
%{_mandir}/man5/bochsrc.5*
%{_docdir}/%{name}-%{version}
