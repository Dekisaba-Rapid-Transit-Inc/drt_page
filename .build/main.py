import jinja2
import markdown
import glob
import os
import pathlib
import shutil
import yaml
from collections import ChainMap

temple=jinja2.Environment(loader=jinja2.FileSystemLoader("./.build/tmpl", encoding="utf-8"))

def conv(path):
    if path.suffix==".md":
        with open(path,"r",encoding="utf-8")as f:
            md=markdown.Markdown(extensions = ['meta'])
            doc=f.read()
            meta={}
            if doc.startswith("---"):
                doc=doc.lstrip("---").split("---")
                meta=yaml.safe_load(doc.pop(0))
                doc="---".join(doc)
            doc=md.convert(doc)
            if meta.get("tmpl") is None:
                return doc.encode("utf-8")
            else:
                return temple.get_template(meta["tmpl"]).render(**ChainMap(meta,{"ogp_pagetype":"article","doc":doc,"desctiption":"でき鯖高速鉄道グループは、できたてサーバー(猫)にて活動している鉄道運営企業です。"})).encode("utf-8")
    else:
        with open(path,"br")as f:return f.read()

def relative_loader(path:pathlib.Path,generated_dir=pathlib.Path("./docs/")):
    generated_dir.mkdir()
    for file_or_dir in path.iterdir():
        if file_or_dir.is_dir():
            relative_loader(file_or_dir,(generated_dir/(file_or_dir.name)))
            continue
        doc=conv(file_or_dir)
        with open((generated_dir/(file_or_dir.name.rstrip(".md")+".html")) if file_or_dir.suffix==".md" else (generated_dir/(file_or_dir.name)) ,"bw")as f:
            f.write(doc)

if __name__=="__main__":
    try:shutil.rmtree("./docs/")
    except FileNotFoundError:pass
    relative_loader(pathlib.Path("./source/"),pathlib.Path("./docs"))