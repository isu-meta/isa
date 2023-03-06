import csv
from io import StringIO
from itertools import zip_longest
from pathlib import Path
from xml.sax.saxutils import escape


def load_csv(csv_file, newline="", delimiter=",", dialect="excel", encoding="utf8"):
    with open(csv_file, "r", newline=newline, encoding=encoding) as fh:
        md = list(csv.DictReader(fh, delimiter=delimiter, dialect=dialect))

    return md


def csv_to_xml(mds):
    return [SpreadsheetMD(md) for md in mds]


def save_xml(xml, output_folder=""):
    file_name = f"{xml.pid.split(':')[-1]}.xml"
    with open(Path(output_folder, file_name), "w", encoding="utf8") as fh:
        fh.write(xml.to_xml())


def save_multiple_xml(xmls, output_folder=""):
    for x in xmls:
        save_xml(x, output_folder)


class SpreadsheetMD:
    def __init__(self, md):
        self.label = md.get("label", "")
        self.binary_file = md.get("binary_file", "")
        self.parent_object = md.get("parent_object", "")
        self.cmodel = md.get("cmodel", "")
        self.pid = md.get("pid", "")
        self.parent_predicate = md.get("parent_predicate", "")
        self.parent_uri = md.get("parent_uri", "")
        self.title = md.get("title", "")
        self.archival_call_number = md.get("archival_call_number", "")
        self.archival_collection = md.get("archival_collection", "")
        self.finding_aid_ark = md.get("finding_aid_ark", "")
        self.physical_location = md.get("physical_location", "")
        self.archival_series_title = md.get("archival_series_title", "")
        self.folder_title = md.get("folder_title", "")
        self.box = md.get("box", "")
        self.folder = md.get("folder", "")
        self.contributing_institution = md.get("contributing_institution", "")
        self.contributing_institution_valueURI = md.get(
            "contributing_institution_valueURI", ""
        )
        self.personal_creator = md.get("personal_creator", "")
        self.corporate_creator = md.get("corporate_creator", "")
        self.interviewee = md.get("interviewee", "")
        self.interviewer = md.get("interviewer", "")
        self.personal_contributor = md.get("personal_contributor", "")
        self.corporate_contributor = md.get("corporate_contributor", "")
        self.personal_creator_valueURI = md.get("personal_creator_valueURI", "")
        self.corporate_creator_valueURI = md.get("corporate_creator_valueURI", "")
        self.interviewee_valueURI = md.get("interviewee_valueURI", "")
        self.interviewer_valueURI = md.get("interviewer_valueURI", "")
        self.personal_contributor_valueURI = md.get("personal_contributor_valueURI", "")
        self.corporate_contributor_valueURI = md.get(
            "corporate_contributor_valueURI", ""
        )
        self.description = md.get("description", "")
        self.disclaimer = md.get("disclaimer", "")
        self.table_of_contents = md.get("table_of_contents", "")
        self.annotation = md.get("annotation", "")
        self.url = md.get("url", "")
        self.language = md.get("language", "")
        self.topical_subject_lcsh = md.get("topical_subject_lcsh", "")
        self.topical_subject_fast = md.get("topical_subject_fast", "")
        self.topical_subject_local = md.get("topical_subject_local", "")
        self.geographic_subject_lcsh = md.get("geographic_subject_lcsh", "")
        self.geographic_subject_fast = md.get("geographic_subject_fast", "")
        self.geographic_subject_local = md.get("geographic_subject_local", "")
        self.geographic_subject_geonames = md.get("geographic_subject_geonames", "")
        self.coordinates = md.get("coordinates", "")
        self.personal_name_subject = md.get("personal_name_subject", "")
        self.corporate_name_subject = md.get("corporate_name_subject", "")
        self.birds_subject = md.get("birds_subject", "")
        self.event_subject = md.get("event_subject", "")
        self.topical_subject_lcsh_valueURI = md.get("topical_subject_lcsh_valueURI", "")
        self.topical_subject_fast_valueURI = md.get("topical_subject_fast_valueURI", "")
        self.topical_subject_local_valueURI = md.get(
            "topical_subject_local_valueURI", ""
        )
        self.geographic_subject_lcsh_valueURI = md.get(
            "geographic_subject_lcsh_valueURI", ""
        )
        self.geographic_subject_fast_valueURI = md.get(
            "geographic_subject_fast_valueURI", ""
        )
        self.geographic_subject_local_valueURI = md.get(
            "geographic_subject_local_valueURI", ""
        )
        self.geographic_subject_geonames_valueURI = md.get(
            "geographic_subject_geonames_valueURI", ""
        )
        self.personal_name_subject_valueURI = md.get(
            "personal_name_subject_valueURI", ""
        )
        self.corporate_name_subject_valueURI = md.get(
            "corporate_name_subject_valueURI", ""
        )
        self.birds_subject_valueURI = md.get("birds_subject_valueURI", "")
        self.event_subject_valueURI = md.get("event_subject_valueURI", "")
        self.chronological_subject = md.get("chronological_subject", "")
        self.extent = md.get("extent", "")
        self.aat_genre = md.get("aat_genre", "")
        self.aat_type = md.get("aat_type", "")
        self.dcmi_type = md.get("dcmi_type", "")
        self.aat_genre_valueURI = md.get("aat_genre_valueURI", "")
        self.aat_type_valueURI = md.get("aat_type_valueURI", "")
        self.dcmi_type_valueURI = md.get("dcmi_type_valueURI", "")
        self.type_of_resource = md.get("type_of_resource", "")
        self.imt_type = md.get("imt_type", "")
        self.cco_description = md.get("cco_description", "")
        self.rights_management = md.get("rights_management", "")
        self.rights_management_valueURI = md.get("rights_management_valueURI", "")
        self.date_original = md.get("date_original", "")
        self.date_digital = md.get("date_digital", "")
        self.place_of_origin = md.get("location_interview", "")
        self.publisher = md.get("publisher", "")
        self.publisher_valueURI = md.get("publisher_valueURI", "")
        self.ark = md.get("ark", "")
        self.local_id = md.get("local_id", "")
        self.avian_id = md.get("avian_id", "")
        self.uid = md.get("uid", "")
        self.project_number = md.get("project_number", "")
        self.file_name = md.get("file_name", "")
        self.date_created = md.get("date_created", "")
        self.date_modified = md.get("date_modified", "")
        self.issuance = md.get("issuance", "")
        self.issuance_start = md.get("issuance_start", "")
        self.issuance_end = md.get("issuance_end", "")
        self.frequency = md.get("frequency", "")
        self.digital_collection = md.get("digital_collection", "")
        self.digital_collection_ark = md.get("digital_collection_ark", "")
        self.related_exhibit = md.get("related_exhibit", "")
        self.related_exhibit_url = md.get("related_exhibit_url", "")
        self.hardware_software = md.get("hardware_software", "")
        self.reformatting_quality = md.get("reformatting_quality", "")
        self.digital_origin = md.get("digital_origin", "")
        self.image_manipulation = md.get("image_manipulation", "")
        self.file_size = md.get("file_size", "")
        self.resolution = md.get("resolution", "")
        self.colorspace = md.get("colorspace", "")
        self.bits_per_sample = md.get("bits_per_sample", "")
        self.samples_per_pixel = md.get("samples_per_pixel", "")
        self.height = md.get("height", "")
        self.width = md.get("width", "")

    def to_xml(self):
        return f"""<?xml version='1.0' encoding='UTF-8'?>
<mods xmlns="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-8.xsd" version="3.8">
  <titleInfo>
    <title>{escape(self.title)}</title>
  </titleInfo>
  <relatedItem type="original" displayLabel="Collection">
    <identifier displayLabel="Call Number">{escape(self.archival_call_number)}</identifier>
    <titleInfo>
      <title>{escape(self.archival_collection)}</title>
    </titleInfo>
    <identifier type="ark">{escape(self.finding_aid_ark)}</identifier>
    <location>
      <physicalLocation>{escape(self.physical_location)}</physicalLocation>
    </location>
    <relatedItem type="series">
    <titleInfo displayLabel="Archival series title">
      <title>{escape(self.archival_series_title)}</title>
    </titleInfo>
    <relatedItem type="constituent">
      <titleInfo displayLabel="Folder title">
        <title>{escape(self.folder_title)}</title>
      </titleInfo>
    </relatedItem>
    </relatedItem>
    <relatedItem type="constituent">
      <titleInfo displayLabel="Box">
        <title>{escape(self.box)}</title>
      </titleInfo>
      <relatedItem type="constituent">
        <titleInfo displayLabel="Folder">
          <title>{escape(self.folder)}</title>
        </titleInfo>
      </relatedItem>
    </relatedItem>
  </relatedItem>
  <relatedItem type="host" displayLabel="Digital Collection">
    <titleInfo>
      <title>{escape(self.digital_collection)}</title>
    </titleInfo>
    <identifier type="ark">{escape(self.digital_collection_ark)}</identifier>
  </relatedItem>
  <relatedItem type="isReferencedBy">
    <titleInfo>
      <title>{escape(self.related_exhibit)}</title>
    </titleInfo>
    <identifier type="ark">{escape(self.related_exhibit_url)}</identifier>
  </relatedItem>
  {self.names_uris_to_xml(self.contributing_institution, self.contributing_institution_valueURI, "corporate", "curator")}
  {self.names_uris_to_xml(self.personal_creator, self.personal_creator_valueURI, "personal", "creator")}
  {self.names_uris_to_xml(self.corporate_creator, self.corporate_creator_valueURI, "corporate", "creator")}
  {self.names_uris_to_xml(self.interviewee, self.interviewee_valueURI, "personal", "interviewee")}
  {self.names_uris_to_xml(self.interviewer, self.interviewer_valueURI, "personal", "interviewer")}
  {self.names_uris_to_xml(self.personal_contributor, self.personal_contributor_valueURI, "personal", "contributor")}
  {self.names_uris_to_xml(self.corporate_contributor, self.corporate_contributor_valueURI, "corporate", "contributor")}
  <originInfo>
    <publisher>{escape(self.publisher)}</publisher>
    <place>
      <placeTerm type="text">{escape(self.place_of_origin)}</placeTerm>
    </place>
    <dateCreated keyDate="yes" encoding="iso8601">{escape(self.date_original)}</dateCreated>
    <dateCaptured encoding="iso8601">{escape(self.date_digital)}</dateCaptured>
{f"    <issuance>{escape(self.issuance)}</issuance>" if self.issuance else ""}
    <dateIssued encoding="iso8601" point="start">{escape(self.issuance_start)}</dateIssued>
    <dateIssued encoding="iso8601" point="end">{escape(self.issuance_end)}</dateIssued>
    <frequency authority="marcfrequency">{escape(self.frequency)}</frequency>
  </originInfo>
  <abstract>{escape(self.description)}</abstract>
  <note type="Disclaimer">{escape(self.disclaimer)}</note>
  <note type="annotation">{escape(self.annotation)}</note>
  <tableOfContents>{escape(self.table_of_contents)}</tableOfContents>
  <language>
    <languageTerm type="code" authority="iso639-3">{escape(self.language)}</languageTerm>
  </language>
  <location>
    <url>{escape(self.url)}</url>
  </location>
  <subject authority="lcsh">
{self.subjects_to_xml(self.topical_subject_lcsh, self.topical_subject_lcsh_valueURI, "topic")}
  </subject>
  <subject authority="fast">
{self.subjects_to_xml(self.topical_subject_fast, self.topical_subject_fast_valueURI, "topic")}
  </subject>
  <subject authority="local">
{self.subjects_to_xml(self.topical_subject_local, self.topical_subject_local_valueURI, "topic")}
  </subject>
  <subject authority="lcsh">
{self.subjects_to_xml(self.birds_subject, self.birds_subject_valueURI, "topic")}
  </subject>
  <subject authority="naf">
{self.subject_names_to_xml(self.personal_name_subject, self.personal_name_subject_valueURI, "personal")}
  </subject>
  <subject authority="naf">
{self.subject_names_to_xml(self.corporate_name_subject, self.corporate_name_subject_valueURI, "corporate")}
  </subject>
{self.geographic_to_xml(self.geographic_subject_lcsh, self.geographic_subject_lcsh_valueURI, self.coordinates, "lcsh")}
{self.geographic_to_xml(self.geographic_subject_fast, self.geographic_subject_fast_valueURI, self.coordinates, "fast")}
{self.geographic_to_xml(self.geographic_subject_geonames, self.geographic_subject_geonames_valueURI, self.coordinates, "geonames")}
{self.geographic_to_xml(self.geographic_subject_local, self.geographic_subject_local_valueURI, self.coordinates, "local")}
  <subject>
{self.subjects_to_xml(self.event_subject, self.event_subject_valueURI, "topic")}
  </subject>
  <subject>
{self.subjects_to_xml(self.chronological_subject, "", "temporal")}
  </subject>
{self.subjects_to_xml(self.aat_genre, self.aat_genre_valueURI, 'genre authority="aat" type="genre"', "  ")}
{self.subjects_to_xml(self.aat_type, self.aat_type_valueURI, 'genre authority="aat"', "  ")}
  <genre authority="cco">{escape(self.cco_description)}</genre>
  <genre authority="dct" valueURI="{escape(self.dcmi_type_valueURI)}">{escape(self.dcmi_type)}</genre>
  <typeOfResource>{escape(self.type_of_resource)}</typeOfResource>
 {self.rights_to_xml(self.rights_management, self.rights_management_valueURI, "  ")}
  <genre authority="imt">{escape(self.imt_type)}</genre>
  <recordInfo>
    <recordCreationDate encoding="iso8601">{escape(self.date_created)}</recordCreationDate>
    <recordChangeDate encoding="iso8601">{escape(self.date_modified)}</recordChangeDate>
  </recordInfo>
  <physicalDescription>
    {'''
    '''.join([f"<extent>{escape(extent.strip())}</extent>" for extent in self.extent.split(";")])}
    {f"<digitalOrigin>{escape(self.digital_origin)}</digitalOrigin>" if self.digital_origin else ""}
    <reformattingQuality>access</reformattingQuality>
    <reformattingQuality>preservation</reformattingQuality>
    <note type="image-manipulation">{escape(self.image_manipulation)}</note>
    <note type="bits-per-sample">{escape(self.bits_per_sample)}</note>
    <note type="samples-per-pixel">{escape(self.samples_per_pixel)}</note>
    <note type="colorspace">{escape(self.colorspace)}</note>
    <note type="resolution">{escape(self.resolution)}</note>
    <note type="file-size">{escape(self.file_size)}</note>
    <note type="height">{escape(self.height)}</note>
    <note type="width">{escape(self.width)}</note>
  </physicalDescription>
  <identifier type="local">{escape(self.local_id)}</identifier>
  <identifier type="ark">{escape(self.ark)}</identifier>
  <identifier type="avian-id">{escape(self.avian_id)}</identifier>
  <identifier type="uid">{escape(self.uid)}</identifier>
  <identifier type="project-number">{escape(self.project_number)}</identifier>
  <identifier>{escape(self.file_name)}</identifier>
  <identifier type="islandora">{escape(self.pid)}</identifier>
  <note type="hardware/software">{escape(self.hardware_software)}</note>
</mods>
"""

    def geographic_to_xml(self, terms, uris, coordinates, authority):
        xml_terms = []
        for t, u, c in zip_longest(
            terms.strip().split(";"),
            uris.strip().split(";"),
            coordinates.strip().split(";"),
            fillvalue="",
        ):
            if t == "":
                return ""
            else:
                xml_terms.append(
                    f"""  <subject authority="{authority}">
    <geographic valueURI="{u.strip()}">{t.strip()}</geographic>
    <cartographics>
      <projection>WGS84</projection>
      <coordinates>{c.strip()}</coordinates>
    </cartographics>
  </subject>"""
                )

        return "\n".join(xml_terms)

    def names_uris_to_xml(self, names, uris, name_type, role, authority="naf"):
        xml_names = []
        for n, u in zip_longest(
            names.strip().split(";"), uris.strip().split(";"), fillvalue=""
        ):
            xml_names.append(
                f"""<name type="{name_type.strip()}" valueURI="{escape(u.strip())}" authority="{escape(authority)}">
    <namePart>{n.strip()}</namePart>
    <role>
    <roleTerm type="text" authority="marcrelator">{role}</roleTerm>
    </role>
  </name>"""
            )

        return "\n".join(xml_names)

    def rights_to_xml(self, rights, uris, indent):
        xml_rights = []
        for r, u in zip_longest(
            rights.strip().split(";"), uris.strip().split(";"), fillvalue=""
        ):
            xml_rights.append(
                f'{indent}<accessCondition type="use and reproduction" valueURI="{escape(u)}">{escape(r)}</accessCondition>'
            )

        return "\n".join(xml_rights)

    def subjects_to_xml(self, terms, uris, term_type, indent="    "):
        xml_terms = []
        term_type_end = term_type.split(" ")[0]
        for t, u in zip_longest(
            terms.strip().split(";"), uris.strip().split(";"), fillvalue=""
        ):
            xml_terms.append(
                f'{indent}<{term_type} valueURI="{u.strip()}">{t.strip()}</{term_type_end}>'
            )

        return "\n".join(xml_terms)

    def subject_names_to_xml(self, names, uris, name_type):
        xml_names = []
        for n, u in zip_longest(
            names.strip().split(";"), uris.strip().split(";"), fillvalue=""
        ):
            xml_names.append(
                f'    <name valueURI="{escape(u.strip())}" type="{name_type}">\n      <namePart>{escape(n.strip())}</namePart>\n    </name>'
            )

        return "\n    ".join(xml_names)
