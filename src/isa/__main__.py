import argparse
from pathlib import Path

from isa import csv2xml as c2x
from isa import xml2csv as x2c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    input_ = Path(args.input)
    output = Path(args.output)

    if input_.is_dir():
        xmls = x2c.load_xml(input_)
        csv = x2c.xml_to_csv(xmls)
        x2c.save_csv(csv, output)
    else:
        csv = c2x.load_csv(input_)
        xmls = c2x.csv_to_xml(csv)
        c2x.save_multiple_xml(xmls, output)


if __name__ == "__main__":
    main()