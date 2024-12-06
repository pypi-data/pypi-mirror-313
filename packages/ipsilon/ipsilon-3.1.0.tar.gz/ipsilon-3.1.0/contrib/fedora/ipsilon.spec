# Bundling request for bootstrap/patternfly: https://fedorahosted.org/fpc/ticket/483

Name:       ipsilon
Version:    3.1.0
Release:    1%{?builddate}%{?gittag}%{?dist}
Summary:    An Identity Provider Server

License:    GPLv3+
URL:        https://pagure.io/ipsilon
Source0:    https://pagure.io/%{name}/archive/v%{version}/ipsilon-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-lasso
BuildRequires:  python3-openid, python3-openid-cla, python3-openid-teams
BuildRequires:  python3-m2crypto
BuildRequires:  make

Requires:       python3-setuptools
Requires:       python3-requests
Requires:       python3-filetype
Requires:       %{name}-base = %{version}-%{release}

%description
Ipsilon is a multi-protocol Identity Provider service. Its function is to
bridge authentication providers and applications to achieve Single Sign On
and Federation.


%package base
Summary:        Ipsilon base IDP server
License:        GPLv3+
Requires:       httpd
Requires:       mod_ssl
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-provider = %{version}-%{release}
Requires:       python3-mod_wsgi
Requires:       python3-cherrypy
Requires:       python3-jinja2
Requires:       python3-lxml
Requires:       python3-sqlalchemy
Requires:       open-sans-fonts
Requires:       fontawesome-fonts
Requires:       pam
Requires(pre):  shadow-utils

%description base
The Ipsilon IdP server without installer


%package filesystem
Summary:        Package providing files required by Ipsilon
License:        GPLv3+

%description filesystem
Package providing basic directory structure required
for all Ipsilon parts


%package client
Summary:        Tools for configuring Ipsilon clients
License:        GPLv3+
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-saml2-base = %{version}-%{release}
Requires:       mod_auth_mellon
Requires:       mod_auth_openidc
Requires:       mod_ssl
Requires:       python3-requests
BuildArch:      noarch

%description client
Client install tools


%package tools-ipa
summary:        IPA helpers
License:        GPLv3+
Requires:       %{name}-authgssapi = %{version}-%{release}
Requires:       %{name}-authform = %{version}-%{release}
Requires:       %{name}-infosssd = %{version}-%{release}
%if 0%{?rhel}
Requires:       ipa-client
Requires:       ipa-admintools
%else
Requires:       freeipa-client
Requires:       freeipa-admintools
%endif
BuildArch:      noarch

%description tools-ipa
Convenience client install tools for IPA support in the Ipsilon identity Provider


%package saml2-base
Summary:        SAML2 base
License:        GPLv3+
Requires:       openssl
Requires:       python3-lasso
Requires:       python3-lxml
BuildArch:      noarch

%description saml2-base
Provides core SAML2 utilities


%package saml2
Summary:        SAML2 provider plugin
License:        GPLv3+
Provides:       ipsilon-provider = %{version}-%{release}
Requires:       %{name}-base = %{version}-%{release}
Requires:       %{name}-saml2-base = %{version}-%{release}
BuildArch:      noarch

%description saml2
Provides a SAML2 provider plugin for the Ipsilon identity Provider


%package openid
Summary:        Openid provider plugin
License:        GPLv3+
Provides:       ipsilon-provider = %{version}-%{release}
Requires:       %{name}-base = %{version}-%{release}
Requires:       python3-openid
Requires:       python3-openid-cla
Requires:       python3-openid-teams
BuildArch:      noarch

%description openid
Provides an OpenId provider plugin for the Ipsilon identity Provider

%package openidc
Summary:        OpenID Connect provider plugin
License:        GPLv3+
Provides:       ipsilon-provider = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       python3-jwcrypto
BuildArch:      noarch

%description openidc
Provides an OpenID Connect and OAuth2 provider plugin for the Ipsilon
identity Provider


%package authform
Summary:        mod_intercept_form_submit login plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       mod_intercept_form_submit
BuildArch:      noarch

%description authform
Provides a login plugin to authenticate with mod_intercept_form_submit


%package authpam
Summary:        PAM based login plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       python3-pam
BuildArch:      noarch

%description authpam
Provides a login plugin to authenticate against the local PAM stack


%package authgssapi
Summary:        mod_auth_gssapi based login plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       mod_auth_gssapi
BuildArch:      noarch

