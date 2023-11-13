import csv
from io import BytesIO, StringIO
from itertools import zip_longest
from pathlib import Path
from xml.sax.saxutils import escape

from lxml import etree
from lxml.builder import E, ElementMaker


def load_csv(csv_file, newline="", delimiter=",", dialect="excel", encoding="utf8"):
    with open(csv_file, "r", newline=newline, encoding=encoding) as fh:
        md = list(csv.DictReader(fh, delimiter=delimiter, dialect=dialect))

    return md


def csv_to_xml(mds):
    return [SpreadsheetMD(md) for md in mds]

def csv_to_xml2(mds):
    return [CsvRow(md) for md in mds]

def save_xml(xml, output_folder=""):
    file_name = f"{xml.pid.split(':')[-1]}.xml"
    with open(Path(output_folder, file_name), "w", encoding="utf8") as fh:
        fh.write(etree.tostring(xml.to_xml()))

def save_xml2(md, schema="mods", output_folder=""):
    parser = etree.XMLParser(remove_blank_text=True)
    file_name = f"{md.pid.split(':')[-1]}.xml" if schema == "mods" else f"dc-{md.pid.split(':')[-1]}.xml"
    xml = md.to_mods() if schema == "mods" else md.to_dc()
    output = etree.parse(
        BytesIO(
            etree.tostring(
                xml,
                xml_declaration=True,
                encoding="UTF-8"
            )
        ),
        parser,
    )
    with open(Path(output_folder, file_name), "w", encoding="utf8") as fh:
        fh.write(
            etree.tostring(
                output,
                pretty_print=True,
                xml_declaration=True,
                encoding="UTF-8",
            ).decode("utf8")
        )


def save_multiple_xml(xmls, output_folder=""):
    for x in xmls:
        save_xml(x, output_folder)

