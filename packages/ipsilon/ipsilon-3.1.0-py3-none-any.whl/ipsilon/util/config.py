# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING

from ipsilon.util.log import Log
import os
import json
import base64
import hashlib
import cherrypy
import six

import filetype


def name_from_image(image):
    if image is None:
        return None

    _type = filetype.image_match(base64.b64decode(image))
    fext = _type.mime.split("/")[1] if _type else None
    m = hashlib.sha1()  # nosec: This file is admin-provided
    m.update(base64.b64decode(image))

    return '%s.%s' % (m.hexdigest(), fext)


def url_from_image(image):
    if image is None:
        return None

    return '%s/cache/%s' % (
        cherrypy.config.get('base.mount', ""),
        name_from_image(image)
    )


class FieldValueError(ValueError):

    def __init__(self, field, *args):
        super(FieldValueError, self).__init__(*args)
        self.field = field

    def __str__(self):
        return ValueError.__str__(self) + ', field: %s' % self.field


class Config(Log):

    def __init__(self, name, *args):
        self.name = name
        self._list = list()
        self._dict = dict()
        for item in args:
            if not isinstance(item, Option):
                raise FieldValueError(self.name, 'Invalid option type for %s'
                                      % repr(item))
            self._list.append(item.name)
            self._dict[item.name] = item
        self.debug('Config(%s) %s' % (self.name, self._dict))

    def __repr__(self):
        return '%s: %s' % (self.__class__, ', '.join(self._list))

    def __str__(self):
        return str(self._list)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if not isinstance(value, Option):
            raise FieldValueError(self.name, 'Invalid type for %s' % value)
        if key != value.name:
            raise NameError('Name mismatch, key=%s but value.name=%s' % (
                key, value.name))
        if key not in self._list:
            self._list.append(key)
        self._dict[key] = value

    def __delitem__(self, key):
        self._list.remove(key)
        del self._dict[key]

    def __iter__(self):
        i = 0
        while i < len(self._list):
            yield self._list[i]
            i += 1

    def __reversed__(self):
        i = len(self._list)
        while i > 0:
            yield self._list[i - 1]
            i -= 1

    def __contains__(self, item):
        return (item in self._dict)

    def iteritems(self):
        i = 0
        while i < len(self._list):
            yield (self._list[i], self._dict[self._list[i]])
            i += 1

    def items(self):
        return [(k, self._dict[k]) for k in self._list]


class Option(Log):

    def __init__(self, name, description, readonly=False):
        self.name = name
        self.description = description
        self._default_value = None
        self._assigned_value = None
        self._readonly = readonly

    def __repr__(self):
        return "%s: %s {%s}, value = %s [def: %s] readonly=%s" % (
            self.__class__,
            self.name,
            self.description,
            self._assigned_value,
            self._default_value,
            self._readonly)

    def __str__(self):
        return '%s=%s' % (self.name, self.get_value())

    def get_value(self, default=True):
        if self._assigned_value is not None:
            return self._assigned_value
        elif default is True:
            return self._default_value
        else:
            return None

    def set_value(self, value):
        self._assigned_value = value

    def export_value(self):
        raise NotImplementedError

    def import_value(self, value):
        raise NotImplementedError

    def _str_export_value(self):
        if self._assigned_value is not None:
            return str(self._assigned_value)
        return None

    def _str_import_value(self, value):
        if not isinstance(value, str):
            raise FieldValueError(self.name, 'Value must be string')
        self._assigned_value = value

    def is_readonly(self):
        return self._readonly


class String(Option):

    def __init__(self, name, description, default_value=None, readonly=False,
                 multiline=False):
        super(String, self).__init__(name, description, readonly=readonly)
        self._default_value = str(default_value)
        self.multiline = multiline

    def set_value(self, value):
        self._assigned_value = str(value)

    def export_value(self):
        return self._str_export_value()

    def import_value(self, value):
        self._str_import_value(value)


class Integer(String):

    def __init__(self, name, description, default_value=None, readonly=False):
        super(Integer, self).__init__(name, description, readonly=readonly)
        self._default_value = int(default_value)

    def _check_value(self, value):
        if not value:
            return
        try:
            int(value)
        except ValueError:
            raise FieldValueError(self.name, 'The value must be an integer')

    def set_value(self, value):
        self._check_value(value)
        if value:
            self._assigned_value = int(value)

    def get_value(self, default=True):
        value = super().get_value(default)
        return int(value) if value is not None else None

    def export_value(self):
        if self._assigned_value is None:
            return None
        return int(self._assigned_value)