%description authgssapi
Provides a login plugin to allow authentication via the mod_auth_gssapi
Apache module.


%package authldap
Summary:        LDAP info and login plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       python3-ldap
BuildArch:      noarch

%description authldap
Provides a login plugin to allow authentication and info retrieval via LDAP.


%package infofas
Summary:        Fedora Authentication System login plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       %{name}-infosssd = %{version}-%{release}
BuildArch:      noarch

%description infofas
Provides an info plugin to retrieve info from the Fedora Authentication System


%package infosssd
Summary:        SSSD based identity plugin
License:        GPLv3+
Requires:       %{name}-base = %{version}-%{release}
Requires:       python3-sssdconfig
Requires:       sssd >= 1.12.4
BuildArch:      noarch

%description infosssd
Provides an info plugin to allow retrieval via SSSD.

%package theme-Fedora
Summary:        Fedora Account System theme
Requires:       %{name}-base = %{version}-%{release}
BuildArch:      noarch

%description theme-Fedora
Provides a theme for Ipsilon used for the Fedora Account System.

%package theme-openSUSE
Summary:        openSUSE Accounts theme
Requires:       %{name}-base = %{version}-%{release}
BuildArch:      noarch

%description theme-openSUSE
Provides a theme for Ipsilon used for openSUSE Accounts.

%prep
%autosetup -p1


%build
%py3_build


%install
%py3_install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libexecdir}/ipsilon
mkdir -p %{buildroot}%{_defaultdocdir}
mkdir -p %{buildroot}%{_localstatedir}/cache/ipsilon
# These 0700 permissions are because ipsilon will store private keys here
install -d -m 0700 %{buildroot}%{_sharedstatedir}/ipsilon
install -d -m 0700 %{buildroot}%{_sysconfdir}/ipsilon
mv %{buildroot}/%{_bindir}/ipsilon %{buildroot}/%{_libexecdir}/ipsilon/ipsilon
mv %{buildroot}/%{_bindir}/ipsilon-server-install %{buildroot}/%{_sbindir}
mv %{buildroot}/%{_bindir}/ipsilon-upgrade-database %{buildroot}/%{_sbindir}
mv %{buildroot}%{_defaultdocdir}/%{name} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -fr %{buildroot}%{python3_sitelib}/tests
ln -s %{_datadir}/fonts %{buildroot}%{_datadir}/ipsilon/ui/fonts

mkdir -p  %{buildroot}%{_sysconfdir}/pam.d
cp %{buildroot}%{_datadir}/ipsilon/templates/install/pam/ipsilon.pamd %{buildroot}%{_sysconfdir}/pam.d/ipsilon

#%check
# The test suite is not being run because:
#  1. The last step of %%install removes the entire test suite
#  2. It increases build time a lot
#  3. It adds more build dependencies (namely postgresql server and client libraries)

%pre base
getent group ipsilon >/dev/null || groupadd -r ipsilon
getent passwd ipsilon >/dev/null || \
    useradd -r -g ipsilon -d %{_sharedstatedir}/ipsilon -s /sbin/nologin \
    -c "Ipsilon Server" ipsilon
exit 0


%files filesystem
%doc README.md
%license COPYING
%dir %{_datadir}/ipsilon
%dir %{_datadir}/ipsilon/templates
%dir %{_datadir}/ipsilon/templates/install
%dir %{python3_sitelib}/ipsilon
%{python3_sitelib}/ipsilon/__init__.py*
%{python3_sitelib}/ipsilon-*.egg-info
%dir %{python3_sitelib}/ipsilon/__pycache__/
%{python3_sitelib}/ipsilon/__pycache__/__init__.*
%dir %{python3_sitelib}/ipsilon/tools
%{python3_sitelib}/ipsilon/tools/__init__.py*
%{python3_sitelib}/ipsilon/tools/files.py*
%dir %{python3_sitelib}/ipsilon/tools/__pycache__
%{python3_sitelib}/ipsilon/tools/__pycache__/__init__.*
%{python3_sitelib}/ipsilon/tools/__pycache__/files.*

