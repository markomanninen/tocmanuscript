#!pip install notion-client mistune html2text

import os, re, glob, base64, json
import mistune, html2text
from notion_client import Client
from os import environ

# Initialize the Notion client
notion = Client(auth=environ.get("NOTION_SECRET"))

def process_inline_formatting(text):
    # Regular expressions for bold and italic markdown
    bold_pattern = r'\*\*(.+?)\*\*'
    italic_pattern = r'\*(.+?)\*'

    # Replace markdown with Notion rich text formatting
    def replace_bold(match):
        return {
            "type": "text",
            "text": {
                "content": match.group(1),
                "link": None
            },
            "annotations": {
                "bold": True,
                "italic": False,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
            },
            "plain_text": match.group(1),
            "href": None
        }

    def replace_italic(match):
        return {
            "type": "text",
            "text": {
                "content": match.group(1),
                "link": None
            },
            "annotations": {
                "bold": False,
                "italic": True,
                "strikethrough": False,
                "underline": False,
                "code": False,
                "color": "default"
            },
            "plain_text": match.group(1),
            "href": None
        }

    # Apply the replacements
    text_parts = []

    # Process bold matches
    bold_matches = list(re.finditer(bold_pattern, text))
    prev_end = 0
    for match in bold_matches:
        if prev_end != match.start():
            text_parts.append(text[prev_end:match.start()])
        text_parts.append(replace_bold(match))
        prev_end = match.end()
    text_parts.append(text[prev_end:])

    # Process italic matches
    new_text_parts = []
    for part in text_parts:
        if isinstance(part, str):
            italic_matches = list(re.finditer(italic_pattern, part))
            prev_end = 0
            for match in italic_matches:
                if prev_end != match.start():
                    new_text_parts.append(part[prev_end:match.start()])
                new_text_parts.append(replace_italic(match))
                prev_end = match.end()
            new_text_parts.append(part[prev_end:])
        else:
            new_text_parts.append(part)

    # Remove empty strings from the list
    return [({"type": "text", "text": {"content": part}} if type(part) == str else part) for part in new_text_parts if part != '']

def parse_markdown_to_notion_blocks(markdown):

    # Detect code blocks enclosed within triple backticks
    code_block_pattern = re.compile(r'```(.+?)```', re.DOTALL)
    numbered_list_pattern = r'^(\d+)\. '
    heading_pattern = r'^(#+) '

    code_blocks = {}
    def replace_code_blocks(match):
        index = len(code_blocks)
        code_blocks[index] = match.group(1)
        return f'CODE_BLOCK_{index}'

    markdown = code_block_pattern.sub(replace_code_blocks, markdown)

    lines = markdown.split("\n")
    blocks = []
    for line in lines:

        heading_match = re.match(heading_pattern, line)
        if heading_match:
            heading_level = len(heading_match.group(1))
            content = re.sub(heading_pattern, '', line)

            # Check the heading level and create the appropriate block
            if 1 <= heading_level <= 3:
                block_type = f"heading_{heading_level}"
                blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": process_inline_formatting(content)
                    }
                })
        elif line.startswith("CODE_BLOCK_"):
            code_block_index = int(line[len("CODE_BLOCK_"):])
            code_content = code_blocks[code_block_index].strip()
            #code_content = json.dumps(code_content)
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "language": "plain text",
                    #"rich_text": json.loads('[{"type": "text", "text": {"content": %s}}]' % code_content)
                    "rich_text": process_inline_formatting(code_content)
                }
            })
        elif line.startswith("* ") or line.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": process_inline_formatting(line[2:])
                }
            })
        elif re.match(numbered_list_pattern, line):
            line = re.sub(numbered_list_pattern, '', line)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": process_inline_formatting(line)
                }
            })
        elif line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": process_inline_formatting(line)
                }
            })
    return blocks

def parse_md(markdown_text):
    # Remove the first two lines.
    markdown_text = '\n'.join(markdown_text.splitlines()[2:]).strip()

    # Convert the Markdown text to HTML
    html_text = mistune.markdown(markdown_text)

    # Convert the HTML back to Markdown using html2text
    markdown_to_notion = html2text.html2text(html_text)

    # Parse the Markdown to create Notion blocks
    return parse_markdown_to_notion_blocks(markdown_text)

def create_notion_page_from_md(markdown_text, title, parent_page_id, cover_url = ''):
    # Create a new child page under the parent page with the given title
    created_page = notion.pages.create(parent={
        "type": "page_id",
        "page_id": parent_page_id
    }, properties={}, children=[])

    cover = {}
    if cover_url != "":
		cover = {
	        "external": {
				# https://images.unsplash.com/photo-1507838153414-b4b713384a76?ixlib=rb-4.0.3&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=3600
	            "url": cover_url
	        }
		}
    # Update the page with the title
    notion.pages.update(created_page["id"], properties=
		{
	        "title": {
	            "title": [{"type": "text", "text": {"content": title}}]
	        }
	    }, cover = cover
	)

    for block in parse_md(markdown_text):
        notion.blocks.children.append(
            created_page["id"],
            children=[block]
        )

    return created_page["url"]
