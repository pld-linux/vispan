%include	/usr/lib/rpm/macros.perl
Summary:	Vispan - VIrus and SPam ANalyser
Summary(pl):	Vispan - analizator wirsów i spamu
Name:		vispan
Version:	2.0.2
Release:	0.9
Epoch:		0
License:	GPL v2
Group:		Applications
Source0:	http://www.while.homeunix.net/mailstats/Vispan-%{version}.tar.gz
# Source0-md5:	62ff80fced226287ea49f8cb897ede71
Patch0:		%{name}-install.patch
URL:		http://www.while.homeunix.net/mailstats/
BuildRequires:	perl-GD-Graph
BuildRequires:	perl-Mail-Sendmail
BuildRequires:	perl-Net-CIDR
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Number-Format
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	crondaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program analyses the mail log file entries created by the
MailScanner program written by Julian Field.

%description -l pl
Ten program analizuje pliki logów stworzonych przez program
MailScanner.

%prep
%setup -q -n Vispan-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLSCRIPT=%{_bindir} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/var/{lib,cache}/vispan,/etc/cron.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/install.pl

sed -e '
	s,/sbin/iptables,/usr/sbin/iptables,
	s,/var/www/html/vispan,/var/lib/vispan,
	s,sdoe@yourdomain.com,postmaster@localhost,
	s,mail.yourdomain.com,localhost,
	s,/tmp/virtmpfile,/var/cache/vispan/virtmpfile,
' Vispan.conf > $RPM_BUILD_ROOT%{_sysconfdir}/Vispan.conf

install vispan.css $RPM_BUILD_ROOT/var/lib/vispan

cat <<'EOF' > $RPM_BUILD_ROOT/etc/cron.d/%{name}
# This is the cron entry to run the Vispan analysis script every 10 minutes.
MAILTO=root
*/10 * * * * stats %{_bindir}/%{name}
# vim:syn=crontab
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/Vispan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/*
%{perl_vendorlib}/Vispan
%dir %attr(770,root,stats) /var/cache/vispan
%dir %attr(775,root,stats) /var/lib/vispan
/var/lib/vispan/vispan.css
