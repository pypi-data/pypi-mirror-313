from typing import List
import os

from .xbrl_generation.ContentDataclasses import ContentDocument

from .xbrl_generation.XbrlProducer import XbrlProducer
from .xbrl_generation.PackageDataclasses import File
from .xbrl_generation.InputData import InputData
from .xbrl_generation.HtmlProducer import HtmlProducer
from .xbrl_generation.TaxonomyProducer import TaxonomyProducer

from .utils.schema_validation import validate_schema

SCHEMA_FOLDER: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "schemas")

def validate_input_data(data: dict) -> None:
    # get schemas
    input_schema_folder = os.path.join(SCHEMA_FOLDER, "input")
    validate_schema(data, "https://xbrl-forge.org/schema/input/wrapper", input_schema_folder)

def load_input_data(data: dict) -> InputData:
    return InputData.from_dict(data)

def create_xbrl(input_data_list: List[InputData], styles: str = None) -> File:
    # load data
    loaded_data: InputData = InputData.combine(input_data_list)
    local_namespace = None
    local_namespace_prefix = None
    local_taxonomy_schema = None
    if loaded_data.taxonomy:
        local_namespace=loaded_data.taxonomy.namespace
        local_namespace_prefix=loaded_data.taxonomy.prefix 
        local_taxonomy_schema=loaded_data.taxonomy.schema_url
    report_files: List[File] = []
    for report in loaded_data.reports:
        if report.inline:
            html_producer: HtmlProducer = HtmlProducer(
                report, 
                styles=styles, 
                local_namespace=local_namespace, 
                local_namespace_prefix=local_namespace_prefix, 
                local_taxonomy_schema=local_taxonomy_schema
            )
            report_files.append(html_producer.create_html())
        else:
            xbrl_producer: XbrlProducer = XbrlProducer(
                report, 
                local_namespace=local_namespace, 
                local_namespace_prefix=local_namespace_prefix, 
                local_taxonomy_schema=local_taxonomy_schema
            )
            report_files.append(xbrl_producer.create_xbrl())
    if not loaded_data.taxonomy:
        return File("reports", contained_files=report_files)
    taxonomy_producer: TaxonomyProducer = TaxonomyProducer(loaded_data.taxonomy)
    return taxonomy_producer.create_files(report_files)