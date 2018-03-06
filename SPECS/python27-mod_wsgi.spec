# IUS spec file for python27-mod_wsgi, forked from Fedora

%global srcname mod_wsgi
%global python python27

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name:           %{python}-%{srcname}
Version:        4.6.2
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
License:        ASL 2.0
URL:            https://modwsgi.readthedocs.io/
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz#/mod_wsgi-%{version}.tar.gz
Source1:        %{name}.conf
Patch0:		mod_wsgi-4.5.24-sphinx-build.patch
Patch1:		mod_wsgi-4.6.2-exports.patch
BuildRequires:  httpd-devel < 2.4.10
BuildRequires:  %{python}-devel
BuildRequires:	%{python}-setuptools
#needed for docs only
BuildRequires:	python-sphinx10
BuildRequires:	python-sphinx_rtd_theme

Requires:	%{python}-setuptools
Requires:       httpd-mmn = %{_httpd_mmn}
Provides:       %{srcname} = %{version}

%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1


%build
make -C docs html

export LDFLAGS="$RPM_LD_FLAGS -L%{_libdir}"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --enable-shared --with-apxs=%{_httpd_apxs} --with-python=%{__python27}
%{__make} %{?_smp_mflags}
%py2_build


%install
%{__make} install DESTDIR=%{buildroot} LIBEXECDIR=%{_httpd_moddir}
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}%{_httpd_confdir}/%{name}.conf
%{__mv} %{buildroot}%{_httpd_moddir}/{%{srcname},%{name}}.so
%py2_install
mv $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express{,-2}
ln -s %{_bindir}/mod_wsgi-express-2 $RPM_BUILD_ROOT%{_bindir}/mod_wsgi-express

%files
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_httpd_confdir}/%{name}.conf
%{_httpd_moddir}/%{name}.so
%{python27_sitearch}/mod_wsgi-*.egg-info
%{python27_sitearch}/mod_wsgi
%{_bindir}/mod_wsgi-express-2
%{_bindir}/mod_wsgi-express


%changelog
* Tue Mar 06 2018 Ben Harper <ben.harper@rackspace.com> - 4.6.2-1.ius
- Latest upstream
- add Patch1, adapted from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/c8a7642dcf4742963337e1c4e15b1263951c6ce6

* Fri Dec 15 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.25-1.ius
- Latest upstream
- update URL from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/5585f33d82e1f027384d70df753b545ac7ab36de
- build docs and mod_wsgi-express from Fedora:
  https://src.fedoraproject.org/rpms/mod_wsgi/c/241a680c246d91f55a733aa1f45a480697c28ff4

* Thu Nov 16 2017 Carl George <carl@george.computer> - 4.5.21-1.ius
- Latest upstream

* Mon Oct 02 2017 Carl George <carl@george.computer> - 4.5.19-1.ius
- Latest upstream

* Tue Aug 29 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.18-1.ius
- Latest upstream

* Fri Jul 07 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.17-1.ius
- Latest upstream

* Tue Mar 14 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.15-1.ius
- Latest upstream

* Wed Jan 25 2017 Carl George <carl.george@rackspace.com> - 4.5.14-1.ius
- Latest upstream

* Wed Jan 04 2017 Ben Harper <ben.harper@rackspace.com> - 4.5.13-1.ius
- Latest upstream

* Wed Dec 14 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.10-1.ius
- Latest upstream

* Tue Nov 29 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.9-1.ius
- Latest upstream

* Wed Sep 21 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.7-1.ius
- Latest upstream

* Tue Sep 06 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.6-1.ius
- Latest upstream

* Tue Aug 16 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.5-1.ius
- Latest upstream

* Fri Aug 12 2016 Carl George <carl.george@rackspace.com> - 4.5.4-1.ius
- Latest upstream

* Thu Jun 23 2016 Carl George <carl.george@rackspace.com> - 4.5.3-1.ius
- Latest upstream

* Tue Apr 26 2016 Ben Harper <ben.harper@rackspace.com> - 4.5.2-1.ius
- Latest upstream

* Mon Apr 11 2016 Carl George <carl.george@rackspace.com> - 4.5.1-1.ius
- Latest upstream
- Switch to GitHub source via srcurl.net
- Use configure/install flags from Fedora
- Filter auto-provides

* Tue Jan 26 2016 Ben Harper <ben.harper@rackspace.com> - 4.4.22-1.ius
- Latest upstream

* Wed Nov 04 2015 Carl George <carl.george@rackspace.com> - 4.4.21-1.ius
- Latest upstream

* Tue Oct 20 2015 Carl George <carl.george@rackspace.com> - 4.4.20-1.ius
- Latest upstream

* Mon Oct 05 2015 Carl George <carl.george@rackspace.com> - 4.4.15-1.ius
- Latest upstream

* Tue Jun 16 2015 Ben Harper <ben.harper@rackspace.com> - 4.4.13-1.ius
- Latest upstream

* Mon Jun 01 2015 Ben Harper <ben.harper@rackspace.com> - 4.4.12-1.ius
- Latest upstream

* Mon Apr 06 2015 Carl George <carl.george@rackspace.com> - 4.4.11-1.ius
- Latest upstream

