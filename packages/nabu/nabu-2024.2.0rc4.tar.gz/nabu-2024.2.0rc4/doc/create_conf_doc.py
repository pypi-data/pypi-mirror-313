#!/usr/bin/env python
import os
from nabu.pipeline.fullfield.nabu_config import nabu_config


def header(file_):
    content = "# Nabu configuration parameters\nThis file lists all the current configuration parameters available in the [configuration file](nabu_config_file.md)."
    print(content, file=file_)

def generate(file_):
    def write(content):
        print(content, file=file_)
    header(file_)
    for section, values in nabu_config.items():
        if section == "about":
            continue
        write("### %s\n" % section)
        for key, val in values.items():
            if val["type"] == "unsupported":
                continue
            help_content = val["help"]
            if "---" in help_content:
                help_content = help_content.replace("--", "")
            write(help_content + "\n")
            write(
                "```ini\n%s = %s\n```"
                % (key, val["default"])
            )



if __name__ == "__main__":
    fname = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "nabu_config_items.md"
    )
    with open(fname, "w") as f:
        generate(f)
