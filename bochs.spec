Summary:	Portable x86 PC Emulator
Summary(pl):	Przeno¶ny emulator x86 PC
Name:		bochs
Version:	1.1.2
Release:	1
License:	GPL
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://bochs.com/pub/%{name}-%{version}.tar.gz
URL:		http://www.bochs.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bochs is a portable x86 PC emulation software package that emulates
enough of the x86 CPU, related AT hardware, and BIOS to run DOS,
Windows '95, Minix 2.0, and other OS's, all on your workstation.

%description -l pl
Bochs jest przeno¶nym emulatorem x86 PC emuluj±cym wystarczaj±co du¿o
architektóry procesora x86 oraz hardwaru AT i BIOS-u ¿eby uruchomiæ
DOS-a, windows'95, Minix 2.0 i inne systemu operacyjne, wszystkie na
twoim komputerze.

%prep
%setup -q

%build
%configure \
	--with-x \
	--enable-cpu-level=5 \
	--enable-vga \
	--enable-fpu \
	--enable-cdrom \
	--with-x11
%{__make}
cd font
for i in vga.bdf hercules.bdf; 
do
	bdftopcf $i -o `basename $i .bdf`.pcf
done;
cd ..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{%{_bindir},%{_datadir}/bochs/bios,%{_datadir}/fonts/misc}
install bochs $RPM_BUILD_ROOT/%{_bindir}
install bios/BIOS-bochs-990925a bios/VGABIOS-elpin-2.40 $RPM_BUILD_ROOT%{_datadir}/bochs/bios
mv -f .bochsrc .brc
echo "Example .bochrc file - put it into selected directory and modify" \
     "path to images" >.bochsrc
sed -e 's#bios#%{_datadir}/bochs/bios#g' <.brc >>.bochsrc
gzip -9nf docs-html/* bios/VGABIOS-elpin-LICENSE .bochsrc font/*.pcf
install font/*.pcf* $RPM_BUILD_ROOT%{_datadir}/fonts/misc

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
%doc docs-html/* bios/VGABIOS-elpin-LICENSE* .bochsrc*
%attr(755,root,root) %{_bindir}/bochs
%dir %{_datadir}/bochs
%{_datadir}/bochs/*
%{_datadir}/fonts/misc/*.pcf*
