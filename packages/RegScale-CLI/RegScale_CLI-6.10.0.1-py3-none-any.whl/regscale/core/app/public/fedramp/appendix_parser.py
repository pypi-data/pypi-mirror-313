"""
This module is used to parse a DOCX file containing FedRAMP Security Controls and their implementation statuses.
"""

import logging
import re
import sys
from typing import Dict, Union, Any, List, Optional

import docx
from lxml import etree
from rapidfuzz import fuzz

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCHEMA = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"  # noqa
TEXT_ELEMENT = ".//{%s}%s" % (SCHEMA, "t")
CHECKBOX_ELEMENT = ".//{%s}%s" % (SCHEMA, "checkBox")
NA_STATUS = "Not Applicable"

# define our statuses we are looking for in the document
STATUSES = [
    "Implemented",
    "Partially Implemented",
    "Planned",
    "In Remediation",
    "Inherited",
    "Alternative Implementation",
    NA_STATUS,
    "Archived",
    "Risk Accepted",
]
LOWER_STATUSES = [status.lower() for status in STATUSES]

ORIGINATIONS = [
    "Service Provider Corporate",
    "Service Provider System Specific",
    "Service Provider Hybrid (Corporate and System Specific)",
    "Configured by Customer (Customer System Specific)",
    "Provided by Customer (Customer System Specific)",
    "Shared (Service Provider and Customer Responsibility)",
    "Inherited from pre-existing FedRAMP Authorization",
]
LOWER_ORIGINATIONS = [origin.lower() for origin in ORIGINATIONS]
DEFAULT_ORIGINATION = "Service Provider Corporate"
POSITIVE_KEYWORDS = ["yes", "true", "1", "☒", "True", "Yes", "☑", "☑️"]

# Define your keywords or phrases that map to each status
STATUS_KEYWORDS = {
    "Implemented": ["implemented", "complete", "done", "yes", "☒", "1"],
    "Partially Implemented": [
        "partially implemented",
        "incomplete",
        "partially done",
        "partial",
        "In process",
        "in process",
        "☒",
        "1",
    ],
    "Planned": ["planned", "scheduled", "Planned", "☒", "1"],
    "Alternative Implementation": [
        "alternative implementation",
        "alternative",
        "Equivalent",
        "☒",
        "1",
    ],
    NA_STATUS: ["not applicable", "irrelevant", "not relevant", "no", "☒", "1"],
}
DEFAULT_STATUS = "Not Implemented"
CONTROL_ORIGIN_KEY = "Control Origination"
CONTROL_SUMMARY_KEY = "Control Summary Information"

STATEMENT_CHECK = "What is the solution and how is it implemented".lower()
DEFAULT_PART = "Default Part"


