# pip install pyzotero
from pyzotero import zotero
import subprocess
# From https://www.zotero.org/settings/keys
library_id = "5818567"
# From https://www.zotero.org/settings/keys/new
api_key = "yArp2NnHeI4BxJdREojr3n7Y"
library_type = "user"
zot = zotero.Zotero(library_id, library_type, api_key)
#zot.add_parameters(q="testlib")
zot.add_parameters(tag="test")
items = zot.items()
string_of_dois = ""
for item in items:
    try:
        string_of_dois += "doi:"
        string_of_dois += item['data']['DOI']
        string_of_dois += " "
    except:
        print(f"Missing DOI: {item['data']['title']}")
command = f"""
manubot \
cite \
--format=markdown \
--output=test.md \
{string_of_dois} \
"""
subprocess.call(command, shell=True)
