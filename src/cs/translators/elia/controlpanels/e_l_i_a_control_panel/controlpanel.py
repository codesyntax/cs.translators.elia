
from cs.translators.elia import _
from cs.translators.elia.interfaces import IBrowserLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface
from zope import schema

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

    translatabel_css_selector = schema.TextLine(
        title=_(
            "The css selector to choose the content to translate",
        ),
        description=_(
            "",
        ),
        default="body",
        required=False,
        readonly=False,
    )

    language_pairs_to = schema.List(
        title=_(
            "Languages to give as translatable",
        ),
        description=_(
            "",
        ),
        value_type=schema.TextLine(
            title="",
        ),
        default=[],
        required=False,
        readonly=False,
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


ELIAControlPanelView = layout.wrap_form(
    ELIAControlPanel, ControlPanelFormWrapper
)



@adapter(Interface, IBrowserLayer)
class ELIAControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IELIAControlPanel
    configlet_id = "e_l_i_a_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("E L I A Control Panel")
    group = ""
    schema_prefix = "cs.translators.elia.e_l_i_a_control_panel"
