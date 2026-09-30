from plone import api
from plone.base.utils import safe_bytes
from plone.memoize.ram import cache

import hashlib
import json
import time
import urllib.request


def _cache_key_translate_content(fun, self, content, source_language, target_language):
    content_hash = hashlib.sha512(safe_bytes(content))
    time_period = time.time() // 3600
    return f"elia-translate-{source_language}-{target_language}-{content_hash.hexdigest()}-{time_period!s}"  # noqa: E501


class ELIATranslationServiceFactory:
    def is_available(self):
        try:
            return api.portal.get_registry_record(
                "cs.translators.elia.e_l_i_a_control_panel.enabled"
            )
        except KeyError:
            return False

    def available_languages(self):
        # Obtain the list of supported languages
        source_languages = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.source_languages",
        )
        target_languages = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.target_languages",
        )

        # Create a list of supported translations
        translation_pairs = [
            (source_lang.lower(), target_lang.lower())
            for source_lang in source_languages
            for target_lang in target_languages
            if source_lang != target_lang
        ]

        return translation_pairs

    @property
    def order(self):
        return api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.order",
        )

    @cache(_cache_key_translate_content)
    def translate_content(self, content, source_language, target_language):

        api_base_url = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.api_base_url",
        )
        api_id = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.api_id",
        )
        api_key = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.api_key",
        )

        timeout = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.timeout",
        )

        translation_engine = api.portal.get_registry_record(
            "cs.translators.elia.e_l_i_a_control_panel.translation_engine",
        )

        url = f"{api_base_url}/translate_string"

        payload = json.dumps({
            "api_id": api_id,
            "api_key": api_key,
            "translation_engine": translation_engine,
            # Language of the original text and target language
            # for the translation: es-eu | eu-es | etc
            "language_pair": f"{source_language}-{target_language}",
            # hardcoded: Content type of the text: txt | html | xml
            "content_type": "html",
            "text": content,
        }).encode("utf-8")

        # Merge HEADERS and ensure Content-Type is set to application/json
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        req = urllib.request.Request(  # noqa: S310
            url,
            data=payload,
            headers=headers,
            method="POST",
        )

        result = urllib.request.urlopen(req, timeout=timeout)  # noqa: S310
        data = json.loads(result.read().decode("utf-8"))

        translated_text = data.get("translated_text", "")
        return translated_text


ELIATranslationService = ELIATranslationServiceFactory()
