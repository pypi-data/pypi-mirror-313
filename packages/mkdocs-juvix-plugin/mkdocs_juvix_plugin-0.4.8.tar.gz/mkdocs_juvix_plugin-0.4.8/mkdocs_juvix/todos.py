"""
This plugin is used to find and report TODOs in the documentation.
"""

from os import getenv
from pathlib import Path
from typing import List, Optional

from markdown.extensions import Extension  # type: ignore
from markdown.preprocessors import Preprocessor  # type: ignore
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from mkdocs_juvix.common.models.loc import FileLoc as Todo
from mkdocs_juvix.env import ENV

log = get_plugin_logger("TodosPlugin")


class RTExtension(Extension):
    env: ENV

    def __repr__(self):
        return "RTExtension"

    def __init__(self, mkconfig):
        self.mkconfig = mkconfig
        self.env = ENV(mkconfig)

    def extendMarkdown(self, md):  # noqa: N802
        self.md = md
        md.registerExtension(self)

        self.imgpp = RTPreprocessor(self.mkconfig)
        md.preprocessors.register(self.imgpp, "todo-pp", 90)


class RTPreprocessor(Preprocessor):
    env: ENV

    def __init__(self, mkconfig: MkDocsConfig):
        self.mkconfig = mkconfig
        self.env = ENV(mkconfig)

    def run(self, lines: List[str]) -> List[str]:
        config = self.mkconfig
        current_page_url = None
        preprocess_page = self.env.SHOW_TODOS_IN_MD

        if "current_page" in config and isinstance(config["current_page"], Page):
            url_relative = self.env.DOCS_PATH / Path(
                config["current_page"].url.replace(".html", ".md")
            )
            current_page_url = url_relative.as_posix()
            current_page_abs: Optional[str] = config["current_page"].file.abs_src_path

            if "todos" in config["current_page"].meta:
                preprocess_page = bool(config["current_page"].meta["todos"])

        if not preprocess_page:
            return lines

        without_todos = []

        offset = 1

        if current_page_abs:
            with open(current_page_abs, "r") as f:
                first_line = f.readline()
                if first_line.startswith("---"):
                    while f.readline().strip() != "---":
                        offset += 1
                    offset += 1

        I: int = 0  # noqa: E741
        while I < len(lines):
            line = lines[I]
            if line.strip().startswith("!!! todo"):
                message = ""
                in_message = False
                I += 1  # noqa: E741
                ROW: int = I
                while I < len(lines):
                    s = lines[I]
                    if in_message:
                        if len(s.strip()) > 0:
                            message += s + "\n"
                        else:
                            break
                    elif len(s.strip()) == 0:
                        in_message = True
                    I += 1  # noqa: E741

                if current_page_url:
                    todo = Todo(
                        path=current_page_url,
                        line=ROW + offset + 1,
                        column=0,
                        text=message,
                    )
                    if self.env.REPORT_TODOS:
                        log.warning(todo)
            else:
                without_todos.append(line)
            I += 1  # noqa: E741

        return lines if self.env.SHOW_TODOS_IN_MD else without_todos


class TodosPlugin(BasePlugin):
    ROOT_PATH: Path
    DOCS_DIRNAME: str
    DOCS_PATH: Path

    def on_config(self, config: MkDocsConfig, **kwargs) -> MkDocsConfig:
        rt_extension = RTExtension(config)
        config_file = config.config_file_path
        ROOT_PATH = Path(config_file).parent.absolute()
        DOCS_DIRNAME = getenv("DOCS_DIRNAME", "docs")
        DOCS_PATH = ROOT_PATH / DOCS_DIRNAME
        config["DOCS_PATH"] = DOCS_PATH
        config["SHOW_TODOS_IN_MD"] = bool(getenv("SHOW_TODOS_IN_MD", False))
        config["REPORT_TODOS"] = bool(getenv("REPORT_TODOS", False))
        config.markdown_extensions.append(rt_extension)  # type: ignore
        return config

    def on_page_markdown(
        self, markdown, page: Page, config: MkDocsConfig, files: Files
    ) -> str:
        config["current_page"] = page  # needed for the preprocessor
        return markdown
