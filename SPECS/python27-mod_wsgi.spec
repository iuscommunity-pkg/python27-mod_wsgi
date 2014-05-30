
%global pybasever 2.7
%global pyver 27
%global real_name mod_wsgi

# not supported by python27 in IUS currently
#%%global __os_install_post %{__python26_os_install_post}
%global __python %{_bindir}/python%{pybasever}

Name:           python%{pyver}-mod_wsgi
Version:        4.1.1
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
Vendor:         IUS Community Project
URL:            http://modwsgi.readthedocs.org
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz
Source1:        python27-mod_wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
BuildRequires:  python%{pyver}, python%{pyver}-devel
Provides:       %{real_name} = %{version}

Obsoletes:      mod_wsgi-python%{pyver} < 3.2-2
Provides:       mod_wsgi-python%{pyver} = %{version}-%{release}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q -n %{real_name}-%{version}


%build
%configure --with-python=python%{pybasever}
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

mv  %{buildroot}%{_libdir}/httpd/modules/mod_wsgi.so \
    %{buildroot}%{_libdir}/httpd/modules/%{name}.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENCE README.rst
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Fri May 30 2014 Ben Harper <ben.harper@rackspace.com> - 4.1.1-1.ius
- Latest sources from upstream

* Mon Nov 26 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-2.ius
- Porting to python27

* Mon Apr 28 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
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

