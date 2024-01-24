import argparse
from pathlib import Path

from isa import csv2xml as c2x
from isa import xml2csv as x2c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--alpha-sort", action="store_true")
    parser.add_argument("--skip-compound-reorder", action="store_true")
    parser.add_argument("--new-compound-reorder", action="store_true")
    parser.add_argument("--generate-dc", action="store_true")
    args = parser.parse_args()

    input_ = Path(args.input)
    output = Path(args.output)

    if input_.is_dir():
        if args.alpha_sort:
            xmls = x2c.load_xml(input_, True)
        else:
            xmls = x2c.load_xml(input_)
        csv = x2c.xml_to_csv(xmls)
        if args.skip_compound_reorder:
            print("Skipping compound reorder")
            x2c.save_csv(csv, output, False)
        else:
            if args.new_compound_reorder:
                x2c.save_csv(csv, output, new=True)
            else:
                x2c.save_csv(csv, output)
    else:
        csv = c2x.load_csv(input_)
        output.mkdir(exist_ok=True)

        xmls = c2x.csv_to_xml(csv)
        for x in xmls:
            c2x.save_xml(x, "mods", output)

        if args.generate_dc:
            for x in xmls:
                c2x.save_xml(x, "dc", output)


if __name__ == "__main__":
    main()