class AppendixAParser:
    """
    A class to parse a DOCX file containing FedRAMP Security Controls and their implementation statuses.
    """

    def __init__(self, filename: str):
        self.controls_implementations = {}
        self.control_id = ""
        self.doc = docx.Document(filename)
        self.header_row_text = ""
        self.cell_data_status = None
        self.processed_texts = []
        self.joined_processed_texts = ""
        self.xml = None
        self.text_elements = None
        self.checkbox_states = None
        self.cell_data = {}
        self.parts = self.generate_parts_full_alphabet()
        self.parts_set = {p.lower() for p in self.parts}

    def fetch_controls_implementations(self) -> Dict:
        """
        Fetch the implementation statuses of the controls from the DOCX file.
        :return: A dictionary containing the control IDs and their implementation statuses.
        :rtype: Dict

        """
        return self.get_implementation_statuses()

    @staticmethod
    def score_similarity(string1: str, string2: str) -> int:
        """
        Score the similarity between two strings using the RapidFuzz library.
        :param str string1: The first string to compare.
        :param str string2: The second string to compare.
        :return: The similarity score between the two strings.
        :rtype: int
        """
        # Scoring the similarity
        score = fuzz.ratio(string1.lower(), string2.lower())

        # Optionally, convert to a percentage
        percentage = score  # fuzz.ratio already gives a score out of 100

        return round(percentage)

    @staticmethod
    def determine_origination(text: str) -> Optional[str]:
        tokens = text.split()
        rejoined_text = " ".join(tokens)  # this removes any newlines or spaces
        rejoined_text = rejoined_text.replace("( ", "(")
        rejoined_text = rejoined_text.replace(" )", ")")

        if CONTROL_ORIGIN_KEY not in text:
            return None
        for origin in ORIGINATIONS:
            for keyword in POSITIVE_KEYWORDS:
                valid_option = f"{keyword} {origin}".lower()
                lower_text = rejoined_text.lower()
                if valid_option in lower_text:
                    return origin  # Return the first matching status
        return None

    @staticmethod
    def determine_status(text: str) -> str:
        # Tokenize the input text
        tokens = text.split()

        # Convert tokens to a single lowercased string for comparison
        token_string = " ".join(tokens).lower()

        matches = []

        # Search for keywords in the tokenized text to determine the status
        for status, keywords in STATUS_KEYWORDS.items():
            for keyword in keywords:
                if f"1 {keyword}" in token_string or f"☒ {keyword}" in token_string:
                    matches.append(status)

        # Determine the status to return
        if len(matches) > 1:
            # More than one match found
            # not applicable takes presendence over planned/partially implemented (only 2 valid multi select statuses for fedramp)
            if matches[1] == NA_STATUS:
                return matches[1]
            else:
                return matches[0]
        elif matches:
            return matches[0]  # Return the first match if only one
        else:
            return DEFAULT_STATUS  # No matches found

    @staticmethod
    def _process_text_element(input_text: str) -> Union[Dict, str]:
        """
        Process a text element from a DOCX cell, checking for structured checkbox information.
        :param str input_text: The text content of the element.
        :return: The processed text or a dictionary containing checkbox information.
        :rtype: Union[Dict, str]
        """
        # Check if the text contains structured checkbox information
        checkbox_info = re.findall(r"\[(.*?): (True|False)\]", input_text)
        if checkbox_info:
            return {item[0].strip(): item[1] == "True" for item in checkbox_info}
        else:
            return input_text

    @staticmethod
    def _get_checkbox_state(checkbox_element: Any) -> bool:
        """
        Get the state of a checkbox element from a DOCX cell.
        :param Any checkbox_element: The checkbox element from the DOCX cell.
        :return: The state of the checkbox.
        :rtype: bool
        """
        # First, try getting the attribute 'val' directly
        val = "{%s}%s" % (SCHEMA, "val")
        checked = "{%s}%s" % (SCHEMA, "checked")
        default = "{%s}%s" % (SCHEMA, "default")
        state = checkbox_element.get(val)
        if state is not None:
            return state == "1"

        # If not found, look for a child element 'checked' that may contain the 'val' attribute
        checked_element = checkbox_element.find(checked)
        if checked_element is not None:
            state = checked_element.get(val)
            return state == "1"

        # If still not found, check for a 'default' state as a fallback
        default_element = checkbox_element.find(default)
        if default_element is not None:
            state = default_element.get(val)
            return state == "1"

        # If there's no indication of the state, return False or handle accordingly
        return False

    def get_implementation_statuses(self) -> Dict:
        """
        Get the implementation statuses of the controls from the DOCX file.
        :return: A dictionary containing the control IDs and their implementation statuses.
        :rtype: Dict
        """
        for table in self.doc.tables:
            for i, row in enumerate(table.rows):
                self._handle_row(i, row)

        logger.debug(f"Found {len(self.controls_implementations.items())} Controls")
        return self.controls_implementations

    def _handle_row(self, i: int, row: Any):
        """
        Handle a row in the DOCX table.
        :param int i: The index of the row.
        :param Any row: The row element from the DOCX table.
        """
        self.header_row_text = " ".join([c.text.strip() for c in row.cells]) if i == 0 else self.header_row_text
        if CONTROL_SUMMARY_KEY.lower() in self.header_row_text.lower():
            self.control_id = self.header_row_text.split(" ")[0] if self.header_row_text else None
            if self.control_id not in self.controls_implementations:
                self.controls_implementations[self.control_id] = {}

        cells = row.cells
        cell_count = len(cells)
        self.handle_row_parts(cells, cell_count)
        for cell_index, cell in enumerate(row.cells):
            self._handle_cell(cell)

    def handle_row_parts(self, cells: Any, cell_count: int) -> None:
        """
        Handle the parts of the control implementation.
        :param Any cells: The cells in the DOCX row.
        :param int cell_count: The number of cells in the row.
        :return: None
        :rtype: None
        """
        check = "what is the solution and how is it implemented".lower()
        if check not in self.header_row_text.lower():
            return
        control_dict = self.controls_implementations.get(self.control_id, {})
        self.handle_part(cells, cell_count, control_dict, check)

    def handle_part(self, cells: Any, cell_count: int, control_dict: Dict, check: str):
        """
        Handle the parts of the control implementation.
        :param Any cells: The cells in the DOCX row.
        :param int cell_count: The number of cells in the row.
        :param Dict control_dict: The dictionary containing the control implementation data.
        :param str check: The check string to exclude from the part value.
        """
        if cell_count > 1:
            name = self.get_cell_text(cells[0]) if cells[0].text else DEFAULT_PART
            value = self.get_cell_text(cells[1])
            part_list = control_dict.get("parts", [])
            val_dict = {"name": name, "value": value}
            if check not in value.lower() and val_dict not in part_list:
                part_list.append(val_dict)
            control_dict["parts"] = part_list
        else:
            value = self.get_cell_text(cells[0])
            value_lower = value.lower()
            pattern = re.compile(r"\b(" + "|".join(re.escape(part) for part in self.parts_set) + r")\b", re.IGNORECASE)
            match = pattern.search(value_lower)
            name = match.group(1) if match else DEFAULT_PART
            part_list = control_dict.get("parts", [])
            val_dict = {"name": name, "value": value}
            if check.lower() not in value_lower and val_dict not in part_list:
                part_list.append(val_dict)
            control_dict["parts"] = part_list

    def set_cell_text(self, cell: Any):
        """
        Set the text content of the cell and process it.
        :param Any cell: The cell element from the DOCX table.
        """
        processed_texts = ""
        self.xml = etree.fromstring(cell._element.xml)
        self.text_elements = self.xml.findall(TEXT_ELEMENT)
        self.checkbox_states = self.xml.findall(CHECKBOX_ELEMENT)
        for element in self.text_elements:
            if element.text:
                processed_texts += self._process_text_element(element.text)
        self.joined_processed_texts = re.sub(r"\.(?!\s|\d|$)", ". ", processed_texts)

    def get_cell_text(self, cell: Any) -> str:
        """
        Get the text content of the cell.
        :param Any cell: The cell element from the DOCX table.
        :return: The text content of the cell.
        :rtype: str
        """
        processed_texts = ""
        xml = etree.fromstring(cell._element.xml)
        text_elements = xml.findall(TEXT_ELEMENT)
        for element in text_elements:
            if element.text:
                processed_texts += self._process_text_element(element.text)
        return re.sub(r"\.(?!\s|\d|$)", ". ", processed_texts)

    def _handle_cell(self, cell: Any):
        """
        Handle a cell in the DOCX table.
        :param Any cell: The cell element from the DOCX table.
        """
        self.set_cell_text(cell)
        self.cell_data = {}
        self._handle_params()
        self.cell_data_status = None
        self._handle_checkbox_states()
        self._handle_implementation_status()
        self._handle_implementation_origination()
        self._handle_implementation_statement()
        # self._handle_implementation_parts(cell_index, cells)
        self._handle_responsibility()

    def _handle_params(self):
        """
        Handle the parameters of the control implementation.
        """
        if (
            CONTROL_SUMMARY_KEY.lower() in self.header_row_text.lower()
            and "parameter" in self.joined_processed_texts.lower()
            and self.control_id in self.controls_implementations
        ):
            control_dict = self.controls_implementations[self.control_id]
            if "parameters" not in control_dict:
                control_dict["parameters"] = []
            # split the first occurrence of : to get the parameter name and value
            parts = self.joined_processed_texts.split(":", 1)
            param_text = self.joined_processed_texts
            param = {"name": "Default Name", "value": "Default Value"}
            if len(parts) == 2:
                param["name"] = parts[0].strip().replace("Parameter", "")
                param["value"] = parts[1].strip()
                if param not in control_dict["parameters"]:
                    control_dict["parameters"].append(param)
            else:
                param["value"] = param_text.replace("parameters", "").strip()
                if param not in control_dict["parameters"]:
                    control_dict["parameters"].append(param)

    def _handle_implementation_origination(self):
        """
        Handle the origination of the control implementation.
        """
        if (
            self.cell_data_status
            and any(
                [self.score_similarity(self.cell_data_status.lower(), origin) > 90 for origin in LOWER_ORIGINATIONS]
            )
            and CONTROL_SUMMARY_KEY.lower() in self.header_row_text.lower()
            and CONTROL_ORIGIN_KEY.lower() in self.joined_processed_texts.lower()
            and self.header_row_text.split(" ")[0] in self.controls_implementations
        ):
            if self.control_id in self.controls_implementations:
                control_dict = self.controls_implementations[self.control_id]
                control_dict["origination"] = self.cell_data_status
        elif origination := self.determine_origination(self.joined_processed_texts):
            if origination in ORIGINATIONS:
                if self.control_id in self.controls_implementations:
                    control_dict = self.controls_implementations[self.control_id]
                    control_dict["origination"] = origination

    def _handle_implementation_status(self):
        """
        Handle the implementation status of the control.
        """
        if (
            self.cell_data_status
            and self.cell_data_status.lower() in LOWER_STATUSES
            and CONTROL_SUMMARY_KEY in self.header_row_text
        ):
            # logger.debug(header_row_text)
            if self.control_id in self.controls_implementations:
                control_dict = self.controls_implementations[self.control_id]
                control_dict["status"] = self.cell_data_status
        elif status := self.determine_status(self.joined_processed_texts):
            if status.lower() in LOWER_STATUSES and CONTROL_SUMMARY_KEY in self.header_row_text:
                if self.control_id in self.controls_implementations:
                    control_dict = self.controls_implementations[self.control_id]
                    control_dict["status"] = status

    def _handle_implementation_statement(self):
        """
        Handle the implementation statement of the control.
        """

        value_check = f"{self.control_id} What is the solution and how is it implemented?"
        if (
            STATEMENT_CHECK in self.header_row_text.lower()
            and value_check.lower() != self.joined_processed_texts.lower()
            and self.control_id in self.controls_implementations
        ):
            control_dict = self.controls_implementations.get(self.control_id, {})
            imp_list = control_dict.get("statement", [])
            if (
                self.joined_processed_texts.strip() != ""
                and STATEMENT_CHECK not in self.joined_processed_texts.strip().lower()
            ):
                imp_list.append(self.joined_processed_texts.strip())
            control_dict["statement"] = imp_list

    @staticmethod
    def generate_parts_full_alphabet() -> List[str]:
        """
        Generates a list of strings in the format "part {letter}"
        for each letter of the alphabet from 'a' to 'z'.

        :return: A list of strings in the format "part {letter}"
        :rtype: List[str]
        """
        # Use chr to convert ASCII codes to letters: 97 is 'a', 122 is 'z'
        parts = [f"part {chr(letter)}" for letter in range(97, 122 + 1)]
        return parts

    def _handle_implementation_parts(self, cell_index: int, cells: Any):
        """
        Handle the implementation statement of the control.
        """
        value_check = f"{self.control_id} What is the solution and how is it implemented?"
        generic_value_check = "What is the solution and how is it implemented".lower()
        if (
            generic_value_check in self.header_row_text.lower()
            and value_check.lower() != self.joined_processed_texts.lower()
            and self.control_id in self.controls_implementations
        ):
            part_value = self.joined_processed_texts.strip()
            control_dict = self.controls_implementations.get(self.control_id, {})
            part_list = control_dict.get("parts", [])
            if any(
                [
                    part_value.strip().lower() == p.lower() or part_value.strip().lower() == f"{p.lower()}:"
                    for p in self.parts
                ]
            ):
                part_name = part_value.strip() or DEFAULT_PART
                next_cell_text = self.get_cell_text(cells[cell_index + 1])
                if ":" not in part_value:
                    part_value = ": ".join(
                        [
                            part_value.strip(),
                            next_cell_text.strip(),
                        ]
                    )
                else:
                    part_value = " ".join([part_value.strip(), next_cell_text.strip()])
                self.build_part_dict(
                    part_name=part_name,
                    part_value=part_value,
                    control_dict=control_dict,
                    part_list=part_list,
                    generic_value_check=generic_value_check,
                )

    def build_part_dict(
        self, part_name: str, part_value: str, control_dict: Dict, part_list: List, generic_value_check: str
    ):
        """
        Build a dictionary for a part of the control implementation.
        :param str part_name: The name of the part.
        :param str part_value: The value of the part.
        :param Dict control_dict: The dictionary containing the control implementation data.
        :param List part_list: The list of parts in the control implementation.
        :param str generic_value_check: The generic value check string.
        """
        if part_value.lower().startswith("part"):
            parts = part_value.split(":", 1)
            part_dict = {"name": part_name, "value": DEFAULT_PART}
            if len(parts) == 2 and parts[1].strip() != "":
                part_dict["name"] = parts[0].strip()
                part_dict["value"] = parts[1].strip()
                logger.debug(f"Part: {part_dict}")
                self.add_to_list(new_dict=part_dict, the_list=part_list)
            elif part_value.strip() != "" and generic_value_check not in part_value.lower():
                part_dict["value"] = part_value.strip()
                self.add_to_list(new_dict=part_dict, the_list=part_list)
        elif generic_value_check not in part_value.lower():
            pdict = {
                "name": DEFAULT_PART,
                "value": part_value.strip(),
            }
            self.add_to_list(new_dict=pdict, the_list=part_list)
        control_dict["parts"] = part_list

    @staticmethod
    def add_to_list(new_dict: Dict, the_list: List):
        """
        Add a value to a list in the control dictionary.
        :param Dict new_dict: The new dictionary to add to the list.
        :param List the_list: The list to add the dictionary to.
        """
        if new_dict not in the_list:
            the_list.append(new_dict)

    def _handle_responsibility(self):
        """
        Handle the responsible roles of the control.
        """
        if (
            CONTROL_SUMMARY_KEY.lower() in self.header_row_text.lower()
            and self.control_id in self.controls_implementations
            and self.joined_processed_texts.lower().startswith("responsible role:")
        ):
            control_dict = self.controls_implementations.get(self.control_id, {})
            parts = self.joined_processed_texts.split(":")
            if len(parts) == 2:
                control_dict["responsibility"] = parts[1].strip()

    def _handle_checkbox_states(self):
        """
        Handle the checkbox states in the DOCX table.
        """
        updated_checkbox_states = [self._get_checkbox_state(state) for state in self.checkbox_states]
        for item in self.processed_texts[1:]:
            if isinstance(item, dict):
                self.cell_data.update(item)
            else:
                self.cell_data[item.strip()] = updated_checkbox_states.pop(0) if updated_checkbox_states else None
            self._get_cell_data_status()

    def _get_cell_data_status(self):
        """
        Get the status of the cell data.
        """
        if self.cell_data != {}:
            for k, v in self.cell_data.items():
                if v:
                    self.cell_data_status = k