class Image(Option):
    """
    An image has two components: the binary blob of the image itself and
    the SHA1 sum of the image.

    We only need the image blob when writing to the cache file or
    updating the database.

    For the purposes of the UI we only need the filename which is
    the SHA1 sum of file type the blob + file type.
    """

    def __init__(self, name, description, default_value=None, readonly=False):
        super(Image, self).__init__(name, description, readonly=readonly)
        self._image = None

        if default_value:
            self._image = default_value

        self._assigned_value = url_from_image(self._image)
        self.__write_cache_file()

    def set_value(self, value):
        if value is None:
            return None

        if os.path.exists(self.__filename()):
            try:
                os.remove(self.__filename())
            except IOError as e:
                self.error('Error removing %s: %s' % (self.__filename(), e))

        self._image = base64.b64encode(value)
        self._assigned_value = url_from_image(value)

    def export_value(self):
        if self._image is None:
            return None

        self.__write_cache_file()
        return base64.b64decode(self._image)

    def import_value(self, value):
        if value is None:
            return None

        if os.path.exists(self.__filename()):
            try:
                os.remove(self.__filename())
            except IOError as e:
                self.error('Error removing %s: %s' % (self.__filename(), e))
        self._image = base64.b64encode(value)
        self._assigned_value = url_from_image(self._image)
        self.__write_cache_file()

    def __filename(self):
        if self._image is None:
            return None

        cdir = cherrypy.config.get('cache_dir', '/var/cache/ipsilon')

        return '%s/%s' % (cdir, name_from_image(self._image))

    def __write_cache_file(self):
        if self._image is None:
            return None

        if not os.path.exists(self.__filename()):
            with open(self.__filename(), 'wb') as imagefile:
                imagefile.write(base64.b64decode(self._image))


class Template(Option):

    def __init__(self, name, description, default_template=None,
                 readonly=False):
        super(Template, self).__init__(name, description, readonly=readonly)
        self._default_value = str(default_template)

    def set_value(self, value):
        self._assigned_value = str(value)

    def templatize(self, args):
        if not args:
            raise FieldValueError(self.name,
                                  'Templatized called w/o arguments')

        return self.get_value() % args

    def export_value(self):
        return self._str_export_value()

    def import_value(self, value):
        self._str_import_value(value)


class List(Option):

    def __init__(self, name, description, default_list=None, readonly=False):
        super(List, self).__init__(name, description, readonly=readonly)
        if default_list:
            self._default_value = default_list
        else:
            self._default_value = []

    def set_value(self, value):
        self._assigned_value = list(value)

    def export_value(self):
        if self._assigned_value:
            return ','.join(self._assigned_value)
        return None

    def import_value(self, value):
        if not isinstance(value, str):
            raise FieldValueError(self.name, 'Value (type: %s) must be string'
                                  % type(value))
        self._assigned_value = [x.strip() for x in value.split(',')]


class ComplexList(List):

    def _check_value(self, value):
        if value is None:
            return
        if not isinstance(value, list):
            raise FieldValueError(self.name,
                                  'The value type must be a list, not "%s"' %
                                  type(value))

    def set_value(self, value):
        self._check_value(value)
        self._assigned_value = value

    def export_value(self):
        if self._assigned_value:
            return json.dumps(self._assigned_value)
        return None

    def import_value(self, value):
        if not isinstance(value, str):
            raise FieldValueError(self.name,
                                  'The value type must be a string, not "%s"' %
                                  type(value))
        jsonval = json.loads(value)
        self.set_value(jsonval)


class MappingList(ComplexList):

    def _check_value(self, value):
        if value is None:
            return
        if not isinstance(value, list):
            raise FieldValueError(self.name,
                                  'The value type must be a list, not "%s"' %
                                  type(value))
        for v in value:
            if not isinstance(v, list):
                raise FieldValueError(self.name,
                                      'Each element must be a list, not "%s"' %
                                      type(v))
            if len(v) != 2:
                raise FieldValueError(self.name,
                                      'Each element must contain 2 values,'
                                      ' not %d' % len(v))

    def import_value(self, value):
        if not isinstance(value, str):
            raise FieldValueError(self.name,
                                  'Value (type: %s) must be string'
                                  % type(value))
        jsonval = json.loads(value)
        self.set_value(jsonval)


