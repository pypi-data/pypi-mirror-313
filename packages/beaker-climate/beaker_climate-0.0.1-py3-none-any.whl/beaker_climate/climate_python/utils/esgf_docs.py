import requests
import os
from pathlib import Path
import nbformat
from bs4 import BeautifulSoup
import pypandoc

def fetch_github_content(url, raw_base="https://raw.githubusercontent.com"):
    """Fetch content from GitHub, converting the regular GitHub URL to raw content URL."""
    if "github.com" in url:
        parts = url.split("github.com/")[1].split("/blob/" if "/blob/" in url else "/tree/")
        raw_url = f"{raw_base}/{parts[0]}/{parts[1]}"
    else:
        raw_url = url
    
    response = requests.get(raw_url)
    response.raise_for_status()
    return response.text

def process_rst_to_md(rst_content):
    """Convert RST content to Markdown using pypandoc with extra options."""
    try:
        extra_args = [
            '--wrap=none',
            '--columns=1000',
            '--markdown-headings=atx',
            '--tab-stop=2',
            '--standalone'
        ]
        
        md_content = pypandoc.convert_text(
            rst_content,
            'gfm',
            format='rst',
            extra_args=extra_args
        )
        return md_content
    except Exception as e:
        print(f"Error converting RST to MD: {e}")
        return rst_content

def process_notebook(notebook_content):
    """Extract code examples and markdown from Jupyter notebook."""
    nb = nbformat.reads(notebook_content, nbformat.NO_CONVERT)
    
    md_output = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            md_output.append(cell.source)
        elif cell.cell_type == 'code':
            md_output.append(f"```python\n{cell.source}\n```")
            if hasattr(cell, 'outputs') and cell.outputs:
                for output in cell.outputs:
                    if 'text' in output:
                        md_output.append(f"```\n{output['text']}\n```")
                    elif 'data' in output and 'text/plain' in output['data']:
                        md_output.append(f"```\n{output['data']['text/plain']}\n```")
    
    return "\n\n".join(md_output)

def fetch_esgf_api_docs():
    """Fetch and process the ESGF API documentation."""
    api_url = "https://esgf.github.io/esg-search/ESGF_Search_RESTful_API.html"
    response = requests.get(api_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the main content
    content = soup.find('div', {'class': 'document'})
    if content:
        # Convert to markdown
        md_content = pypandoc.convert_text(
            str(content),
            'gfm',
            format='html',
            extra_args=['--wrap=none', '--columns=1000']
        )
        return md_content
    return ""

def fetch_api_docs():
    """Fetch and process the ESGF Python Client API documentation."""
    api_docs_url = "https://esgf-pyclient.readthedocs.io/en/latest/api.html"
    
    try:
        response = requests.get(api_docs_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract only the main content area (right side)
        api_content = soup.find('div', {'class': 'body'})  # This gets just the main content
        if not api_content:
            return ""
            
        # Process the content to maintain formatting
        content_md = []
        
        # Add the main title
        content_md.append("# API Reference\n\n")
        
        # Process each section
        for section in api_content.find_all(['div', 'section'], recursive=False):
            # Handle section titles
            title = section.find('h1') or section.find('h2') or section.find('h3')
            if title:
                level = int(title.name[1])  # h1 -> 1, h2 -> 2, etc.
                content_md.append(f"{'#' * level} {title.text.strip()}\n\n")
            
            # Handle code blocks
            for code in section.find_all('pre'):
                content_md.append(f"```python\n{code.text.strip()}\n```\n\n")
            
            # Handle warning boxes
            for warning in section.find_all('div', {'class': 'warning'}):
                content_md.append(f"> **Warning:**\n> {warning.text.strip()}\n\n")
            
            # Handle parameter lists
            for var_list in section.find_all('dl'):
                for dt, dd in zip(var_list.find_all('dt'), var_list.find_all('dd')):
                    param = dt.text.strip()
                    desc = dd.text.strip()
                    content_md.append(f"- **{param}** – {desc}\n")
                content_md.append("\n")
            
            # Handle regular paragraphs
            for p in section.find_all('p', recursive=False):
                content_md.append(f"{p.text.strip()}\n\n")
        
        return "\n".join(content_md)
        
    except Exception as e:
        print(f"Error processing API documentation: {e}")
        return ""

def fetch_and_process_docs():
    """Main function to fetch and process documentation."""
    # URLs
    concepts_url = "https://github.com/ESGF/esgf-pyclient/blob/master/docs/source/concepts.rst"
    api_docs_url = "https://esgf-pyclient.readthedocs.io/en/latest/api.html"
    demo_notebooks_url = "https://github.com/ESGF/esgf-pyclient/tree/master/notebooks/demo"
    examples_notebooks_url = "https://github.com/ESGF/esgf-pyclient/tree/master/notebooks/examples"
    
    # Process documentation
    md_content = ["# ESGF Python Client Documentation\n\n"]
    
    # Process concepts.rst
    try:
        rst_content = fetch_github_content(concepts_url)
        md_content.append(process_rst_to_md(rst_content))
        md_content.append("\n---\n")
    except Exception as e:
        print(f"Error processing concepts.rst: {e}")
    
    # Add Python Client API documentation
    md_content.append("\n# ESGF Python Client API Reference\n\n")
    api_docs = fetch_api_docs()
    if api_docs:
        md_content.append(api_docs)
        md_content.append("\n---\n")
    
    # Process notebooks from both directories
    md_content.append("\n# Code Examples from Notebooks\n\n")
    
    for notebooks_url in [demo_notebooks_url, examples_notebooks_url]:
        try:
            notebooks_response = requests.get(notebooks_url)
            notebooks_soup = BeautifulSoup(notebooks_response.text, 'html.parser')
            
            dir_name = "Demo" if "demo" in notebooks_url else "Examples"
            md_content.append(f"\n## {dir_name} Notebooks\n\n")
            
            for link in notebooks_soup.find_all('a', href=True):
                if link['href'].endswith('.ipynb'):
                    notebook_url = f"https://github.com{link['href']}"
                    try:
                        notebook_content = fetch_github_content(notebook_url)
                        md_content.append(f"\n### {link['href'].split('/')[-1]}\n")
                        md_content.append(process_notebook(notebook_content))
                        md_content.append("\n---\n")
                    except Exception as e:
                        print(f"Error processing notebook {notebook_url}: {e}")
        except Exception as e:
            print(f"Error accessing notebooks directory {notebooks_url}: {e}")
    
    # Add ESGF API documentation
    md_content.append("\n# General Information about the ESGF API\n\n")
    try:
        api_docs = fetch_esgf_api_docs()
        md_content.append(api_docs)
    except Exception as e:
        print(f"Error fetching ESGF API documentation: {e}")
    
    # Write to file
    output_path = Path("esgf_documentation.md")
    output_path.write_text("\n".join(md_content))
    
    return output_path

if __name__ == "__main__":
    output_file = fetch_and_process_docs()
    print(f"Documentation has been saved to {output_file}")

