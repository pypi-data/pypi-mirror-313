from ipsilon.util import config as pconfig
from ipsilon.info.common import InfoProviderBase
from ipsilon.info.infosssd import InfoProvider as SSSDInfoProvider


class InfoProvider(SSSDInfoProvider):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        self.name = "fas"
        self.description = """
A Fedora-specific version of the SSSd info plugin.
"""
        self.new_config(
            self.name,
            pconfig.Condition(
                'preconfigured',
                'FAS can only be used when SSSd is pre-configured',
                False),
            pconfig.String(
                'aws idp arn',
                'The AWS IDP ARN.',
                ''),
            pconfig.MappingList(
                'aws groups',
                'AWS groups mapping',
                []),
        )

    def get_user_attrs(self, user):
        reply = super().get_user_attrs(user)
        reply["_extras"]["awsroles"] = []
        aws_idp_arn = self.get_config_value("aws idp arn")
        if not aws_idp_arn:
            return reply
        aws_groups = dict(self.get_config_value("aws groups"))
        for group in reply["_groups"]:
            if group in aws_groups:
                reply["_extras"]["awsroles"].append(
                    "%s,%s" % (aws_idp_arn, aws_groups[group])
                )
        return reply

    # SSSD disables the admin UI, but we want it.

    def get_config_obj(self):
        return InfoProviderBase.get_config_obj(self)

    def save_plugin_config(self, config=None):
        return InfoProviderBase.save_plugin_config(self, config)