* Mon Mar 23 2015 Carl George <carl.george@rackspace.com> - 4.4.10-1.ius
- Latest upstream

* Thu Mar 05 2015 Carl George <carl.george@rackspace.com> - 4.4.9-1.ius
- Latest upstream

* Wed Feb 18 2015 Carl George <carl.george@rackspace.com> - 4.4.8-1.ius
- Latest upstream

* Mon Feb 02 2015 Carl George <carl.george@rackspace.com> - 4.4.7-1.ius
- Latest upstream

* Thu Jan 15 2015 Carl George <carl.george@rackspace.com> - 4.4.6-1.ius
- Latest upstream

* Thu Jan 08 2015 Carl George <carl.george@rackspace.com> - 4.4.5-2.ius
- Ensure we build against and require the stock version of httpd

* Mon Jan 05 2015 Carl George <carl.george@rackspace.com> - 4.4.5-1.ius
- Latest upstream

* Thu Dec 18 2014 Carl George <carl.george@rackspace.com> - 4.4.2-1.ius
- Latest upstream

* Mon Dec 15 2014 Carl George <carl.george@rackspace.com> - 4.4.1-1.ius
- Latest upstream

* Mon Dec 01 2014 Ben Harper <ben.harper@rackspace.com> - 4.4.0-1.ius
- Latest upstream

* Tue Nov 11 2014 Carl George <carl.george@rackspace.com> - 4.3.2-1.ius
- Latest upstream

* Mon Nov 03 2014 Ben Harper <ben.harper@rackspace.com> - 4.3.1-1.ius
- Latest upstream

* Mon Sep 15 2014 Carl George <carl.george@rackspace.com> - 4.3.0-1.ius
- Latest upstream

* Wed Aug 27 2014 Carl George <carl.george@rackspace.com> - 4.2.8-1.ius
- Latest upstream

* Mon Aug 04 2014 Ben Harper <ben.harper@rackspace.com> - 4.2.7-1.ius
- Latest upstream

* Wed Jul 16 2014 Carl George <carl.george@rackspace.com> - 4.2.6-1.ius
- Latest upstream
- Patch1 merged upstream

* Tue Jul 15 2014 Carl George <carl.george@rackspace.com> - 4.2.5-2.ius
- Backport fix for segfault on apache httpd 2.2.3 (el5)
  https://bugs.launchpad.net/ius/+bug/1341325

* Mon Jul 07 2014 Carl George <carl.george@rackspace.com> - 4.2.5-1.ius
- Latest upstream

* Thu Jun 19 2014 Carl George <carl.george@rackspace.com> - 4.2.4-1.ius
- Get source from pypi instead of github
- Latest sources from upstream

* Thu Jun 05 2014 Carl George <carl.george@rackspace.com> - 4.1.3-1.ius
- Latest sources from upstream
- Override __os_install_post to fix .pyc/pyo magic

* Mon Jun 02 2014 Carl George <carl.george@rackspace.com> - 4.1.2-1.ius
- Latest sources from upstream
- Implement python packaging best practices
- Fix missing requirements
- Combine two install commands into one

* Fri May 30 2014 Ben Harper <ben.harper@rackspace.com> - 4.1.1-1.ius
- Latest sources from upstream

* Mon Nov 26 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-2.ius
- Porting to python27

* Sat Apr 28 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
- Latest sources from upstream

* Mon Apr 16 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-4.ius
- Rebuilding against latest python31

* Mon Jun 13 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-3.ius
- Rebuilding against latest python 3.1.4

* Tue May 31 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-2.ius
- Rebuilt against python 3.1.3 to fix api breakage
  https://bugs.launchpad.net/ius/+bug/790060
- Correcting a incorrect reference to python26 in SOURCE config

* Tue Nov 02 2010 BJ Dierkes <wdierkes@rackspace.com> - 3.3.ius
- Latest sources from upstream.  Full changelog available at:
  http://code.google.com/p/modwsgi/wiki/ChangesInVersion0303
  http://code.google.com/p/modwsgi/wiki/ChangesInVersion0302  
- Removed Conflicts: mod_python (use IfModule instead).
- Add posttrans hack for upgrading from mod_wsgi-python31

* Thu Dec 17 2009 BJ Dierkes <wdierkes@rackspace.com> - 3.1.ius
- Latest sources from upstream.

* Mon Nov 23 2009 BJ Dierkes <wdierkes@rackspace.com> 3.0.ius
- Latest sources from upstream.

* Mon Oct 19 2009 BJ Dierkes <wdierkes@rackspace.com> 3.0c5-1.ius
- Rebuilding for IUS
- Latest stable sources from upstream

* Wed Oct 08 2008 James Bowes <jbowes@redhat.com> 2.1-2
- Remove requires on httpd-devel

* Wed Jul 02 2008 James Bowes <jbowes@redhat.com> 2.1-1
- Update to 2.1

* Mon Jun 16 2008 Ricky Zhou <ricky@fedoraproject.org> 1.3-4
- Build against the shared python lib.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 James Bowes <jbowes@redhat.com> 1.3-2
- Require httpd

* Sat Jan 05 2008 James Bowes <jbowes@redhat.com> 1.3-1
- Update to 1.3

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.0-1
- Initial packaging for Fedora

