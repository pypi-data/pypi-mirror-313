import logging
from mkdocs.structure.nav import Section, Page
from .types import MD_to_Page, ConfluencePage

logger = logging.getLogger('mkdocs.plugins.confluence_publisher.create_pages')

def create_pages(confluence, items, prefix, space_key, parent_id, md_to_page: MD_to_Page):
    for item in items:
        page_title = f"{prefix}{item.title}"
        logger.debug(f"Processing item: {page_title}")

        # Check if the page already exists
        existing_page = confluence.get_page_by_title(space_key, page_title)

        if existing_page:
            logger.debug(f"Page already exists: {page_title}")
            page_id = existing_page['id']
        else:
            if isinstance(item, Section):
                body = '<ac:structured-macro ac:name="children" />'
                logger.info(f"Creating section page: {page_title}")
            else:
                # It's a "Page"
                body = ""
                logger.info(f"Creating empty page: {page_title}")

            try:
                new_page = confluence.create_page(
                    space=space_key,
                    title=page_title,
                    body=body,
                    parent_id=parent_id
                )
                page_id = new_page['id']
            except Exception as e:
                logger.error(f"Error creating page {page_title}: {str(e)}")
                continue

        # Store the mapping of URL to page ID
        if  isinstance(item, Page):
            md_to_page[item.file.src_path] = ConfluencePage(id=page_id, title=page_title)
            logger.debug(f"Mapped URL {item.url} to page ID {page_id}")

        # If it's a "Section", recursively create child pages
        if isinstance(item, Section) and item.children:
            logger.debug(f"Processing children of {page_title}")
            create_pages(confluence, item.children, prefix, space_key, page_id, md_to_page)

    return md_to_page