class Choice(Option):

    def __init__(self, name, description, allowed=None, default=None,
                 readonly=False):
        super(Choice, self).__init__(name, description, readonly=readonly)
        if allowed:
            self._allowed_values = list(allowed)
        else:
            self._allowed_values = list()
        self._default_value = list()
        if default is None:
            default = []
        for name in default:
            if name not in self._allowed_values:
                raise FieldValueError(
                    self.name,
                    'item [%s] is not in allowed [%s]' % (name, allowed))
            self._default_value.append(name)

    def __repr__(self):
        return "%s: %s {%s}, values = %s d:%s ok:%s" % (self.__class__,
                                                        self.name,
                                                        self.description,
                                                        self._assigned_value,
                                                        self._default_value,
                                                        self._allowed_values)

    def __str__(self):
        return '%s=%s' % (self.name, self.get_value())

    def set_value(self, value):
        if not isinstance(value, list):
            value = [value]
        self._assigned_value = list()
        for val in value:
            if val not in self._allowed_values:
                raise FieldValueError(
                    self.name,
                    'Value "%s" not allowed [%s]' % (val,
                                                     self._allowed_values))
            self._assigned_value.append(val)

        if not self._assigned_value:
            self._assigned_value = None

    def unset_value(self, value):
        if isinstance(value, str):
            value = [value]
        unset = list()
        for val in value:
            unset.append((val, False))
        self.set_value(unset)

    def get_allowed(self):
        return self._allowed_values

    def export_value(self):
        enabled = self.get_value()
        return ', '.join(enabled)

    def import_value(self, value):
        enabled = [x.strip() for x in value.split(',')]
        if enabled:
            if self._assigned_value is None:
                self._assigned_value = list()
        for val in enabled:
            if val not in self._allowed_values:
                # We silently ignore invalid options on import for now
                continue
            self._assigned_value.append(val)


class Pick(Option):

    def __init__(self, name, description, allowed, default_value,
                 readonly=False):
        super(Pick, self).__init__(name, description, readonly=readonly)
        self._allowed_values = list(allowed)
        if default_value not in self._allowed_values:
            raise FieldValueError(
                self.name,
                'The default value is not in the allowed list')
        self._default_value = default_value

    def set_value(self, value):
        if value not in self._allowed_values:
            raise FieldValueError(
                self.name,
                'Value "%s" not allowed [%s]' % (value, self._allowed_values))
        self._assigned_value = value

    def get_allowed(self):
        return self._allowed_values

    def export_value(self):
        return self._str_export_value()

    def import_value(self, value):
        self._str_import_value(value)


class Condition(Pick):

    def __init__(self, name, description, default_value=False,
                 readonly=False):
        # We're not too picky about what data we get, but we make sure it's a
        # boolean by the time we're done with it
        if default_value in ['1', 'True', True]:
            default_value = True
        else:
            default_value = False
        super(Condition, self).__init__(name, description,
                                        [True, False], default_value,
                                        readonly=readonly)

    def import_value(self, value):
        # Convert the text string stored in the database back to a boolean
        if value == 'True':
            self._assigned_value = True
        elif value == 'False':
            self._assigned_value = False


class ConfigHelper(Log):

    def __init__(self):
        self._config = None

    def new_config(self, name, *config_args):
        self._config = Config(name, *config_args)

    def get_config_obj(self):
        if self._config is None:
            raise AttributeError('Config not initialized')
        return self._config

    def import_config(self, config):
        if not self._config:
            raise AttributeError('Config not initialized, cannot import')

        for key, value in six.iteritems(config):
            if key in self._config:
                self._config[key].import_value(str(value))

    def export_config(self):
        config = dict()
        for name, option in self._config.iteritems():
            config[name] = option.export_value()
        return config

    def get_config_value(self, name):
        if not self._config:
            raise AttributeError('Config not initialized')
        return self._config[name].get_value()

    def set_config_value(self, name, value):
        if not self._config:
            raise AttributeError('Config not initialized')
        return self._config[name].set_value(value)
