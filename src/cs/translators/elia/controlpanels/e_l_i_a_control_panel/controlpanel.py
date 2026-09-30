
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
    myfield_name = schema.TextLine(
        title=_(
            "This is an example field for this control panel",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )


class ELIAControlPanel(RegistryEditForm):
    schema = IELIAControlPanel
    schema_prefix = "cs.translators.elia.e_l_i_a_control_panel"
    label = _("E L I A Control Panel")


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