class CsvRow:
    def __init__(self, md):
        self.md = md
        self.mods_root = etree.fromstring(
            b"""<?xml version='1.0' encoding='UTF-8'?>
<mods xmlns="http://www.loc.gov/mods/v3"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-8.xsd" version="3.8">
</mods>"""
        )
        self.mods = self.mods_root
        self.dc_root = etree.fromstring(
            b"""<?xml version="1.0" encoding="UTF-8"?>
<oai_dc:dc xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
           xmlns:srw_dc="info:srw/schema/1/dc-schema"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
</oai_dc:dc>"""
        )
        self.dc = self.dc_root
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
        self.personal_creator = self._get_concatenated_field("personal_creator")
        self.corporate_creator = self._get_concatenated_field("corporate_creator")
        self.interviewee = self._get_concatenated_field("interviewee")
        self.interviewer = self._get_concatenated_field("interviewer")
        self.personal_contributor = self._get_concatenated_field("personal_contributor")
        self.corporate_contributor = self._get_concatenated_field("corporate_contributor")
        self.personal_creator_valueURI = self._get_concatenated_field("personal_creator_valueURI")
        self.corporate_creator_valueURI = self._get_concatenated_field("corporate_creator_valueURI")
        self.interviewee_valueURI = self._get_concatenated_field("interviewee_valueURI")
        self.interviewer_valueURI = self._get_concatenated_field("interviewer_valueURI")
        self.personal_contributor_valueURI = self._get_concatenated_field("personal_contributor_valueURI")
        self.corporate_contributor_valueURI = self._get_concatenated_field("corporate_contributor_valueURI")
        self.description = md.get("description", "")
        self.disclaimer = md.get("disclaimer", "")
        self.table_of_contents = md.get("table_of_contents", "")
        self.transcript = md.get("transcript", "")
        self.annotation = md.get("annotation", "")
        self.url = md.get("url", "")
        self.language = self._get_concatenated_field("language")
        self.topical_subject_lcsh = self._get_concatenated_field("topical_subject_lcsh")
        self.topical_subject_fast = self._get_concatenated_field("topical_subject_fast")
        self.topical_subject_local = self._get_concatenated_field("topical_subject_local")
        self.geographic_subject_lcsh = self._get_concatenated_field("geographic_subject_lcsh")
        self.geographic_subject_fast = self._get_concatenated_field("geographic_subject_fast")
        self.geographic_subject_local = self._get_concatenated_field("geographic_subject_local")
        self.geographic_subject_geonames = self._get_concatenated_field("geographic_subject_geonames")
        self.coordinates = self._get_concatenated_field("coordinates")
        self.personal_name_subject = self._get_concatenated_field("personal_name_subject")
        self.corporate_name_subject = self._get_concatenated_field("corporate_name_subject")
        self.birds_subject = self._get_concatenated_field("birds_subject")
        self.event_subject = self._get_concatenated_field("event_subject")
        self.topical_subject_lcsh_valueURI = self._get_concatenated_field("topical_subject_lcsh_valueURI")
        self.topical_subject_fast_valueURI = self._get_concatenated_field("topical_subject_fast_valueURI")
        self.topical_subject_local_valueURI = self._get_concatenated_field("topical_subject_local_valueURI")
        self.geographic_subject_lcsh_valueURI = self._get_concatenated_field("geographic_subject_lcsh_valueURI")
        self.geographic_subject_fast_valueURI = self._get_concatenated_field("geographic_subject_fast_valueURI")
        self.geographic_subject_local_valueURI = self._get_concatenated_field("geographic_subject_local_valueURI")
        self.geographic_subject_geonames_valueURI = self._get_concatenated_field("geographic_subject_geonames_valueURI")
        self.personal_name_subject_valueURI = self._get_concatenated_field("personal_name_subject_valueURI")
        self.corporate_name_subject_valueURI = self._get_concatenated_field("corporate_name_subject_valueURI")
        self.birds_subject_valueURI = self._get_concatenated_field("birds_subject_valueURI")
        self.event_subject_valueURI = self._get_concatenated_field("event_subject_valueURI")
        self.chronological_subject = self._get_concatenated_field("chronological_subject")
        self.extent = self._get_concatenated_field("extent")
        self.aat_genre = self._get_concatenated_field("aat_genre")
        self.aat_type = self._get_concatenated_field("aat_type")
        self.dcmi_type = self._get_concatenated_field("dcmi_type")
        self.aat_genre_valueURI = self._get_concatenated_field("aat_genre_valueURI")
        self.aat_type_valueURI = self._get_concatenated_field("aat_type_valueURI")
        self.dcmi_type_valueURI = self._get_concatenated_field("dcmi_type_valueURI")
        self.type_of_resource = self._get_concatenated_field("type_of_resource")
        self.imt_type = md.get("imt_type", "")
        self.cco_description = md.get("cco_description", "")
        self.rights_management = self._get_concatenated_field("rights_management")
        self.rights_management_valueURI = self._get_concatenated_field("rights_management_valueURI")
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

        self.dc_namespace = "http://purl.org/dc/elements/1.1/"
        self.dc_nsmap = {"dc": "http://purl.org/dc/elements/1.1/"}
        self.dc_E = ElementMaker(namespace=self.dc_namespace, nsmap=self.dc_nsmap)
        self.dc_separator = "; "

    def _get_concatenated_field(self, field):
        return [m.strip() for m in self.md.get(field, "").split(";")]

    def _list_not_empty(self, lst):
        return bool([x for x in lst if x != ""])

    def _mods_object_title(self, update=True):
        object_title = E.titleInfo(
            E.title(escape(self.title))
        )

        if update:
            self.mods.append(object_title)

        return object_title

    def _mods_physical_collection(self, update=True):
        if (
                self.archival_call_number or
                self.archival_collection or
                self.finding_aid_ark or
                self.physical_location or
                self.archival_series_title or
                self.folder_title or
                self.box or
                self.folder
        ):
            physical_collection = E.relatedItem(
                type="original",
                displayLabel="Collection",
            )

            if self.archival_call_number:
                physical_collection.append(
                    E.identifier(
                        escape(self.archival_call_number),
                        displayLabel="Call Number",
                    )
                )
            if self.archival_collection:
                physical_collection.append(
                    E.titleInfo(
                        E.title(escape(self.archival_collection))
                    )
                )
            if self.finding_aid_ark:
                physical_collection.append(
                    E.identifier(
                        escape(self.finding_aid_ark),
                        type="ark",
                    )
                )
            if self.physical_location:
                physical_collection.append(
                    E.location(
                        E.physicalLocation(
                            escape(self.physical_location)
                        )
                    )
                )
            if self.archival_series_title:
                physical_collection.append(
                    E.relatedItem(
                        E.titleInfo(
                            E.title(
                                escape(self.archival_series_title)
                            ),
                            displayLabel="Archival series title",
                        ),
                        type="series",
                    )
                )
            if self.folder_title:
                physical_collection.append(
                    E.relatedItem(
                        E.titleInfo(
                            E.title(
                                escape(self.folder_title),
                            )
                        ),
                        type="constituent",
                    )
                )
            if self.box or self.folder:
                if self.box:
                    box = E.relatedItem(
                        E.titleInfo(
                            E.title(
                                escape(self.box)
                            ),
                        ),
                        type="constituent",
                        displayLabel="Box",
                    )
                else:
                    box = E.relatedItem(
                        type="constituent",
                        displayLabel="Box",
                    )

                    if self.folder:
                        box.append(
                            E.relatedItem(
                                E.titleInfo(
                                    E.title(


                                        escape(self.folder)
                                    ),
                                    displayLabel="Folder",
                                ),
                            type="constituent",
                            )
                        )

            if update:
                self.mods.append(physical_collection)

            return physical_collection

        return None

    def _mods_digital_collection(self, update=True):
        digital_collection = E.relatedItem(
            E.titleInfo(
                E.title(escape(self.digital_collection))
            ),
            E.identifier(
                escape(self.digital_collection_ark),
                type="ark",
            ),
            type="host",
            displayLabel="Digital Collection",
        )

        if update:
            self.mods.append(digital_collection)

        return digital_collection

    def _mods_digital_exhibit(self, update=True):
        if self.related_exhibit or self.related_exhibit_url:
            digital_exhibit = E.relatedItem(
                type="isReferencedBy",
            )
            if self.related_exhibit:
                digital_exhibit.append(
                    E.titleInfo(
                        E.title(escape(self.related_exhibit))
                    )
                )
            if self.related_exhibit_url:
                digital_exhibit.append(
                    E.identifier(
                        escape(self.related_exhibit_url),
                        type="ark",
                    )
                )

            if update:
                self.mods.append(digital_exhibit)
            return digital_exhibit
        return None

    def _mods_names(self, names, value_uris, _type, authority, role, update=True):
        returnables = []
        for name, uri in zip_longest(names, value_uris, fillvalue=""):
            element = E.name(
                E.namePart(escape(name)),
                E.role(
                    E.roleTerm(
                        role,
                        type="text",
                        authority="marcrelator",
                    )
                ),
                type=_type,
                authority=authority,
            )
            if uri:
                element.attrib["valueURI"] = uri

            returnables.append(element)
            if update:
                self.mods.append(element)

        return returnables

    def _mods_contributing_institution(self, update=True):
        contributing_institution = self._mods_names(
            [self.contributing_institution],
            [self.contributing_institution_valueURI],
            "corporate",
            "naf",
            "curator",
            update,
        )

        return contributing_institution

    def _mods_creators_contributors(self, update=True):
        returnables = []
        if self._list_not_empty(self.personal_creator):
            personal_creators = self._mods_names(
                self.personal_creator,
                self.personal_creator_valueURI,
                "personal",
                "naf",
                "creator",
                update,
            )
            returnables.append(personal_creators)
        if self._list_not_empty(self.corporate_creator):
            corporate_creators = self._mods_names(
                self.corporate_creator,
                self.corporate_creator_valueURI,
                "corporate",
                "naf",
                "creator",
                update,
            )
            returnables.append(corporate_creators)
        if self._list_not_empty(self.interviewee):
            interviewees = self._mods_names(
                self.interviewee,
                self.interviewee_valueURI,
                "personal",
                "naf",
                "interviewee",
                update,
            )
            returnables.append(interviewees)
        if self._list_not_empty(self.interviewer):
            interviewers = self._mods_names(
                self.interviewer,
                self.interviewer_valueURI,
                "personal",
                "naf",
                "interviewer",
                update,
            )
            returnables.append(interviewers)
        if self._list_not_empty(self.personal_contributor):
            personal_contributors = self._mods_names(
                self.personal_contributor,
                self.personal_contributor_valueURI,
                "personal",
                "naf",
                "contributor",
                update,
            )
            returnables.append(personal_contributors)
        if self._list_not_empty(self.corporate_contributor):
            corporate_contributors = self._mods_names(
                self.corporate_contributor,
                self.corporate_contributor_valueURI,
                "corporate",
                "naf",
                "contributor",
                update,
            )
            returnables.append(corporate_contributors)
        return returnables

    def _mods_origin_info(self, update=True):
        origin_info = E.originInfo()
        if self.publisher:
            origin_info.append(escape(self.publisher))
        if self.place_of_origin:
            origin_info.append(
                E.place(
                    E.placeTerm(
                        escape(self.place_of_origin),
                        type="text",
                    )
                )
            )
        if self.date_original:
            origin_info.append(
                E.dateCreated(
                    escape(self.date_original),
                    keyDate="yes",
                    encoding="iso8601",
                )
            )

        if self.date_digital:
            origin_info.apppend(
                E.dateCaptured(
                    escape(self.date_digital),
                    encoding="iso8601",
                )
            )

        if self.issuance:
            origin_info.append(
                E.issuance(
                    escape(self.issuance)
                )
            )
        if self.issuance_start:
            origin_info.append(
                escape(self.issuance_start),
                encoding="iso8601",
                point="start",
            )
        if self.issuance_end:
            origin_info.append(
                escape(self.issuance_end),
                encoding="iso8601",
                point="end",
            )
        if self.frequency:
            origin_info.append(
                escape(self.frequency),
                authority="marcfrequency",
            )

        if update:
            self.mods.append(origin_info)

        return origin_info

    def _mods_notes(self, update=True):
        notes = []
        if self.description:
            notes.append(
                E.abstract(escape(self.description))
            )
        if self.disclaimer:
            notes.append(
                E.note(
                    escape(self.disclaimer),
                    type="disclaimer",
                )
            )
        if self.annotation:
            notes.append(
                E.note(
                    escape(self.annotation),
                    type="annotation",
                )
            )
        if self.table_of_contents:
            notes.append(
                E.tableOfContents(
                    escape(self.table_of_contents),
                )
            )

        if update:
            for element in notes:
                self.mods.append(element)

        return notes

    def _mods_language(self, update=True):
        if self.language:
            languages = []
            for lang in self.language:
                languages.append(
                    E.language(
                        E.languageTerm(
                            escape(lang),
                            type="code",
                            authority="iso639-3",
                            )
                        )
                )
            if update:
                for lang in languages:
                    self.mods.append(lang)
            return languages

        return None

    def _mods_url(self, update=True):
        if self.url:
            url = E.location(
                E.url(escape(self.url))
            )
            if update:
                self.mods.append(url)
            return url

        return None

    def _mods_subject_elements(self, subjects, subject_value_uris, kind, authority):
        root = E.subject()
        if authority:
            root.attrib["authority"] = authority
        for sub, uri in zip_longest(subjects, subject_value_uris, fillvalue=""):
            element = E._makeelement(kind)
            element.text = sub
            if uri:
                element.attrib["valueURI"] = uri
            root.append(element)
        return root

    def _mods_subject_name_elements(self, names, name_value_uris, kind, authority):
        root = E.subject()
        if authority:
            root.attrib["authority"] = authority
        for name, uri in zip_longest(names, name_value_uris, fillvalue=""):
            element = E.name(
                E.namePart(name),
                type=kind,
            )
            if uri:
                element.attrib["valueURI"] = uri
            root.append(element)
        return root

    def _mods_subject_geographic_elements(self, subjects, subject_value_uris, coordinates, authority):
        root = E.subject()
        if authority:
            root.attrib["authority"] = authority
        for sub, uri, coord in zip_longest(subjects, subject_value_uris, coordinates, fillvalue=""):
            element = E.geographic(sub)
            if uri:
                element.attrib["valueURI"] = uri
            if coord:
                element.append(
                    E.cartographics(
                        E.projection("WGS84"),
                        E.coordinates(coord),
                    )
                )
            root.append(element)
        return root

    def _mods_subjects(self, update=True):
        subjects = []
        if self._list_not_empty(self.topical_subject_lcsh):
            subjects.append(
                self._mods_subject_elements(
                    self.topical_subject_lcsh,
                    self.topical_subject_lcsh_valueURI,
                    "topic",
                    "lcsh",
                )
            )
        if self._list_not_empty(self.topical_subject_fast):
            subjects.append(
                self._mods_subject_elements(
                    self.topical_subject_fast,
                    self.topical_subject_fast_valueURI,
                    "topic",
                    "fast",
                )
            )
        if self._list_not_empty(self.topical_subject_local):
            subjects.append(
                self._mods_subject_elements(
                    self.topical_subject_local,
                    self.topical_subject_local_valueURI,
                    "topic",
                    "local",
                )
            )
        if self._list_not_empty(self.birds_subject):
            subjects.append(
                self._mods_subject_elements(
                    self.birds_subject,
                    self.birds_subject_valueURI,
                    "topic",
                    "lcsh",
                )
            )
        if self._list_not_empty(self.personal_name_subject):
            subjects.append(
                self._mods_subject_name_elements(
                    self.personal_name_subject,
                    self.personal_name_subject_valueURI,
                    "personal",
                    "naf",
                )
            )
        if self._list_not_empty(self.corporate_name_subject):
            subjects.append(
                self._mods_subject_name_elements(
                    self.corporate_name_subject,
                    self.corporate_name_subject_valueURI,
                    "corporate",
                    "naf",
                )
            )
        if self._list_not_empty(self.event_subject):
            subjects.append(
                self._mods_subject_elements(
                    self.event_subject,
                    self.event_subject_valueURI,
                    "topic",
                    "",
                )
            )
        if self._list_not_empty(self.chronological_subject):
            subjects.append(
                self._mods_subject_elements(
                    self.chronological_subject,
                    [],
                    "temporal",
                    "",
                )
            )

        if update:
            for sub in subjects:
                self.mods.append(sub)

        return subjects

    def _mods_genre_elements(self, genres, value_uris, authority, kind=""):
        elements = []
        for genre, uri in zip_longest(genres, value_uris, fillvalue=""):
            element = E.genre(genre)
            if authority:
                element.attrib["authority"] = authority
            if uri:
                element.attrib["valueURI"] = uri
            elements.append(element)
        return elements

    def _mods_genre_type(self, update=True):
        genres = []
        if self._list_not_empty(self.aat_genre):
            genres.extend(self._mods_genre_elements(self.aat_genre, self.aat_genre_valueURI, "aat", "genre"))
        if self._list_not_empty(self.aat_type):
            genres.extend(self._mods_genre_elements(self.aat_type, self.aat_type_valueURI, "aat"))
        if self.cco_description:
            genres.extend(self._mods_genre_elements(self.cco_description, [], "cco"))
        if self._list_not_empty(self.dcmi_type):
            genres.extend(self._mods_genre_elements(self.dcmi_type, self.dcmi_type_valueURI, "dct"))
        if self._list_not_empty(self.type_of_resource):
            for tor in self.type_of_resource:
                genres.append(E.typeOfResource(escape(tor)))
        if self.imt_type:
            genres.append(E.genre(self.imt_type, authority="imt"))

        if update:
            for genre in genres:
                self.mods.append(genre)

        return genres

    def _mods_rights(self, update=True):
        rights = []
        if self._list_not_empty(self.rights_management):
            for statement, uri in zip_longest(self.rights_management, self.rights_management_valueURI, fillvalue=""):
                element = E.accessCondition(escape(statement))
                if uri:
                    element.attrib["valueURI"] = uri
                rights.append(element)

        if update:
            for right in rights:
                self.mods.append(right)

        return rights

    def _mods_record_info(self, update=True):
        record_info = E.recordInfo()
        if self.date_created:
            record_info.append(
                E.recordCreationDate(
                    escape(self.date_created),
                    encoding="iso8601",
                )
            )
        if self.date_modified:
            record_info.append(
                E.recordChangeDate(
                    escape(self.date_modified),
                    encoding="iso8601",
                )
            )

        if update:
            self.mods.append(record_info)

        return record_info

    def _mods_physical_description(self, update=True):
        physical_description = E.physicalDescription()
        if self.extent:
            for extent in self.extent:
                physical_description.append(
                    E.extent(escape(extent))
                )
        if self.digital_origin:
            physical_description.append(E.digitalOrigin(escape(self.digital_origin)))
        physical_description.append(E.reformattingQuality("access"))
        physical_description.append(E.reformattingQuality("preservation"))
        if self.image_manipulation:
            physical_description.append(E.note(escape(self.image_manipulation), type="image-manipulation"))
        if self.bits_per_sample:
            physical_description.append(E.note(escape(self.bits_per_sample), type="bits-per-sample"))
        if self.samples_per_pixel:
            physical_description.append(E.note(escape(self.samples_per_pixel), type="samples-per-pixel"))
        if self.colorspace:
            physical_description.append(E.note(escape(self.colorspace), type="colorspace"))
        if self.resolution:
            physical_description.append(E.note(escape(self.resolution), type="resolution"))
        if self.file_size:
            physical_description.append(E.note(escape(self.file_size), type="file-size"))
        if self.height:
            physical_description.append(E.note(escape(self.height), type="height"))
        if self.width:
            physical_description.append(E.note(escape(self.width), type="width"))

        hardware_software = E.note(escape(self.hardware_software), type="hardware/software") if self.hardware_software else None

        if update:
            if physical_description.getchildren():
                self.mods.append(physical_description)

            if hardware_software is not None:
                self.mods.append(hardware_software)

        return physical_description, hardware_software

    def _mods_identifiers(self, update=True):
        identifiers = []
        if self.ark:
            identifiers.append(E.identifier(escape(self.ark), type="ark"))
        if self.local_id:
            identifiers.append(E.identifier(escape(self.local_id), type="local"))
        if self.avian_id:
            identifiers.append(E.identifier(escape(self.avian_id), type="avian-id"))
        if self.uid:
            identifiers.append(E.identifier(escape(self.uid), type="uid"))
        if self.project_number:
            identifiers.append(E.identifier(escape(self.project_number), type="project-number"))
        if self.file_name:
            identifiers.append(E.identifier(escape(self.file_name)))
        if self.pid:
            identifiers.append(E.identifier(escape(self.pid), type="islandora"))

        if update:
            for ident in identifiers:
                self.mods.append(ident)

        return identifiers

    def _dc_add_fields(self, element, fields, update=True):
        e = self.dc_E
        output_items = []
        for field in fields:
            if field:
                output = e._makeelement(f"{{http://purl.org/dc/elements/1.1/}}{element}", nsmap=self.dc_nsmap)
                output.text = escape(field)
                output_items.append(output)
                if update:
                    self.dc.append(output)
        if output_items:
            return output_items
        return None

    def _dc_add_multiple_paired_fields(self, element, fields, update=True):
        e = self.dc_E
        output = []
        for field in fields:
            for pair in field:
                item = e._makeelement(f"{{http://purl.org/dc/elements/1.1/}}{element}", nsmap=self.dc_nsmap)
                if pair[1]:
                    item.text = escape(self.dc_separator.join(pair))
                else:
                    item.text = escape(pair[0])
                output.append(item)
        if update:
            for item in output:
                self.dc.append(item)

        return output

    def _dc_add_single_field(self, element, content, update=True):
        e = self.dc_E
        if content:
            item = e._makeelement(f"{{http://purl.org/dc/elements/1.1/}}{element}", nsmap=self.dc_nsmap)
            item.text = escape(content)
            if update:
                self.dc.append(item)
            return item
        return None

    def _dc_add_multiple_single_fields(self, element, content, update=True):
        return [self._dc_add_single_field(element, c, update) for c in content]

    def _zip(self, one, two, fillvalue=""):
        return list(zip_longest(one, two, fillvalue=fillvalue))

    def _alternate_fields(self, one, two, fillvalue=""):
        # Primarily added to allow for alternating text and URI fields.
        # Alternating fields allow for related URI/string pairs to appear
        # next to one another in the DC output.
        #
        # DPLA requires rights URIs and allows for the addition of a matching
        # string rights statement. (https://docs.google.com/document/d/1aInokOIIsgf-B4iMTXU33qYN5B2jA3s91KgWoh7DZ7Q/edit#heading=h.ma4e226diad0)
        # For best quality metadata, DPLA recommends including URIs in
        # addition to string values. (https://docs.google.com/document/d/1dITqEYEWsMX1a2pLPmkL78k1LN2b4im03spn8_QFscY/edit)
        #
        # Because the string value is secondary in the case of rights statements,
        # URIs should appear first.
        #
        # Because the URI value is seconary for other controlled fields, the
        # text should appear first all other controlled fields.
        return [
            item
            for pair
            in self._zip(
                one,
                two,
                fillvalue=fillvalue,
            )
            for item
            in pair
        ]

    def _dc_title(self, update=True):
        e = self.dc_E
        title = e.title(escape(self.title))

        if update:
            self.dc.append(title)

        return title

    def _dc_source(self, update=True):
        source_elements = [
            self.archival_collection,
            self.finding_aid_ark,
            self.archival_call_number,
        ]
        return self._dc_add_fields("source", source_elements, update)

    def _dc_relation(self, update=True):
        relation_elements = [
            self.digital_collection,
            self.digital_collection_ark,
        ]

        return self._dc_add_fields("relation", relation_elements, update)

    def _dc_publisher(self, update=True):
        return self._dc_add_fields("publisher", [self.contributing_institution, self.contributing_institution_valueURI], update)

    def _dc_creator(self, update=True):
        creator_bits = [
            *self._alternate_fields(self.interviewee, self.interviewee_valueURI),
            *self._alternate_fields(self.interviewer, self.interviewer_valueURI),
            *self._alternate_fields(self.personal_creator, self.personal_creator_valueURI),
            *self._alternate_fields(self.corporate_creator, self.corporate_creator_valueURI),
        ]
        return self._dc_add_fields("creator", creator_bits, update)

    def _dc_contributor(self, update=True):
        contributor_bits = [
            *self._alternate_fields(self.personal_contributor, self.personal_contributor_valueURI),
            *self._alternate_fields(self.corporate_contributor, self.corporate_contributor_valueURI),
        ]
        return self._dc_add_multiple_paired_fields("contributor", contributor_bits, update)


    def _dc_date(self, update=True):
        return self._dc_add_single_field("date", self.date_original, update)

    def _dc_language(self, update=True):
        return self._dc_add_multiple_single_fields("language", self.language, update)

    def _dc_description(self, update=True):
        return self._dc_add_single_field("description", self.description, update)

    def _dc_subject(self, update=True):
        subject_bits = [
            *self._alternate_fields(self.topical_subject_lcsh, self.topical_subject_lcsh_valueURI),
            *self._alternate_fields(self.topical_subject_fast, self.topical_subject_fast_valueURI),
            *self._alternate_fields(self.topical_subject_local, self.topical_subject_local_valueURI),
            *self._alternate_fields(self.birds_subject, self.birds_subject_valueURI),
            *self._alternate_fields(self.event_subject, self.event_subject_valueURI),
            *self._alternate_fields(self.personal_name_subject, self.personal_name_subject_valueURI),
            *self._alternate_fields(self.corporate_name_subject, self.corporate_name_subject_valueURI),
        ]
        return self._dc_add_fields("subject", subject_bits, update)

    def _dc_coverage(self, update=True):
        coverage_bits = [
            *self._alternate_fields(self.geographic_subject_lcsh, self.geographic_subject_lcsh_valueURI),
            *self._alternate_fields(self.geographic_subject_fast, self.geographic_subject_fast_valueURI),
            *self._alternate_fields(self.geographic_subject_local, self.geographic_subject_local_valueURI),
            *self._alternate_fields(self.geographic_subject_geonames, self.geographic_subject_geonames_valueURI),
            *self._alternate_fields(self.chronological_subject, []),
        ]
        return self._dc_add_fields("coverage", coverage_bits, update)

    def _dc_type(self, update=True):
        types = [
            *self._alternate_fields(self.aat_genre, self.aat_genre_valueURI),
            *self._alternate_fields(self.aat_type, self.aat_type_valueURI),
            *self._alternate_fields(self.dcmi_type, self.dcmi_type_valueURI),
        ]
        return self._dc_add_fields("type", types, update)

    def _dc_rights(self, update=True):
        rights_bits = self._alternate_fields(self.rights_management_valueURI, self.rights_management)
        return self._dc_add_fields("rights", rights_bits, update)

    def _dc_format(self, update=True):
        return self._dc_add_multiple_single_fields("format", self.extent, update)

    def _dc_identifier(self, update=True):
        identifiers = [
            self.ark,
            self.local_id,
            self.file_name,
            self.avian_id,
            self.uid,
            self.project_number,
        ]
        return self._dc_add_multiple_single_fields("identifier", identifiers, update)

    def to_mods(self):
        self.mods = self.mods_root
        self._mods_object_title()
        self._mods_physical_collection()
        self._mods_digital_collection()
        self._mods_digital_exhibit()
        self._mods_contributing_institution()
        self._mods_creators_contributors()
        self._mods_origin_info()
        self._mods_notes()
        self._mods_language()
        self._mods_url()
        self._mods_subjects()
        self._mods_genre_type()
        self._mods_rights()
        self._mods_record_info()
        self._mods_physical_description()
        self._mods_identifiers()

        return self.mods

    def to_dc(self):
        self.dc = self.dc_root
        self._dc_title()
        self._dc_source()
        self._dc_relation()
        self._dc_publisher()
        self._dc_creator()
        self._dc_contributor()
        self._dc_date()
        self._dc_description()
        self._dc_language()
        self._dc_subject()
        self._dc_coverage()
        self._dc_type()
        self._dc_rights()
        self._dc_format()
        self._dc_identifier()

        return self.dc

