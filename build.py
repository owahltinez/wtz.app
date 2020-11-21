#!/bin/env python
import json
import shutil
from pathlib import Path
from string import Template

def render(tpl_path: Path, **config) -> str:
    with open(tpl_path, 'r') as fd:
        tpl = Template(fd.read())
        return tpl.substitute(**config)

if __name__ == "__main__":

    # Process the arguments from the config.json file
    with open("config.json", "r") as fd:
        config = json.load(fd)

    # Create a /public folder and ensure it's empty
    public = Path(__file__).parent / "public"
    if public.exists():
        shutil.rmtree(public)
    public.mkdir()

    # Publish the output under the /public folder
    with open(public / "index.html", "w") as fd:
        fd.write(render('index.tpl.html', **config))

    # Publish our custom 404 page undet the /public folder
    with open(public / "404.html", "w") as fd:
        fd.write(render('404.tpl.html', **config))

