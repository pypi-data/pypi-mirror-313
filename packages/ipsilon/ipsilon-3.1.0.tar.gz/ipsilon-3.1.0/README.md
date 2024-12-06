
Ipsilon - Identity Provider
===========================

The Ipsilon project implements an [Identity Provider](http://en.wikipedia.org/wiki/Identity_provider)
that is easy to use and configure. And it aims at providing installation scripts
for applications that can use an Apache fronted to perform user authentication.

An IdP server allows users to authenticate against any identity provider
whether that is a corporate LDAP server or even just local files or custom
pluggable modules and allows applications to authenticate users while being
completely agnostic of what authentication infrastructure is being used.

Applications can currently use the [SAML2](http://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
protocol to talk to the Ipsilon identity provider, an application that uses
SAML is called a Service Provider.

Ipsilon uses the [LASSO](http://lasso.entrouvert.org) libraries and Python
bindings to implement SAML support.

Quick test instance
===================

You can run a test instance of Ipsilson from a Git clone, using the
`quickrun.py` script:

    $ ./quickrun.py

This will start an instance which you can access at <http://localhost:8080>.
You can log with any username and password 'ipsilon'. Log in with the special
username 'admin' to get access to the administration console; you can then
visit http://localhost:8080/admin and configure the various identity providers
and more.

The local state is stored in the ./qrun subdirectory, and will be re-loaded
from that directory the next time that the `quickrun.py` script is run.

Ipsilon Server Installation
===========================

The Ipsilon server can be easily installed by simply running the
`ipsilon-server-install` command.

Prerequisites:
- An Apache server with SSL configured
- A keytab if Kerberos authentication is desired
- An unprivileged user to run the Ipsilon code (defaults to 'ipsilon')

Currently there are only two available authentication modules, GSSAPI and
PAM. The Kerberos module uses `mod_auth_gssapi` (which it will configure for
you at install time), the Pam module simply uses the PAM stack with a default service
name set to `ipsilon`.

**NOTE** The PAM module is invoked as an unprivileged user so if you are using the
pam_unix plugin to authenticate users you'll find out that authentication does
not work properly. Please use a different PAM module, like `pam_sss`, `pam_ldap`,
etc..

Before you run the install script make sure to create an administrative user
that can be authenticated either via PAM or GSSAPI. The default name the
installation script expects is `admin` but that can be changed with the command
line option named `--admin-user`

The hostname used is the system host name, if you can't set the system hostname
to a fully qualified name, used the `--hostname` option to pass the desired fully
qualified name for the IdP. It is important to use the correct name as this
name is referenced and resolved by remote clients.

Other options are available by running `ipsilon-server-install --help`

To install a server that allow both GSSAPI (Kerberos) and PAM authentication
use:

    $ ipsilon-server-install --gssapi=yes --pam=yes

This command will generate a default instance called `idp` (you can change the
default name using the `--instance` switch). Multiple instance can be installed
in parallel, each wit a different name.

Instances are configured to be available at https://hostname/instance

So for a server called ipsilon.example.com, using the default installation
options the IdP will be available at https://ipsilon.example.com/idp/

The install script expects to find the keytab in /etc/httpd/conf/http.keytab

**NOTE:** If you are installing Ipsilon in a [FreeIPA](http://www.freeipa.org )
environment you can use the --ipa switch to simplify the deployment.
Using the `--ipa` switch will allow the use of your IPA Kerberos administrative
credentials to automatically provision a keytab for the HTTP service if one is
not available yet.  You will likely want to use the `--admin-user` option to
specify the full principal of the user who will administer Ipsilon.
For example to use the FreeIPA admin user for the EXAMPLE.COM realm, you would use:

    $ ipsilon-server-install --ipa --admin-user admin@EXAMPLE.COM

Once the script has successfully completed the installation, restart the Apache
HTTPD server to activate it.

Use your `admin` user to connect to the Web UI and perform additional
administration tasks.


Ipsilon Clients configuration
=============================

Ipsilon clients can be quickly configured running the provided
`ipsilon-client-install` command.

Prerequisites:
- An Apache server with SSL configured
- The [mod_mellon](https://code.google.com/p/modmellon/) authentication module for Apache
- A previously installed SAML IdP server (like Ipsilon itself)

The default configuration for the client will install a configuration in Apache
that will authenticate via the IdP any attempt to connect to the location named
'/protected', a test file is returned at that location.

In order to successfully install a client 2 steps are necessary:

1. Prepare the client configuration and SAML metadata file.

To generate a valid metadata file and configuration it is necessary to provide
the IdP metadata file  to the installer, it is also useful to decide upfront
where the application to be protected is located.

Let's assume the IdP is a standard install of the Ipsilon server on the server
name ipsilon.example.com, and the client to be installed is called
media.exmple.com with a wiki application located under /wiki

The following command will configure the server and generate the metadata file:

     $ ipsilon-client-install \
     --saml-idp-metadata http://ipsilon.example.com/idp/saml2/metadata \
     --saml-auth /wiki

Use --help to explore all the possible options.

2. Upload the generated metadata file to the IdP.

Once the script has successfully completed installation it will create a
few files in /etc/httpd/saml2/`hostname`. There you will find a (self-signed)
certificate and a private key used to authenticate with the IdP and 2 metadata
files, one of which is called 'metadata.xml'

Log in with the 'admin' account to the Ipsilon server and go to:
 Administration -> Identity Providers -> saml2 -> Administer
Click the 'Add New' button and add a new entry uploading the metadata.xml file
just generated.

Once this is done, test that the authentication is working by going to the
application server url: https://media.example.com/wiki
The SP should redirect you to the IdP server, perform authentication, and then
redirect you automatically back to the application server where you should find
yourself authenticated.

NOTE: read modmellon's documentation to find out how to pass additional
authorization data to the application. For simple authentication the application
should expect a user have been authenticate if it finds a non empty 'REMOTE_USER'
environment variable in the incoming requests.

ALSO NOTE: If your application is already SAML aware you can simply run the
install script with the --saml-no-httpd option. This will generate the
certificates and the metadata.xml file you need to provide to the application
and the IdP in the current directory.


Development with Vagrant
========================

A Vagrant setup is available if you prefer developing on Vagrant VMs. You'll
need the following packages:
- vagrant
- vagrant-libvirt
- vagrant-hostmanager
- vagrant-sshfs

Then just run `vagrant up` and it will build a FreeIPA VM and an Ipsilon VM
for you. The Ipsilon VM comes with the
[test-auth](https://github.com/abompard/test-auth) application to test
authentication methods. Open your browser to http://ipsilon.test/ and you
should see the links.

You can create users in FreeIPA, the admin user has the username `admin` and
the password `password`. For example, you can do:

```
$ echo password | kinit admin
$ ipa user-add --first Foo --last Bar --password foobar
Password:
Enter Password again to verify:
Added user "foobar"
```

You can now login in test-auth with the username `foobar` and the password you
chose.
