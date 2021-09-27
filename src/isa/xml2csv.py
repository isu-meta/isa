import csv
from pathlib import Path

from lxml.etree import parse


def load_xml(xml_dir):
    xmls = []
    for x in Path(xml_dir).glob("*.xml"):
        xmls.append(parse(str(x)))

    return xmls


def xml_to_csv(mds):
    return [XmlMD(md) for md in mds]


def save_csv(mds, output_path, delimiter=",", newline="\n"):
    headers = [
        "pid",
        "title",
        "archival_call_number",
        "archival_collection",
        "finding_aid_ark",
        "physical_location",
        "archival_series_title",
        "folder_title",
        "box",
        "folder",
        "contributing_institution",
        "personal_creator",
        "personal_creator_valueURI",
        "corporate_creator",
        "corporate_creator_valueURI",
        "interviewee",
        "interviewee_valueURI",
        "interviewer",
        "interviewer_valueURI",
        "personal_contributor",
        "personal_contributor_valueURI",
        "corporate_contributor",
        "corporate_contributor_valueURI",
        "description",
        "table_of_contents",
        "annotation",
        "url",
        "language",
        "topical_subject_fast",
        "topical_subject_fast_valueURI",
        "geographic_subject_fast",
        "geographic_subject_fast_valueURI",
        "topical_subject_lcsh",
        "topical_subject_lcsh_valueURI",
        "topical_subject_local",
        "topical_subject_local_valueURI",
        "geographic_subject_lcsh",
        "geographic_subject_lcsh_valueURI",
        "geographic_subject_local",
        "geographic_subject_local_valueURI",
        "geographic_subject_geonames",
        "geographic_subject_geonames_valueURI",
        "personal_name_subject",
        "personal_name_subject_valueURI",
        "corporate_name_subject",
        "corporate_name_subject_valueURI",
        "birds_subject",
        "birds_subject_valueURI",
        "chronological_subject",
        "event_subject",
        "event_subject_valueURI",
        "extent",
        "aat_type",
        "aat_type_valueURI",
        "dcmi_type",
        "dcmi_type_valueURI",
        "type_of_resource",
        "imt_type",
        "cco_description",
        "rights_management",
        "date_original",
        "date_digital",
        "location_interview",
        "publisher",
        "ark",
        "local_id",
        "file_name",
        "uid",
        "avian_id",
        "project_number",
        "date_created",
        "date_modified",
        "issuance",
        "issuance_start",
        "issuance_end",
        "frequency",
        "digital_collection",
        "digital_collection_ark",
        "hardware_software",
        "image_manipulation",
        "file_size",
        "resolution",
        "colorspace",
        "bits_per_sample",
        "samples_per_pixel",
        "height",
        "width",
        "digital_origin",
    ]
    
    csv_md = [headers] + [md.to_row() for md in mds]
    #csv_text = newline.join([delimiter.join(row) for row in csv_md])

    with open(output_path, "w", encoding="utf8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerows(csv_md)


class XmlMD:
    def __init__(self, md):
        ns = {"mods": "http://www.loc.gov/mods/v3"}

        self.pid = md.xpath("string(/mods:mods/mods:identifier[@type='islandora'])", namespaces=ns)
        self.title = md.xpath("string(/mods:mods/mods:titleInfo/mods:title)", namespaces=ns)
        self.archival_call_number = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:identifier[@displayLabel='Call Number'])",
            namespaces=ns,
        )
        self.archival_collection = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.finding_aid_ark = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:identifier[@type='ark'])",
            namespaces=ns,
        )
        self.physical_location = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:location/mods:physicalLocation)",
            namespaces=ns,
        )
        self.archival_series_title = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:relatedItem[@type='series']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.folder_title = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:relatedItem[@type='series']/mods:relatedItem[@type='constituent']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.box = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:relatedItem[@type='constituent']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.folder = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='original']/mods:relatedItem[@type='constituent']/mods:relatedItem[@type='constituent']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.contributing_institution = md.xpath(
            "string(/mods:mods/mods:name/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='curator'])",
            namespaces=ns,
        )
        self.personal_creator = "; ".join(
            md.xpath( 
                "/mods:mods/mods:name[@type='personal']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='creator']/text()",
                namespaces=ns,
            )
        )
        self.personal_creator_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='personal' and ./mods:role/mods:roleTerm/text()='creator']/@valueURI",
                namespaces=ns,
            )
        )
        self.corporate_creator = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='corporate']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='creator']/text()",
                namespaces=ns,
            )
        )
        self.corporate_creator_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='corporate' and ./mods:role/mods:roleTerm/text()='creator']/@valueURI",
                namespaces=ns,
            )
        )
        self.interviewee = md.xpath(
            "string(/mods:mods/mods:name[@type='personal']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='interviewee']/text())",
            namespaces=ns,
        )
        self.interviewee_valueURI = md.xpath(
            "string(/mods:mods/mods:name[@type='personal' and ./mods:role/mods:roleTerm/text()='interviewee']/@valueURI)",
            namespaces=ns,
        )
        self.interviewer = md.xpath(
            "string(/mods:mods/mods:name[@type='personal']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='interviewer']/text())",
            namespaces=ns,
        )
        self.interviewer_valueURI = md.xpath(
            "string(/mods:mods/mods:name[@type='personal' and ./mods:role/mods:roleTerm/text()='interviewer']/@valueURI)",
            namespaces=ns,
        )
        self.personal_contributor = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='personal']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='contributor']/text()",
                namespaces=ns,
            )
        )
        self.personal_contributor_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='personal' and ./mods:role/mods:roleTerm/text()='contributor']/@valueURI",
                namespaces=ns,
            )
        )
        self.corporate_contributor = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='corporate']/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='contributor']/text()",
                namespaces=ns,
            )
        )
        self.corporate_contributor_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:name[@type='corporate' and ./mods:role/mods:roleTerm/text()='contributor']/@valueURI",
                namespaces=ns,
            )
        )
        self.description = md.xpath("string(/mods:mods/mods:abstract)", namespaces=ns)
        self.table_of_contents = md.xpath("string(/mods:mods/mods:tableOfContents)", namespaces=ns)
        self.annotation = md.xpath(
            "string(/mods:mods/mods:note[@type='annotation'])", namespaces=ns
        )
        self.url = md.xpath("string(/mods:mods/mods:location/mods:url)", namespaces=ns)
        self.language = "; ".join(
            md.xpath("mods:language/mods:languageTerm/text()", namespaces=ns)
        )
        self.topical_subject_fast = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='fast']/mods:topic/text()", namespaces=ns)
        )
        self.topical_subject_fast_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='fast']/mods:topic/@valueURI", namespaces=ns
            )
        )
        self.geographic_subject_fast = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='fast']/mods:geographic/text()", namespaces=ns)
        )
        self.geographic_subject_fast_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='fast']/mods:geographic/@valueURI",
                namespaces=ns,
            )
        )
        self.topical_subject_lcsh = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='lcsh']/mods:topic/text()", namespaces=ns)
        )
        self.topical_subject_lcsh_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='lcsh']/mods:topic/@valueURI", namespaces=ns
            )
        )
        self.topical_subject_local = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='local']/mods:topic/text()", namespaces=ns)
        )
        self.topical_subject_local_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='local']/mods:topic/@valueURI", namespaces=ns
            )
        )
        self.geographic_subject_lcsh = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='lcsh']/mods:geographic/text()", namespaces=ns)
        )
        self.geographic_subject_lcsh_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='lcsh']/mods:geographic/@valueURI",
                namespaces=ns,
            )
        )
        self.geographic_subject_local = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='local']/mods:geographic/text()", namespaces=ns)
        )
        self.geographic_subject_local_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='local']/mods:geographic/@valueURI",
                namespaces=ns,
            )
        )
        self.geographic_subject_geonames = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='geonames']/mods:geographic/text()", namespaces=ns
            )
        )
        self.geographic_subject_geonames_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='geonames']/mods:geographic/@valueURI",
                namespaces=ns,
            )
        )
        self.personal_name_subject = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='naf']/mods:name[@type='personal']/mods:namePart/text()",
                namespaces=ns,
            )
        )
        self.personal_name_subject_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='naf']/mods:name[@type='personal']/@valueURI",
                namespaces=ns,
            )
        )
        self.corporate_name_subject = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='naf']/mods:name[@type='corporate']/mods:namePart/text()",
                namespaces=ns,
            )
        )
        self.corporate_name_subject_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='naf']/mods:name[@type='corporate']/@valueURI",
                namespaces=ns,
            )
        )
        self.birds_subject = "; ".join(
            md.xpath("/mods:mods/mods:subject[@authority='gbif']/mods:topic/text()", namespaces=ns)
        )
        self.birds_subject_valueURI = "; ".join(
            md.xpath(
                "/mods:mods/mods:subject[@authority='gbif']/mods:topic/@valueURI", namespaces=ns
            )
        )
        self.chronological_subject = "; ".join(
            md.xpath("/mods:mods/mods:subject[not(@authority)]/mods:temporal/text()", namespaces=ns)
        )
        self.event_subject = "; ".join(
            md.xpath("/mods:mods/mods:subject[not(@authority)]/mods:topic/text()", namespaces=ns)
        )
        self.event_subject_valueURI = "; ".join(
            md.xpath("/mods:mods/mods:subject[not(@authority)]/mods:topic/@valueURI", namespaces=ns)
        )
        self.extent = "; ".join(
            md.xpath("/mods:mods/mods:physicalDescription/mods:extent/text()", namespaces=ns)
        )
        self.aat_type = "; ".join(
            md.xpath("/mods:mods/mods:genre[@authority='aat']/text()", namespaces=ns)
        )
        self.aat_type_valueURI = "; ".join(
            md.xpath("/mods:mods/mods:genre[@authority='aat']/@valueURI", namespaces=ns)
        )
        self.dcmi_type = md.xpath("string(/mods:mods/mods:genre[@authority='dct'])", namespaces=ns)
        self.dcmi_type_valueURI = md.xpath(
            "string(/mods:mods/mods:genre[@authority='dct']/@valueURI)", namespaces=ns
        )
        self.type_of_resource = md.xpath("string(/mods:mods/mods:typeOfResource)", namespaces=ns)
        self.imt_type = md.xpath("string(/mods:mods/mods:genre[@authority='imt'])", namespaces=ns)
        self.cco_description = md.xpath(
            "string(/mods:mods/mods:genre[@authority='cco'])", namespaces=ns
        )
        self.rights_management = md.xpath(
            "string(/mods:mods/mods:accessCondition)", namespaces=ns
        )
        self.date_original = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:dateCreated)", namespaces=ns
        )
        self.date_digital = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:dateCaptured)", namespaces=ns
        )
        self.location_interview = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:place/mods:placeTerm)", namespaces=ns
        )
        self.publisher = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:publisher)", namespaces=ns
        )
        self.ark = md.xpath("string(/mods:mods/mods:identifier[@type='ark'])", namespaces=ns)
        self.local_id = md.xpath(
            "string(/mods:mods/mods:identifier[@type='local'])", namespaces=ns
        )
        self.file_name = md.xpath("string(/mods:mods/mods:identifier[not(@*)])", namespaces=ns)
        self.uid = md.xpath("string(/mods:mods/mods:identifier[@type='uid'])", namespaces=ns)
        self.avian_id = md.xpath(
            "string(/mods:mods/mods:identifier[@type='avian-id'])", namespaces=ns
        )
        self.project_number = md.xpath(
            "string(/mods:mods/mods:identifier[@type='project-number'])", namespaces=ns
        )
        self.date_created = md.xpath(
            "string(/mods:mods/mods:recordInfo/mods:recordCreationDate)", namespaces=ns
        )
        self.date_modified = md.xpath(
            "string(/mods:mods/mods:recordInfo/mods:recordChangeDate)", namespaces=ns
        )
        self.issuance = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:issuance)", namespaces=ns
        )
        self.issuance_start = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:dateIssued[@point='start'])", namespaces=ns
        )
        self.issuance_end = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:dateIssued[@point='end'])", namespaces=ns
        )
        self.frequency = md.xpath(
            "string(/mods:mods/mods:originInfo/mods:frequency)", namespaces=ns
        )
        self.digital_collection = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='host']/mods:titleInfo/mods:title)",
            namespaces=ns,
        )
        self.digital_collection_ark = md.xpath(
            "string(/mods:mods/mods:relatedItem[@type='host']/mods:identifier[@type='ark'])", 
            namespaces=ns,
        )
        self.hardware_software = md.xpath(
            "string(/mods:mods/mods:note[@type='hardware/software'])", namespaces=ns
        )
        self.image_manipulation = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='image-manipulation'])",
            namespaces=ns,
        )
        self.file_size = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='file-size'])",
            namespaces=ns,
        )
        self.resolution = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='resolution'])",
            namespaces=ns,
        )
        self.colorspace = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='colorspace'])",
            namespaces=ns,
        )
        self.bits_per_sample = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='bits-per-sample'])",
            namespaces=ns,
        )
        self.samples_per_pixel = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='samples-per-pixel'])",
            namespaces=ns,
        )
        self.height = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='height'])", namespaces=ns
        )
        self.width = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:note[@type='width'])", namespaces=ns
        )
        self.digital_origin = md.xpath(
            "string(/mods:mods/mods:physicalDescription/mods:digitalOrigin)", namespaces=ns
        )

    def to_row(self):
        return [
                self.pid,
                self.title,
                self.archival_call_number,
                self.archival_collection,
                self.finding_aid_ark,
                self.physical_location,
                self.archival_series_title,
                self.folder_title,
                self.box,
                self.folder,
                self.contributing_institution,
                self.personal_creator,
                self.personal_creator_valueURI,
                self.corporate_creator,
                self.corporate_creator_valueURI,
                self.interviewee,
                self.interviewee_valueURI,
                self.interviewer,
                self.interviewer_valueURI,
                self.personal_contributor,
                self.personal_contributor_valueURI,
                self.corporate_contributor,
                self.corporate_contributor_valueURI,
                self.description,
                self.table_of_contents,
                self.annotation,
                self.url,
                self.language,
                self.topical_subject_fast,
                self.topical_subject_fast_valueURI,
                self.geographic_subject_fast,
                self.geographic_subject_fast_valueURI,
                self.topical_subject_lcsh,
                self.topical_subject_lcsh_valueURI,
                self.topical_subject_local,
                self.topical_subject_local_valueURI,
                self.geographic_subject_lcsh,
                self.geographic_subject_lcsh_valueURI,
                self.geographic_subject_local,
                self.geographic_subject_local_valueURI,
                self.geographic_subject_geonames,
                self.geographic_subject_geonames_valueURI,
                self.personal_name_subject,
                self.personal_name_subject_valueURI,
                self.corporate_name_subject,
                self.corporate_name_subject_valueURI,
                self.birds_subject,
                self.birds_subject_valueURI,
                self.chronological_subject,
                self.event_subject,
                self.event_subject_valueURI,
                self.extent,
                self.aat_type,
                self.aat_type_valueURI,
                self.dcmi_type,
                self.dcmi_type_valueURI,
                self.type_of_resource,
                self.imt_type,
                self.cco_description,
                self.rights_management,
                self.date_original,
                self.date_digital,
                self.location_interview,
                self.publisher,
                self.ark,
                self.local_id,
                self.file_name,
                self.uid,
                self.avian_id,
                self.project_number,
                self.date_created,
                self.date_modified,
                self.issuance,
                self.issuance_start,
                self.issuance_end,
                self.frequency,
                self.digital_collection,
                self.digital_collection_ark,
                self.hardware_software,
                self.image_manipulation,
                self.file_size,
                self.resolution,
                self.colorspace,
                self.bits_per_sample,
                self.samples_per_pixel,
                self.height,
                self.width,
                self.digital_origin,
            ]