class SpreadsheetMD:
    def __init__alternate_fields(self, md):
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
        self.transcript = md.get("transcript", "")
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
{self.subject_names_to_xml(escape(self.corporate_name_subject), self.corporate_name_subject_valueURI, "corporate")}
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
{self.dcmi_to_xml(self.dcmi_type, self.dcmi_type_valueURI, "  ")}
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
  <identifier type="ark">{escape(self.ark)}</identifier>
  <identifier type="local">{escape(self.local_id)}</identifier>
  <identifier type="avian-id">{escape(self.avian_id)}</identifier>
  <identifier type="uid">{escape(self.uid)}</identifier>
  <identifier type="project-number">{escape(self.project_number)}</identifier>
  <identifier>{escape(self.file_name)}</identifier>
  <identifier type="islandora">{escape(self.pid)}</identifier>
  <note type="hardware/software">{escape(self.hardware_software)}</note>
</mods>
"""

    def dcmi_to_xml(self, types, uris, indent):
        types_xml = []
        for t, u in zip_longest(
            types.strip().split(";"),
            uris.strip().split(";"),
            fillvalue="",
        ):
            types_xml.append(
                f'{indent}<genre authority="dct" valueURI="{escape(u)}">{escape(t)}</genre>'
            )

        return "\n".join(types_xml)

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
                f'{indent}<{term_type} valueURI="{u.strip()}">{escape(t.strip())}</{term_type_end}>'
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
