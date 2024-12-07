from mkdocs.plugins import BasePlugin
import re
import xml.etree.ElementTree as ET
import os


def parse_xml_bom(bom_path):
    print("Parsing BOM : " + bom_path)
    tree = ET.parse(bom_path)
    root = tree.getroot()
    bom_attributes = root.attrib
    components = []
    for group in root.findall("group"):
        component = {
            "Row": group.get("Row"),
            "Description": group.get("Description"),
            "Part": group.get("Part"),
            "References": group.get("References"),
            "Value": group.get("Value"),
            "Footprint": group.get("Footprint"),
            "Quantity_Per_PCB": group.get("Quantity_Per_PCB"),
            "Datasheet": group.get("Datasheet"),
        }
        components.append(component)
    return components


class AkizukiDenshiOrderButtonPlugin(BasePlugin):
    components = []

    def on_page_markdown(self, markdown, page, config, files):
        for button in re.finditer(
            r"@akizuki_denshi_order_button\(.+?\)", markdown, re.MULTILINE
        ):
            for content in re.finditer(
                r"(?<=@akizuki_denshi_order_button\().*?(?=\))",
                button.group(),
                re.MULTILINE,
            ):
                bom_path = os.path.join(
                    os.path.dirname(page.file.abs_src_path), content.group()
                )
                self.components = parse_xml_bom(bom_path)
                print(self.components)
            markdown = markdown.replace(
                button.group(),
                "[Order parts on AkizukiDenshi]("
                + self.get_url_from_parts_ids(self.get_parts_info())
                + "){ .md-button .md-button--primary }",
            )
        return markdown

    def get_parts_info(self):
        parts_info = []
        for component in self.components:
            if self.extract_item_number(component["Datasheet"]) is not None:
                parts_info.append(
                    {
                        "id": self.extract_item_number(component["Datasheet"]),
                        "quantity": component["Quantity_Per_PCB"],
                    }
                )
        return parts_info

    def extract_item_number(self, url):
        pattern = r"https://akizukidenshi\.com/catalog/g/g(\d+)/?"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        elif self.is_target_url(url):
            raise Exception(
                "URL "
                + url
                + " was guessed as akizuki denshi URL, but I could not get parts ID."
            )
        return None

    def is_target_url(self, url):
        pattern = r"^https://akizukidenshi\.com"
        return re.match(pattern, url) is not None

    def get_url_from_parts_ids(self, parts_info):
        url = "https://akizukidenshi.com/catalog/quickorder/blanketorder.aspx?regist_goods="
        for i, parts in enumerate(parts_info):
            url = url + parts["id"] + "+" + parts["quantity"]
            if i != (len(parts_info) - 1):
                url = url + "%0D"
        #     # url = url +
        print(url)
        return url


def main():
    pass


if __name__ == "__main__":
    pass
