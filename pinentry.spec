Name:           pinentry
Version:        1.1.1
Release:        1
Summary:        A new module that contains various interfaces to enter a PIN/passphrase.

License:        GPLv2+
URL:            https://github.com/gpg/pinentry/archive/pinentry-1.1.0.tar.gz
Source0:        https://www.gnupg.org/ftp/gcrypt/pinentry/%{name}-%{version}.tar.bz2

# source1 is from opensuse
Source1:        pinentry-wrapper
Source2:        https://www.gnupg.org/ftp/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

BuildRequires:  pkgconfig(Qt5Widgets) libcap-devel ncurses-devel libassuan-devel
BuildRequires:  libgpg-error-devel libsecret-devel pkgconfig(Qt5Core) gcc
BuildRequires:  pkgconfig(Qt5Gui) gcr-devel gtk2-devel

Requires(pre):  %{_sbindir}/update-alternatives
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Provides:       %{name}-gui = %{version}-%{release}
Provides:       pinentry-gtk2 = %{version}-%{release}
Provides:       %{name}-curses = %{version}-%{release}
Provides:       %{name}-emacs %{name}-gnome3 %{name}-gtk
Obsoletes:      %{name}-emacs %{name}-gnome3 %{name}-gtk

%description
This is a collection of PIN or passphrase entry dialogs which
utilize the Assuan protocol as specified in the Libassuan manual.

There are programs for different toolkits available.  For all GUIs it
is automatically detected which modules can be built, but it can also
be requested explicitly.

%package        qt
Summary:        Collection of Simple PIN or Passphrase Entry Dialogs
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-gui = %{version}-%{release}
Obsoletes:      %{name}-qt4 < 0.8.0-2
Provides:       %{name}-qt5 = %{version}-%{release}

%description qt
Pinentry is a collection of PIN or passphrase entry dialogs which
utilize the Assuan protocol as specified in the Libassuan manual.

This package contains the Qt4 and Qt5 GUI based version of the PIN entry dialog.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --enable-pinentry-gnome3 --enable-pinentry-gtk2 --enable-pinentry-emacs \
          --enable-pinentry-qt5 --enable-libsecret --disable-pinentry-fltk --disable-rpath\
          --without-libcap --disable-dependency-tracking
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}
ln -s pinentry-gtk-2 %{buildroot}%{_bindir}/pinentry-gtk
ln -s pinentry-qt %{buildroot}%{_bindir}/pinentry-qt4

%post
if [ -f %{_infodir}/pinentry.info* ]; then
  /sbin/install-info %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi

%preun
if [ $1 -eq 0 -a -f %{_infodir}/pinentry.info* ] ; then
  /sbin/install-info --delete %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi

%files
%doc AUTHORS README THANKS
%license COPYING
%{_bindir}/pinentry
%{_bindir}/pinentry-curses
%{_bindir}/pinentry-emacs
%{_bindir}/pinentry-gnome3
%{_bindir}/pinentry-gtk*
%{_datadir}/info/pinentry.info.gz
%exclude %{_datadir}/info/dir

%files qt
%{_bindir}/pinentry-qt*

%files help
%doc ChangeLog NEWS TODO

%changelog
* Thu Dec 30 2021 zoulin <zoulin13@huawei.com> - 1.1.1-1
- update version to 1.1.1

* Tue Sep 17 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.1.0-5
- Package Init
