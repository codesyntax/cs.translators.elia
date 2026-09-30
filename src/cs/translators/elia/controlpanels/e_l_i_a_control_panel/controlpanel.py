from cs.translators.elia import _
from cs.translators.elia.interfaces import IBrowserLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IELIAControlPanel(Interface):
    api_base_url = schema.TextLine(
        title=_(
            "The API base url",
        ),
        description=_(
            "",
        ),
        default="https://mt-api.elhuyar.eus",
        required=False,
        readonly=False,
    )
    translation_engine = schema.TextLine(
        title=_(
            "The API engine",
        ),
        description=_(
            "Engine for the language pair: nmt | apertium | apertiumc",
        ),
        default="nmt",
        required=False,
        readonly=False,
    )

    api_id = schema.TextLine(
        title=_(
            "The API id provided by Elhuyar",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    api_key = schema.TextLine(
        title=_(
            "The API key provided by Elhuyar",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    enabled = schema.Bool(
        title=_("Enabled"),
        description=_(
            "If enabled this service will be enabled used to get the translations."
        ),
        required=False,
        default=True,
    )

    order = schema.Int(
        title=_("Order"),
        description=_(
            "Ordering of this service. The lower the sooner this service will be used."
        ),
        default=30,
        required=True,
    )

    source_languages = schema.List(
        title=_("Source languages"),
        description=_("Select which source languages does this service allow"),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"
        ),
    )

    target_languages = schema.List(
        title=_("Target languages"),
        description=_("Select which target languages does this service allow"),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"
        ),
    )

    timeout = schema.Int(
        title=_(
            "Default timeout used when connecting to the translation service",
        ),
        default=10,
        required=True,
        readonly=False,
    )


class ELIAControlPanel(RegistryEditForm):
    schema = IELIAControlPanel
    schema_prefix = "cs.translators.elia.e_l_i_a_control_panel"
    label = _("ELIA Control Panel")


ELIAControlPanelView = layout.wrap_form(ELIAControlPanel, ControlPanelFormWrapper)


@adapter(Interface, IBrowserLayer)
class ELIAControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IELIAControlPanel
    configlet_id = "e_l_i_a_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("E L I A Control Panel")
    group = ""
    schema_prefix = "cs.translators.elia.e_l_i_a_control_panel"
