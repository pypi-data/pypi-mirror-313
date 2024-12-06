#!/usr/bin/python
#
# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING

from lxml import html
import requests
import string
from six.moves.urllib.parse import urlparse, urlencode
import json
from requests_kerberos import HTTPKerberosAuth, OPTIONAL


class WrongPage(Exception):
    pass


class PageTree(object):

    def __init__(self, result):
        self.result = result
        self.text = result.text
        self._tree = None

    @property
    def tree(self):
        if self._tree is None:
            self._tree = html.fromstring(self.text)
        return self._tree

    def first_value(self, rule):
        result = self.tree.xpath(rule)
        if isinstance(result, list):
            if len(result) > 0:
                result = result[0]
            else:
                result = None
        return result

    def all_values(self, rule):
        result = self.tree.xpath(rule)
        if isinstance(result, list):
            return result
        return [result]

    def make_referer(self):
        return self.result.url

    def expected_value(self, rule, expected):
        value = self.first_value(rule)
        if value != expected:
            raise ValueError("Expected [%s], got [%s]" % (expected, value))

    def expected_status(self, expected):
        status = self.result.status_code
        if status != expected:
            raise ValueError("Expected HTTP status [%d], got [%d]" %
                             (expected, status))


class HttpSessions(object):

    def __init__(self):
        self.servers = dict()

    def add_server(self, name, baseuri, user=None, pwd=None):
        new = {'baseuri': baseuri,
               'session': requests.Session()}
        if user:
            new['user'] = user
        if pwd:
            new['pwd'] = pwd
        self.servers[name] = new

    def get_session(self, url):
        for srv in self.servers:
            d = self.servers[srv]
            if url.startswith(d['baseuri']):
                return d['session']

        raise ValueError("Unknown URL: %s" % url)

    def get_idp_uri(self, idp):
        if idp == 'root':
            return ''
        else:
            return '/%s' % idp

    def get(self, url, krb=False, **kwargs):
        session = self.get_session(url)
        allow_redirects = False
        if krb:
            # python-requests-kerberos isn't too bright about doing mutual
            # authentication and it tries to do it on any non-401 response
            # which doesn't work in our case since we follow redirects.
            kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
            kwargs['auth'] = kerberos_auth
            allow_redirects = True
        return session.get(url, allow_redirects=allow_redirects, **kwargs)

    def post(self, url, **kwargs):
        session = self.get_session(url)
        return session.post(url, allow_redirects=False, **kwargs)

    def access(self, action, url, krb=False, **kwargs):
        action = action.lower()
        if action == 'get':
            return self.get(url, krb, **kwargs)
        elif action == 'post':
            return self.post(url, **kwargs)
        else:
            raise ValueError("Unknown action type: [%s]" % action)

    def new_url(self, referer, action):
        if action.startswith('/'):
            u = urlparse(referer)
            return '%s://%s%s' % (u.scheme, u.netloc, action)
        return action

    def get_form_data(self, page, form_id, input_fields):
        form_selector = '//form'
        if form_id:
            form_selector += '[@id="%s"]' % form_id
        values = []
        action = page.first_value('%s/@action' % form_selector)
        values.append(action)
        method = page.first_value('%s/@method' % form_selector)
        values.append(method)
        for field in input_fields:
            value = page.all_values('%s/input/@%s' % (form_selector,
                                                      field))
            values.append(value)
        return values

    def handle_login_form(self, idp, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")

        srv = self.servers[idp]

        try:
            results = self.get_form_data(page, "login_form", ["name", "value"])
            action_url = results[0]
            method = results[1]
            names = results[2]
            values = results[3]
            if action_url is None:
                raise Exception
        except Exception:  # pylint: disable=broad-except
            raise WrongPage("Not a Login Form Page")

        referer = page.make_referer()
        headers = {'referer': referer}
        payload = {}
        for i in range(0, len(names)):
            payload[names[i]] = values[i]

        # replace known values
        payload['login_name'] = srv['user']
        payload['login_password'] = srv['pwd']

        return [method, self.new_url(referer, action_url),
                {'headers': headers, 'data': payload}]

    def handle_return_form(self, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")

        try:
            results = self.get_form_data(page, "saml-response",
                                         ["name", "value"])
            action_url = results[0]
            if action_url is None:
                raise Exception
            method = results[1]
            names = results[2]
            values = results[3]
        except Exception:  # pylint: disable=broad-except
            raise WrongPage("Not a Return Form Page")

        referer = page.make_referer()
        headers = {'referer': referer}

        payload = {}
        for i in range(0, len(names)):
            payload[names[i]] = values[i]

        return [method, self.new_url(referer, action_url),
                {'headers': headers, 'data': payload}]

    def handle_openid_form(self, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")

        if not page.first_value('//title/text()') == \
                'OpenID transaction in progress':
            raise WrongPage('Not OpenID autosubmit form')

        try:
            results = self.get_form_data(page, None,
                                         ["name", "value"])
            action_url = results[0]
            if action_url is None:
                raise Exception
            method = results[1]
            names = results[2]
            values = results[3]
        except Exception:  # pylint: disable=broad-except
            raise WrongPage("Not OpenID autosubmit form")

        referer = page.make_referer()
        headers = {'referer': referer}

        payload = {}
        for i in range(0, len(names)):
            payload[names[i]] = values[i]

        return [method, self.new_url(referer, action_url),
                {'headers': headers, 'data': payload}]

    def handle_openid_consent_form(self, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")

        try:
            results = self.get_form_data(page, "consent_form",
                                         ['name', 'value'])
            action_url = results[0]
            if action_url is None:
                raise Exception
            method = results[1]
            names = results[2]
            values = results[3]
        except Exception:  # pylint: disable=broad-except
            raise WrongPage("Not an OpenID Consent Form Page")

        referer = page.make_referer()
        headers = {'referer': referer}

        payload = {}
        for i in range(0, len(names)):
            payload[names[i]] = values[i]

        # Replace known values
        payload['decided_allow'] = 'Allow'

        return [method, self.new_url(referer, action_url),
                {'headers': headers, 'data': payload}]

    def handle_openidc_form(self, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")

        if not page.first_value('//title/text()') == \
                'Submitting...':
            raise WrongPage('Not OpenIDC autosubmit form')

        url = page.make_referer()
        if '#' not in url:
            raise WrongPage('Not OpenIDC fragment submit page')
        url, arguments = url.split('#', 1)

        arguments = arguments.split('&')
        params = {'response_mode': 'fragment'}
        for argument in arguments:
            key, value = argument.split('=')
            params[key] = value

        return ['post', url, {'data': params}]

    def get_openidc_oob(self, page):
        if not isinstance(page, PageTree):
            raise TypeError("Expected PageTree object")
        result = page.first_value(
            '//div[contains(@class, "ipsilon-oob")]/pre'
        )
        return result.text

    def fetch_page(self, idp, target_url, follow_redirect=True, krb=False,
                   require_consent=None, return_prefix=None, post_forms=True,
                   allowed_codes=(200,)):
        """
        Fetch a page and parse the response code to determine what to do
        next.

        The login process consists of redirections (302/303) and
        potentially an unauthorized (401). For the case of unauthorized
        try the page returned in case of fallback authentication.

        require_consent indicates whether consent should or should not be asked
        or if that's not in this test. None means not tested, False means must
        not be asked, True means must be asked.

        If the url we would be requesting starts with return_prefix, instead of
        requesting the next page, we return the previous page.
        """
        url = target_url
        action = 'get'
        args = {}
        seen_consent = False
        redirects = 0
        r = None

        if follow_redirect is True:
            # Just make sure we get to an end at some point
            follow_redirect = 50

        while True:
            if return_prefix and url.startswith(return_prefix):
                if r:
                    return PageTree(r)
                else:
                    return None
            r = self.access(action, url, krb=krb, **args)
            if r.status_code == 303 or r.status_code == 302:
                if follow_redirect is False or redirects >= follow_redirect:
                    return PageTree(r)
                redirects += 1
                url = r.headers['location']
                action = 'get'
                args = {}
            elif r.status_code == 401:
                page = PageTree(r)
                if r.headers.get('WWW-Authenticate', None) is None:
                    return page

                # Fall back, hopefully to testauth authentication.
                try:
                    if post_forms:
                        (action, url, args) = self.handle_login_form(idp, page)
                        continue
                except WrongPage:
                    pass
            elif r.status_code in allowed_codes:
                page = PageTree(r)

                try:
                    if post_forms:
                        (action, url, args) = self.handle_login_form(idp, page)
                        continue
                except WrongPage:
                    pass

                try:
                    if post_forms:
                        (action, url, args) = self.handle_return_form(page)
                        continue
                except WrongPage:
                    pass

                try:
                    if post_forms:
                        (action, url, args) = self.handle_openid_consent_form(
                            page)
                        seen_consent = True
                        continue
                except WrongPage:
                    pass

                try:
                    if post_forms:
                        (action, url, args) = self.handle_openid_form(page)
                        continue
                except WrongPage:
                    pass

                try:
                    if post_forms:
                        (action, url, args) = self.handle_openidc_form(page)
                        continue
                except WrongPage:
                    pass

                # Either we got what we wanted, or we have to stop anyway
                if (not seen_consent) and require_consent:
                    raise ValueError('IDP did not present consent page, but '
                                     'consent is required.')
                elif seen_consent and (require_consent is False):
                    raise ValueError('IDP presented consent page, but '
                                     'consent is disallowed.')

                return page
            else:
                raise ValueError("Unhandled status (%d) on url %s: %s" % (
                                 r.status_code, url, r.content))

    def auth_to_idp(self, idp, krb=False, rule=None, expected=None):

        srv = self.servers[idp]
        target_url = '%s%s/' % (srv['baseuri'], self.get_idp_uri(idp))

        r = self.access('get', target_url, krb=krb)
        if r.status_code != 200:
            raise ValueError("Access to idp failed: %s" % repr(r))

        page = PageTree(r)
        page.expected_value('//div[@id="content"]/p/a/text()', 'Log In')
        href = page.first_value('//div[@id="content"]/p/a/@href')
        url = self.new_url(target_url, href)

        page = self.fetch_page(idp, url, krb=krb)

        if rule is None:
            rule = '//div[@id="welcome"]/p/text()'
        if expected is None:
            expected = 'Welcome %s!' % srv['user']

        page.expected_value(rule, expected)

    def logout_from_idp(self, idp):

        srv = self.servers[idp]
        target_url = '%s%s/logout' % (srv['baseuri'], self.get_idp_uri(idp))

        r = self.access('get', target_url)
        if r.status_code != 200:
            raise ValueError("Logout from idp failed: %s" % repr(r))

    def get_sp_metadata(self, idp, sp):
        spuri = self.servers[sp]['baseuri']

        return requests.get('%s/saml2/metadata' % spuri)

    def add_sp_metadata(self, idp, sp, rest=False):
        m = self.get_sp_metadata(idp, sp)
        return self.add_metadata(idp, sp, m.content, rest)

    def add_metadata(self, idp, desc, m, rest=False):
        expected_status = 200
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']
        url = '%s%s/admin/providers/saml2/admin/new' % (idpuri,
                                                        self.get_idp_uri(idp))
        headers = {'referer': url}
        if rest:
            expected_status = 201
            payload = {
                'metadata': m,
                'visible': True,
                'description': desc,
                'image': 'Zm9v',
                'splink': 'https://test.example.com/secret/',
            }
            headers['content-type'] = 'application/x-www-form-urlencoded'
            url = '%s%s/rest/providers/saml2/SPS/%s' % (idpuri,
                                                        self.get_idp_uri(idp),
                                                        desc)
            r = self.post(url, headers=headers, data=urlencode(payload))
        else:
            metafile = {'metafile': m}
            payload = {'name': desc}
            r = self.post(url, headers=headers, data=payload, files=metafile)
        if r.status_code != expected_status:
            raise ValueError('Failed to post SP data [%s]: %s' % (repr(r), r.content))

        if not rest:
            page = PageTree(r)
            page.expected_value('//div[@class="alert alert-success"]/p/text()',
                                'SP Successfully added')

    def set_sp_default_nameids(self, idp, sp, nameids):
        """
        nameids is a list of Name ID formats to enable
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']
        url = '%s%s/admin/providers/saml2/admin/sp/%s' % (
            idpuri, self.get_idp_uri(idp), sp)
        headers = {'referer': url}
        headers['content-type'] = 'application/x-www-form-urlencoded'
        payload = {'submit': 'Submit',
                   'allowed_nameids': ', '.join(nameids)}
        r = idpsrv['session'].post(url, headers=headers,
                                   data=payload)
        if r.status_code != 200:
            raise ValueError('Failed to post SP data [%s]' % repr(r))

    # pylint: disable=dangerous-default-value
    def set_attributes_and_mapping(self, idp, mapping=None, attrs=None,
                                   spname=None):
        """
        Set allowed attributes and mapping in the IDP or the SP. In the
        case of the SP both allowed attributes and the mapping need to
        be provided. An empty option for either means delete all values.

        mapping is a list of list of rules of the form:
           [['from-1', 'to-1'], ['from-2', 'from-2']]

        ex. [['*', '*'], ['fullname', 'namefull']]

        attrs is the list of attributes that will be allowed:
           ['fullname', 'givenname', 'surname']
        """
        if mapping is None:
            mapping = []
        if attrs is None:
            attrs = []
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']
        if spname:  # per-SP setting
            url = '%s%s/admin/providers/saml2/admin/sp/%s' % (
                idpuri, self.get_idp_uri(idp), spname)
            mapname = 'Attribute Mapping'
            attrname = 'Allowed Attributes'
        else:  # global default
            url = '%s/%s/admin/providers/saml2' % (idpuri, idp)
            mapname = 'default attribute mapping'
            attrname = 'default allowed attributes'

        headers = {'referer': url}
        headers['content-type'] = 'application/x-www-form-urlencoded'
        payload = {'submit': 'Submit'}
        count = 0
        for m in mapping:
            payload['%s %s-from' % (mapname, count)] = m[0]
            payload['%s %s-to' % (mapname, count)] = m[1]
            count += 1
        count = 0
        for attr in attrs:
            payload['%s %s-name' % (attrname, count)] = attr
            count += 1
        r = idpsrv['session'].post(url, headers=headers,
                                   data=payload)
        if r.status_code != 200:
            raise ValueError('Failed to post IDP data [%s]' % repr(r))

    def update_options(self, idp, relurl, options):
        """
        Update options on a specific page.

        relurl must be the relative url to the admin page, not starting with /.

        options must be a dict of options to change.
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/admin/%s' % (
            idpuri, self.get_idp_uri(idp), relurl)
        headers = {'referer': url}
        r = idpsrv['session'].post(url, data=options, headers=headers)
        if r.status_code != 200:
            raise ValueError('Failed to update settings [%s]' % repr(r))
        if 'alert alert-success' not in r.text:
            raise Exception('No success message returned')
        for key in options:
            if options[key] not in r.text:
                raise Exception('Option value %s (key %s) not found' %
                                (options[key], key))

    def enable_plugin(self, idp, plugtype, plugin):
        """
        Enable a login stack plugin.

        plugtype must be one of 'login', 'info', or 'authz'

        plugin must be the name of the plugin to enable
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/admin/loginstack/%s/enable/%s' % (
            idpuri, self.get_idp_uri(idp), plugtype, plugin)
        rurl = '%s%s/admin/loginstack' % (idpuri, self.get_idp_uri(idp))
        headers = {'referer': rurl}
        r = idpsrv['session'].get(url, headers=headers)
        if r.status_code != 200:
            raise ValueError('Failed to enable plugin [%s]' % repr(r))

    def disable_plugin(self, idp, plugtype, plugin):
        """
        Disable a login stack plugin.

        plugtype must be one of 'login', 'info', or 'authz'

        plugin must be the name of the plugin to enable
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/admin/loginstack/%s/disable/%s' % (
            idpuri, self.get_idp_uri(idp), plugtype, plugin)
        rurl = '%s%s/admin/loginstack' % (idpuri, self.get_idp_uri(idp))
        headers = {'referer': rurl}
        r = idpsrv['session'].get(url, headers=headers)
        if r.status_code != 200:
            raise ValueError('Failed to disable plugin [%s]' % repr(r))

    def set_plugin_order(self, idp, plugtype, order=None):
        """
        Set the order of the specified login stack plugin type.

        plugtype must be one of 'login', 'info', or 'authz'

        order must be a list of zero or more plugin names in order
        """
        if order is None:
            order = []

        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/admin/loginstack/%s/order' % (
            idpuri, self.get_idp_uri(idp), plugtype)
        headers = {'referer': url}
        headers['content-type'] = 'application/x-www-form-urlencoded'
        payload = {'order': ','.join(order)}
        r = idpsrv['session'].post(url, headers=headers, data=payload)
        if r.status_code != 200:
            raise ValueError('Failed to post IDP data [%s]' % repr(r))

    def delete_oidc_client(self, idp, client_id):
        """
        Delete the specified client from the OpenID client list.
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/admin/providers/openidc/admin/client/%s/delete' % (
            idpuri, self.get_idp_uri(idp), client_id)
        headers = {'referer': url}
        headers['content-type'] = 'application/x-www-form-urlencoded'
        r = idpsrv['session'].get(url, headers=headers)
        if r.status_code != 200:
            raise ValueError('Failed to delete client [%s]' % repr(r))
        if client_id in r.text:
            raise ValueError('Client was not gone after deletion')

    def revoke_all_consent(self, idp):
        """
        Revoke user's consent for all clients.
        """
        idpsrv = self.servers[idp]
        idpuri = idpsrv['baseuri']

        url = '%s%s/portal' % (idpuri, self.get_idp_uri(idp))
        headers = {'referer': url}
        r = idpsrv['session'].get(url, headers=headers)
        if r.status_code != 200:
            ValueError('Failed to load user portal [%s]' % repr(r))
        page = PageTree(r)

        revbtns = page.all_values('//a[starts-with(@id, "revoke-")]')

        for btn in revbtns:
            url = '%s%s' % (idpuri, btn.get('href'))
            headers = {'referer': url}
            headers['content-type'] = 'application/x-www-form-urlencoded'

            r = idpsrv['session'].get(url, headers=headers)
            if btn.get('id') in r.text:
                raise ValueError('Client was not gone after revoke')

    def fetch_rest_page(self, idpname, uri):
        """
        idpname - the name of the IDP to fetch the page from
        uri - the URI of the page to retrieve

        The URL for the request is built from known-information in
        the session.

        returns dict if successful
        returns ValueError if the output is unparseable
        """
        baseurl = self.servers[idpname].get('baseuri')
        page = self.fetch_page(
            idpname,
            '%s%s' % (baseurl, uri)
        )
        return json.loads(page.text)

    def get_rest_sp(self, idpname, spname=None):
        if spname is None:
            uri = '%s/rest/providers/saml2/SPS/' % self.get_idp_uri(idpname)
        else:
            uri = '%s/rest/providers/saml2/SPS/%s' % (
                self.get_idp_uri(idpname), spname)

        return self.fetch_rest_page(idpname, uri)