%files
%license COPYING
%{_sbindir}/ipsilon-server-install
%{_bindir}/ipsilon-db2conf
%{_datadir}/ipsilon/templates/install/*.conf
%{_datadir}/ipsilon/ui/saml2sp
%dir %{python3_sitelib}/ipsilon/helpers
%{python3_sitelib}/ipsilon/helpers/common.py*
%{python3_sitelib}/ipsilon/helpers/__init__.py*
%dir %{python3_sitelib}/ipsilon/helpers/__pycache__
%{python3_sitelib}/ipsilon/helpers/__pycache__/__init__.*
%{python3_sitelib}/ipsilon/helpers/__pycache__/common.*
%{_mandir}/man*/ipsilon-server-install.1*

%files base
%license COPYING
%doc examples doc
%{_defaultdocdir}/%{name}-%{version}
%{python3_sitelib}/ipsilon/admin
%{python3_sitelib}/ipsilon/authz
%{python3_sitelib}/ipsilon/rest
%{python3_sitelib}/ipsilon/tools/dbupgrade.py*
%{python3_sitelib}/ipsilon/tools/__pycache__/dbupgrade.*
%dir %{python3_sitelib}/ipsilon/login
%{python3_sitelib}/ipsilon/login/__init__*
%{python3_sitelib}/ipsilon/login/common*
%{python3_sitelib}/ipsilon/login/authtest*
%dir %{python3_sitelib}/ipsilon/login/__pycache__
%{python3_sitelib}/ipsilon/login/__pycache__/__init__*
%{python3_sitelib}/ipsilon/login/__pycache__/common*
%{python3_sitelib}/ipsilon/login/__pycache__/authtest*
%dir %{python3_sitelib}/ipsilon/info
%{python3_sitelib}/ipsilon/info/__init__*
%{python3_sitelib}/ipsilon/info/common*
%{python3_sitelib}/ipsilon/info/infonss*
%dir %{python3_sitelib}/ipsilon/info/__pycache__
%{python3_sitelib}/ipsilon/info/__pycache__/__init__*
%{python3_sitelib}/ipsilon/info/__pycache__/common*
%{python3_sitelib}/ipsilon/info/__pycache__/infonss*
%dir %{python3_sitelib}/ipsilon/providers
%{python3_sitelib}/ipsilon/providers/__init__*
%{python3_sitelib}/ipsilon/providers/common*
%dir %{python3_sitelib}/ipsilon/providers/__pycache__
%{python3_sitelib}/ipsilon/providers/__pycache__/__init__*
%{python3_sitelib}/ipsilon/providers/__pycache__/common*
%{python3_sitelib}/ipsilon/root.py*
%{python3_sitelib}/ipsilon/__pycache__/root.*
%{python3_sitelib}/ipsilon/util
%{python3_sitelib}/ipsilon/user
%{_mandir}/man*/ipsilon.7*
%{_mandir}/man*/ipsilon.conf.5*
%{_datadir}/ipsilon/templates/*.html
%{_datadir}/ipsilon/templates/admin
%{_datadir}/ipsilon/templates/user
%dir %{_datadir}/ipsilon/templates/login
%{_datadir}/ipsilon/templates/login/index.html
%{_datadir}/ipsilon/templates/login/form.html
%dir %{_datadir}/ipsilon/ui
%{_datadir}/ipsilon/ui/css
%{_datadir}/ipsilon/ui/img
%{_datadir}/ipsilon/ui/js
%{_datadir}/ipsilon/ui/fonts
%{_datadir}/ipsilon/ui/fonts-local
%{_libexecdir}/ipsilon/
%{_sbindir}/ipsilon-upgrade-database
%dir %attr(0751,root,root) %{_sharedstatedir}/ipsilon
%dir %attr(0751,root,root) %{_sysconfdir}/ipsilon
%dir %attr(0750,ipsilon,apache) %{_localstatedir}/cache/ipsilon
%config(noreplace) %{_sysconfdir}/pam.d/ipsilon
%dir %{_datadir}/ipsilon/themes

%files client
%license COPYING
%{_bindir}/ipsilon-client-install
%{_datadir}/ipsilon/templates/install/saml2
%{_datadir}/ipsilon/templates/install/openidc
%{_mandir}/man*/ipsilon-client-install.1*

%files tools-ipa
%license COPYING
%{python3_sitelib}/ipsilon/helpers/ipa.py*
%{python3_sitelib}/ipsilon/helpers/__pycache__/ipa.*

%files saml2-base
%license COPYING
%{python3_sitelib}/ipsilon/tools/saml2metadata.py*
%{python3_sitelib}/ipsilon/tools/certs.py*
%{python3_sitelib}/ipsilon/tools/__pycache__/saml2metadata.*
%{python3_sitelib}/ipsilon/tools/__pycache__/certs.*

