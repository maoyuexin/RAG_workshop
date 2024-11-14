from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os
import html
 
 

import html
def table_to_html(table):
    table_html = "<table>"
    rows = [sorted([cell for cell in table['cells'] if cell['rowIndex'] == i], key=lambda cell: cell['columnIndex']) for i in range(table['rowCount'])]
    for row_cells in rows:
        table_html += "<tr>"
        for cell in row_cells:
            try:
                if (cell['kind'] == "columnHeader" or cell['kind'] == "rowHeader"):
                    tag = "th"
                else:
                    tag = "td"
            except:
                tag = "td"

           # tag = "th" if (cell['kind'] == "columnHeader" or cell['kind'] == "rowHeader") else "td"
            cell_spans = ""
            try:
                if cell['columnSpan'] > 1: cell_spans += f" colSpan={cell['columnSpan']}"
            except:
                cell_spans = cell_spans
            try:
                if cell['rowSpan'] > 1: cell_spans += f" rowSpan={cell['rowSpan']}"
            except:
                cell_spans = cell_spans
            table_html += f"<{tag}{cell_spans}>{html.escape(cell['content'])}</{tag}>"
        table_html +="</tr>"
    table_html += "</table>"
    return table_html

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
 
def pdf_parsing_Doc_intelligence(form_recognizer_results):
      
    for page_num, page in enumerate(form_recognizer_results['pages']):
        tables_on_page = [table for table in form_recognizer_results['tables'] if table['tables']['bounding_regions'][0]["page_number"] == page_num + 1]

        # mark all positions of the table spans in the page
        page_offset = page['spans'][0]["offset"]
        page_length = page['spans'][0]["length"]
        table_chars = [-1]*page_length
        for table_id, table in enumerate(tables_on_page):
            for span in table["spans"]:
                # replace all table spans with "table_id" in table_chars array
                for i in range(span["length"]):
                    idx = span["offset"] - page_offset + i
                    if idx >=0 and idx < page_length:
                        table_chars[idx] = table_id

        # build page text by replacing charcters in table spans with table html
        page_text = ""
        added_tables = set()
        for idx, table_id in enumerate(table_chars):
            if table_id == -1:
                page_text += form_recognizer_results["content"][page_offset + idx]
            elif not table_id in added_tables:
                page_text += table_to_html(tables_on_page[table_id])
                added_tables.add(table_id)

        page_text += " "
        page_map.append((page_num, offset, page_text))
        offset += len(page_text)
 
    return page_map
