Summary:	Portable x86 PC Emulator
Summary(pl):	Przeno¶ny emulator x86 PC
Name:		bochs
Version:	1.3
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	http://prdownloads.sourceforge.net/bochs/%{name}-%{version}.tar.gz
URL:		http://bochs.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	libstdc++-devel
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

%build
%configure2_13 \
	--with-x \
	--enable-cpu-level=5 \
	--enable-vga \
	--enable-fpu \
	--enable-cdrom \
	--with-x11
%{__make}
cd font
#for i in vga.bdf hercules.bdf;
#do
#	bdftopcf $i -o `basename $i .bdf`.pcf
#done;
# vga.pcf has moved to XFree86-fonts
bdftopcf hercules.bdf -o hercules.pcf
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{%{_bindir},%{_datadir}/bochs/bios,%{_datadir}/fonts/misc,%{_mandir}/man1}
install bochs install-x11-fonts bximage $RPM_BUILD_ROOT/%{_bindir}
install bios/BIOS-bochs-latest* bios/VGABIOS-elpin-2.40 $RPM_BUILD_ROOT%{_datadir}/bochs/bios
install doc/man/{bochs,bochsrc,bximage}.1 $RPM_BUILD_ROOT%{_mandir}/man1

mv -f .bochsrc .brc
echo "Example .bochrc file - put it into selected directory and modify" \
     "path to images" >.bochsrc
sed -e 's#bios#%{_datadir}/bochs/bios#g' <.brc >>.bochsrc

gzip -9nf bios/VGABIOS-elpin-LICENSE .bochsrc font/*.pcf CHANGES TESTFORM.txt

install font/hercules.pcf* $RPM_BUILD_ROOT%{_datadir}/fonts/misc

%clean
rm -rf $RPM_BUILD_ROOT
%post
if [ -x /usr/X11R6/bin/mkfontdir ]; then
        (cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%postun
if [ -x /usr/X11R6/bin/mkfontdir ]; then
        (cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
killall -USR1 xfs > /dev/null 2>&1 ||:

%files
%defattr(644,root,root,755)
%doc docs-html/*.html bios/VGABIOS-elpin-LICENSE* .bochsrc* *.gz
%attr(755,root,root) %{_bindir}/bochs
%attr(755,root,root) %{_bindir}/bximage
%dir %{_datadir}/bochs
%{_datadir}/bochs/*
%{_datadir}/fonts/misc/*.pcf*
%{_mandir}/man1/*
