from lxml import etree
from typing import Dict
from os import path
from xml.sax.saxutils import XMLGenerator
import re
from sensestreet.deterministic_anonymization import anonimize_to_name, anonimize_to_hash
from functools import lru_cache
"""
BBXMLAnonymiser
Handles the parsing, anonymizing, and writing of XML files.

Initialization Parameters:
bank_pattern: str - A regular expression pattern used to identify companies related to a bank role in conversation (mapped to "BANK" in final xml).
role_field: str, optional - The XML tag that contains company information for role identification, default is "CompanyName".
bank_value: str, optional - The value to replace the company name with if it matches the bank_pattern, default is "BANK".
"""


class BBXMLAnonymiser:
    def __init__(
        self,
        bank_pattern,
        role_field="CompanyName",
        bank_value="BANK",
    ):
        self.bank_pattern = bank_pattern
        self.role_field = role_field
        self.bank_value = bank_value
        self._xmlwriter = None
        self._current_user = None
        self._inside_user = False
        self.user_generator = FakeUserGenerator()

    def anonymise_xml(self, xml_in, xml_out):
        context = etree.iterparse(xml_in, events=("start", "end"))
        self._inside_user = False
        with open(xml_out, "w", encoding="UTF-8") as fp:
            self._xmlwriter = XMLGenerator(
                fp, encoding="UTF-8", short_empty_elements=False
            )
            self._xmlwriter.startDocument()

            for event, elem in context:
                if event == "start":
                    self._element_start(elem)
                elif event == "end":
                    self._element_end(elem)
                    elem.clear()

            self._xmlwriter.endDocument()

    def _element_start(self, elem):
        self._xmlwriter.startElement(name=elem.tag, attrs=elem.attrib)
        if elem.tag == "User":
            self._inside_user = True

        if self._inside_user and elem.tag == "LoginName" and elem.text:
            self._current_user = self.user_generator.generate_user_data(elem.text)

    def _element_end(self, elem):
        if elem.tag == "LoginName" and elem.text:
            self._current_user = self.user_generator.generate_user_data(elem.text)

        if elem.tag == self.role_field and re.search(
            self.bank_pattern, str(elem.text), flags=re.IGNORECASE
        ):
            elem.text = self.bank_value
            if self._inside_user:
                self._current_user[elem.tag] = self.bank_value
        elif (
            self._inside_user and elem.tag in self.user_generator.elements_to_anonymise
        ):
            self._current_user[f"{elem.tag}_original"] = elem.text
            elem.text = self._current_user[elem.tag]

        if elem.text:
            self._xmlwriter.characters(elem.text)

        self._xmlwriter.endElement(name=elem.tag)
        self._xmlwriter.characters("\n")

        if elem.tag == "User":
            self._inside_user = False
            self._current_user = None


class FakeUserGenerator:
    def __init__(self):
        self.elements_to_anonymise = {
            "LoginName",
            "FirstName",
            "LastName",
            "CompanyName",
            "EmailAddress",
            "UUID",
            "FirmNumber",
            "AccountNumber",
            "CorporateEmailAddress",
        }

    @lru_cache(maxsize=100)
    def generate_user_data(self, login) -> Dict:
        first_name, last_name = anonimize_to_name(login)
        login = anonimize_to_hash(login, short=False)
        company = "ACME"
        email = f"{login}@{company.lower().replace(' ', '').replace(',','').replace('-','')}.com"

        return {
            "FirstName": first_name,
            "LastName": last_name,
            "LoginName": login,
            "EmailAddress": email,
            "UUID": login,
            "FirmNumber": login,
            "AccountNumber": login,
            "CompanyName": company,
            "CorporateEmailAddress": email,
        }


"""
A convenience function to create an instance of BBXMLAnonymiser and anonymize an XML file.

Parameters:
xml_in: str - The input XML file path.
xml_out: str - The output file path where the anonymized XML will be saved.
bank_pattern: str - Regular expression pattern to identify bank side in conversation.
"""


def anonymise_bbg_xml(xml_in, xml_out, bank_pattern):
    anonymiser = BBXMLAnonymiser(bank_pattern=bank_pattern)
    anonymiser.anonymise_xml(xml_in, xml_out)


if __name__ == "__main__":
    anonymise_bbg_xml(
        "./example.xml",
        "./test.xml",
        r"\bbank\b",
    )
