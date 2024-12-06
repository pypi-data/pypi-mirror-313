import logging
import os
from dotenv import load_dotenv
from typing import List, Dict

from atlassian import Confluence
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Page

from .create_pages import create_pages
from .update_page import update_page
from .upload_attachments import upload_attachments
from .types import MD_to_Page

class ConfluencePublisherPlugin(BasePlugin):
    config_scheme = (
        ('confluence_prefix', config_options.Type(str, default='')),
        ('space_key', config_options.Type(str, required=True)),
        ('parent_page_id', config_options.Type(int, required=True)),
    )

    def __init__(self):
        load_dotenv()
        self.confluence = None
        self.logger = logging.getLogger('mkdocs.plugins.confluence_publisher')
        self.md_to_page: MD_to_Page = {}
        self.page_attachments: Dict[str, List[str]] = {}

    def on_config(self, config):
        self.logger.debug("Initializing Confluence connection")
        self.confluence = Confluence(
            url=os.environ.get('CONFLUENCE_URL'),
            username=os.environ.get('CONFLUENCE_USERNAME'),
            password=os.environ.get('CONFLUENCE_API_TOKEN')
        )
        self.logger.debug("Confluence connection initialized")
        return config

    def on_nav(self, nav, config, files):
        prefix = self.config['confluence_prefix']
        space_key = self.config['space_key']
        parent_page_id = self.config['parent_page_id']
        self.logger.info(
            f"Ensuring pages exist in Confluence with prefix '{prefix}' under parent {parent_page_id} in space: '{space_key}'")
        self.md_to_page = create_pages(self.confluence, nav.items, prefix, space_key, parent_page_id,
                                          self.md_to_page)
        self.logger.debug(f"URL to Page ID mapping: {self.md_to_page}")

    def on_page_markdown(self, markdown, page: Page, config, files):
        self.logger.debug(f"Processing markdown for page: {page.file.src_path}")
        attachments = update_page(markdown, page, self.confluence, self.md_to_page)
        self.page_attachments[page.file.src_path] = attachments
        self.logger.debug(f"Stored page in Confluence. Attachments: {attachments}")
        return markdown

    def on_post_page(self, output, page, config):
        page_id = self.md_to_page.get(page.file.src_path).id
        attachments = self.page_attachments.get(page.file.src_path, [])
        self.logger.debug(f"Uploading attachments {attachments} for page: {page.file.src_path}, Page ID: {page_id}")
        upload_attachments(page_id, attachments, self.confluence, self.config['space_key'])
        self.logger.debug(f"Uploaded {len(attachments)} attachments for page: {page.file.src_path}")
        return output

    def on_post_build(self, config):
        self.logger.info("Publish to confluence complete")
