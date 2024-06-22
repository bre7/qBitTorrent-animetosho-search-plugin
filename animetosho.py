# VERSION: 1.00
# AUTHORS: ALAA_BRAHIM
# LICENSING INFORMATION

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from xml.dom.minidom import parseString
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
import traceback
import sys

class animetosho(object):
    url = "https://animetosho.org"
    name = "Anime Tosho"
    supported_categories = {
        "anime": [""],
    }

    def __init__(self):
        pass

    def download_torrent(self, info):
        print(download_file(info))

    def search(self, what, cat='anime'):
        url = f"https://feed.animetosho.org/api?q={what}"
        data = retrieve_url(url)
        parser = self.DataExtractor()
        parser.feed(data)
        results = parser.get_results()
        for result in results:
            prettyPrinter(result)

    class DataExtractor():
        def __init__(self):
            super().__init__()
            self.results = []
            self.current_result = {"engine_url": "https://animetosho.org/"}

        def feed(self, data):
            try:
                document = parseString(data)
                # print("results: ", len(document.getElementsByTagName("item")))

                for item in document.getElementsByTagName("item"):
                    self.current_result["name"] = item.getElementsByTagName("title")[0].firstChild.nodeValue
                    self.current_result["desc_link"] = item.getElementsByTagName("link")[0].firstChild.nodeValue
                    self.current_result["seeds"] = "0"
                    self.current_result["leech"] = "0"

                    for child in item.childNodes:
                        if child.nodeName == "newznab:attr":
                            if child.getAttribute("name") == "size":
                                self.current_result["size"] = child.getAttribute("value")
                        if child.nodeName == "torznab:attr":
                            if child.getAttribute("name") == "magneturl":
                                self.current_result["link"] = child.getAttribute("value")
                            if child.getAttribute("name") == "seeders":
                                self.current_result["seeds"] = child.getAttribute("value")
                            if child.getAttribute("name") == "leechers":
                                self.current_result["leech"] = child.getAttribute("value")
                    self.check_current_result_completed()
            except Exception as e:
                print(e, traceback.format_exc(), file=sys.stderr)

        def check_current_result_completed(self):
            if len(self.current_result) == 7:
                self.results.append(self.current_result)
                self.current_result = {"engine_url": "https://animetosho.org/"}

        def get_results(self):
            return self.results


if __name__ == "__main__":
    a = animetosho()
    a.search("zom+judas")
