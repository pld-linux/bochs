# TODO:
#	- more --with and --enable in configure

Summary:	Portable x86 PC Emulator
Summary(pl):	Przeno¶ny emulator x86 PC
Name:		bochs
Version:	2.0
Release:	1.1
License:	GPL
Group:		Applications/Emulators
Source0:	http://telia.dl.sourceforge.net/sourceforge/bochs/%{name}-%{version}.tar.gz
URL:		http://bochs.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	libstdc++-devel
BuildRequires:	wxGTK-devel
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

%build
%configure \
	--enable-cdrom \
	--enable-cpu-level=6 \
	--enable-vbe \
	--with-x \
	--with-wx \
	--with-x11
	
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
%{_datadir}/%{name}/keymaps/*.map
%{_datadir}/%{name}/*BIOS*
%{_mandir}/man[15]/*
%{_docdir}/%{name}-%{version}
