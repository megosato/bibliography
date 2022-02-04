# adapted from: https://github.com/slochower/zotero-manubot/blob/master/fetch_papers.py

# pip install pyzotero
from pyzotero import zotero
import subprocess
import argparse
import os

def createMarkdownFileWithHeader(tempfile: str, outfile: str, header: str):
    with open(outfile, 'w') as outf:
        outf.write(f"# {header}\n\n")

        with open(tempfile, 'r') as tempf:
            for line in tempf:
                outf.write(line)


def getManubotCommand(outfile: str):
    command = "manubot cite --format=markdown "

    if outfile:
        command += f"--output={outfile} "

    return command




if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--tag", help="Zotero library tag", required=False)
    ap.add_argument("--lib-id", help="Zotero user ID from https://www.zotero.org/settings/keys", required=True)
    ap.add_argument("--api-key", help="Zotero API key from https://www.zotero.org/settings/keys/new", required=True)
    ap.add_argument("--outfile", help="Filename for Markdown output", required=False)
    ap.add_argument("--outfile-header", help="Header text for Markdown output", required=False)

    args = vars(ap.parse_args())
    
    print("id", args["lib_id"])
    print("key", args["api_key"])
    

    # From https://www.zotero.org/settings/keys
    #library_id = "5818567"
    # From https://www.zotero.org/settings/keys/new
    #api_key = "yArp2NnHeI4BxJdREojr3n7Y"


    library_type = "user"
    zot = zotero.Zotero(args["lib_id"], library_type, args["api_key"])

    if args["tag"]:
        zot.add_parameters(tag=args["tag"], sort="date")
    else:
        raise NotImplementedError


    items = zot.items()


    string_of_identifiers = ""
    for item in items:
        try:
            string_of_identifiers += "doi:"
            string_of_identifiers += item['data']['DOI']
            string_of_identifiers += " "
        except:
            print(f"Missing DOI: {item['data']['title']}")


    ofile = None
    tempfile = "temp.md"
    if args["outfile"] and args["outfile_header"]:
        ofile = tempfile
    if args["outfile"] and not args["outfile_header"]:
        ofile = args["outfile"]

    command = getManubotCommand(ofile) + string_of_identifiers
    print(command)

    subprocess.call(command, shell=True)

    # if a header is specified, create a markdown file with header
    if args["outfile"] and args["outfile_header"]:
        createMarkdownFileWithHeader(ofile, args["outfile"], args["outfile_header"])
        if os.path.isfile(ofile):
            os.remove(ofile)



