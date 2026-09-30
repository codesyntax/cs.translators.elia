from cs.translators.elia.utility import ELIATranslationService
from plone import api
from zope.component import getUtility


PREFIX = "cs.translators.elia.e_l_i_a_control_panel"


def record(name: str) -> str:
    return f"{PREFIX}.{name}"


class TestServiceRegistration:
    def test_utility_is_registered(self, portal):
        from plone.app.multilingual.interfaces import IExternalTranslationService

        service = getUtility(IExternalTranslationService, name="elia")
        assert service is ELIATranslationService

    def test_service_implements_interface_contract(self, portal):
        from plone.app.multilingual.interfaces import IExternalTranslationService

        interface = IExternalTranslationService
        for name in ("is_available", "available_languages", "translate_content"):
            assert name in interface
            assert callable(getattr(ELIATranslationService, name))
        assert isinstance(ELIATranslationService.order, int)


class TestRegistryRecords:
    def test_defaults(self, portal):
        assert (
            api.portal.get_registry_record(record("api_base_url"))
            == "https://mt-api.elhuyar.eus"
        )
        assert api.portal.get_registry_record(record("translation_engine")) == "nmt"
        assert api.portal.get_registry_record(record("api_id")) == ""
        assert api.portal.get_registry_record(record("api_key")) == ""
        assert api.portal.get_registry_record(record("enabled")) is True
        assert api.portal.get_registry_record(record("order")) == 30
        assert api.portal.get_registry_record(record("timeout")) == 10
        assert api.portal.get_registry_record(record("source_languages")) == []
        assert api.portal.get_registry_record(record("target_languages")) == []


class TestIsAvailable:
    def test_reads_enabled_registry_record(self, portal):
        assert ELIATranslationService.is_available() is True

        api.portal.set_registry_record(record("enabled"), False)
        assert ELIATranslationService.is_available() is False


class TestAvailableLanguages:
    def test_reads_language_lists_from_registry(self, portal):
        api.portal.set_registry_record(record("source_languages"), ["eu", "es"])
        api.portal.set_registry_record(record("target_languages"), ["eu", "fr"])

        assert ELIATranslationService.available_languages() == [
            ("eu", "fr"),
            ("es", "eu"),
            ("es", "fr"),
        ]

    def test_empty_when_no_languages_configured(self, portal):
        assert ELIATranslationService.available_languages() == []


class TestOrder:
    def test_reads_order_from_registry(self, portal):
        assert ELIATranslationService.order == 30

        api.portal.set_registry_record(record("order"), 10)
        assert ELIATranslationService.order == 10


class TestControlPanel:
    def test_controlpanel_action_is_registered(self, controlpanel_actions):
        assert "e_l_i_a_control_panel-controlpanel" in controlpanel_actions