%files saml2
%license COPYING
%{python3_sitelib}/ipsilon/providers/saml2*
%{python3_sitelib}/ipsilon/providers/__pycache__/saml2*
%{_datadir}/ipsilon/templates/saml2

%files openid
%license COPYING
%{python3_sitelib}/ipsilon/providers/openidp.py*
%{python3_sitelib}/ipsilon/providers/__pycache__/openidp.*
%{python3_sitelib}/ipsilon/providers/openid/
%{python3_sitelib}/ipsilon/providers/openid/__pycache__/
%{_datadir}/ipsilon/templates/openid

%files openidc
%license COPYING
%{python3_sitelib}/ipsilon/providers/openidcp.py*
%{python3_sitelib}/ipsilon/providers/__pycache__/openidcp.*
%{python3_sitelib}/ipsilon/providers/openidc/
%{python3_sitelib}/ipsilon/providers/openidc/__pycache__/
%{_datadir}/ipsilon/templates/openidc

%files authform
%license COPYING
%{python3_sitelib}/ipsilon/login/authform*
%{python3_sitelib}/ipsilon/login/__pycache__/authform*

%files authpam
%license COPYING
%{python3_sitelib}/ipsilon/login/authpam*
%{python3_sitelib}/ipsilon/login/__pycache__/authpam*
%{_datadir}/ipsilon/templates/install/pam

%files authgssapi
%license COPYING
%{python3_sitelib}/ipsilon/login/authgssapi*
%{python3_sitelib}/ipsilon/login/__pycache__/authgssapi*
%{_datadir}/ipsilon/templates/login/gssapi.html

%files authldap
%license COPYING
%{python3_sitelib}/ipsilon/login/authldap*
%{python3_sitelib}/ipsilon/info/infoldap*
%{python3_sitelib}/ipsilon/login/__pycache__/authldap*
%{python3_sitelib}/ipsilon/info/__pycache__/infoldap*

%files infosssd
%license COPYING
%{python3_sitelib}/ipsilon/info/infosssd.*
%{python3_sitelib}/ipsilon/info/__pycache__/infosssd*

%files infofas
%license COPYING
%{python3_sitelib}/ipsilon/info/infofas.*
%{python3_sitelib}/ipsilon/info/__pycache__/infofas*

%files theme-Fedora
%license COPYING
%{_datadir}/ipsilon/themes/Fedora

%files theme-openSUSE
%license COPYING
%{_datadir}/ipsilon/themes/openSUSE


%changelog
* Thu Dec 05 2024 Aurelien Bompard <abompard@fedoraproject.org> - 3.1.0-1
- Release 3.1.0

* Mon May 23 2022 Aurelien Bompard <abompard@fedoraproject.org> - 3.0.0-1
- Release 3.0.0

* Tue Nov 14 2017 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.1.0-1
- Release 2.1.0

* Mon Oct 31 2016 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.0.2-1
- Release 2.0.2

* Mon Oct 31 2016 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.0.1-1
- Enabling allow authz on upgrade

* Tue Oct 25 2016 Patrick Uiterwijk <puiterwijk@redhat.com> - 2.0.0-1
- Release 2.0.0

* Mon May 02 2016 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.2.0-1
- Release 1.2.0

* Sat Sep 05 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.1.0-1
- Release 1.1.0

* Mon Jun 22 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-2
- Added mod_ssl requirement for ipsilon-client

* Mon May 11 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.0.0-1
- Release 1.0.0

* Wed Apr 15 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.6.0-1
- Release 0.6.0

* Mon Mar 30 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.5.0-1
- Released 0.5.0

* Fri Feb 27 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.4.0-1
- Released 0.4.0

* Tue Feb 24 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-7
- Split the installer into -tools
- Split authform into -authform

* Thu Feb 12 2015 Rob Crittenden <rcritten@redhat.com> - 0.3.0-6
- Add mod_identity_lookup info plugin package

* Wed Jan 28 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-5
- Split IPA tools

* Mon Jan 12 2015 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-4
- Add symlink to fonts directory

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-3
- Fix typo
- Add comments on why the test suite is not in check
- The subpackages require the base package
- Add link to FPC ticket for bundling exception request

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-2
- Fix shebang removal

* Tue Dec 16 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.3.0-1
- Initial packaging
