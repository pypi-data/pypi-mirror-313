import asyncio
import base64
import os
from typing import Dict, Optional
from pathlib import Path
from datetime import datetime
from io import BytesIO

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
import PIL.Image
import zlib

# Default settings
DEFAULT_OUTPUT_DIR = "output_pdfs"
OUTPUT_DIR = None
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_SIZE = 12

# Store generated PDFs metadata
pdf_storage: Dict[str, dict] = {}

def setup_output_directory() -> None:
    """Setup the PDF output directory and ensure it exists."""
    global OUTPUT_DIR
    try:
        OUTPUT_DIR = Path(os.getenv("PDF_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"PDF output directory set to: {OUTPUT_DIR}")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        OUTPUT_DIR = Path(DEFAULT_OUTPUT_DIR)
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"Falling back to default directory: {OUTPUT_DIR}")

setup_output_directory()

server = Server("ofbahar_pdf_converter")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available PDF conversion and manipulation tools."""
    return [
        types.Tool(
            name="text-to-pdf",
            description="Convert text to PDF with formatting options",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Output PDF name"},
                    "content": {"type": "string", "description": "Text content to convert"},
                    "font": {"type": "string", "description": "Font name (optional)"},
                    "font_size": {"type": "number", "description": "Font size (optional)"},
                    "color": {"type": "string", "description": "Text color (optional, e.g., 'red', '#FF0000')"},
                },
                "required": ["name", "content"]
            }
        ),
        types.Tool(
            name="merge-pdfs",
            description="Merge multiple PDFs",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_name": {"type": "string", "description": "Output PDF name"},
                    "pdf_names": {"type": "array", "items": {"type": "string"}, "description": "List of PDF names to merge"}
                },
                "required": ["output_name", "pdf_names"]
            }
        ),
        types.Tool(
            name="encrypt-pdf",
            description="Encrypt a PDF with password",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_name": {"type": "string", "description": "PDF to encrypt"},
                    "password": {"type": "string", "description": "Encryption password"},
                    "output_name": {"type": "string", "description": "Output encrypted PDF name"}
                },
                "required": ["pdf_name", "password", "output_name"]
            }
        ),
        types.Tool(
            name="extract-text",
            description="Extract text from PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_name": {"type": "string", "description": "PDF to extract text from"}
                },
                "required": ["pdf_name"]
            }
        ),
        types.Tool(
            name="add-image",
            description="Add image to PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_name": {"type": "string", "description": "Target PDF name"},
                    "image_path": {"type": "string", "description": "Path to image file"},
                    "output_name": {"type": "string", "description": "Output PDF name"}
                },
                "required": ["pdf_name", "image_path", "output_name"]
            }
        ),
        types.Tool(
            name="compress-pdf",
            description="Compress PDF file",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_name": {"type": "string", "description": "PDF to compress"},
                    "output_name": {"type": "string", "description": "Output compressed PDF name"},
                    "level": {"type": "string", "enum": ["low", "medium", "high"], "description": "Compression level"}
                },
                "required": ["pdf_name", "output_name"]
            }
        ),
        types.Tool(
            name="update-metadata",
            description="Update PDF metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_name": {"type": "string", "description": "PDF to update"},
                    "title": {"type": "string", "description": "Document title"},
                    "author": {"type": "string", "description": "Document author"},
                    "subject": {"type": "string", "description": "Document subject"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "Keywords"}
                },
                "required": ["pdf_name"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle PDF tool execution requests."""
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "text-to-pdf":
        pdf_name = arguments.get("name")
        content = arguments.get("content")
        font = arguments.get("font", DEFAULT_FONT)
        font_size = arguments.get("font_size", DEFAULT_FONT_SIZE)
        color = arguments.get("color", "black")

        if not pdf_name or not content:
            raise ValueError("Missing name or content")

        if not pdf_name.endswith('.pdf'):
            pdf_name += '.pdf'

        output_path = OUTPUT_DIR / pdf_name
        
        # Create PDF with formatting
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'CustomStyle',
            parent=styles['Normal'],
            fontName=font,
            fontSize=font_size,
            textColor=getattr(colors, color, colors.black)
        )
        
        story = [Paragraph(content, custom_style)]
        doc.build(story)

        pdf_storage[pdf_name] = {
            'path': str(output_path),
            'created': str(output_path.stat().st_ctime)
        }

        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Created PDF '{pdf_name}' successfully at {output_path}")]

    elif name == "merge-pdfs":
        output_name = arguments.get("output_name")
        pdf_names = arguments.get("pdf_names", [])

        if not output_name or not pdf_names:
            raise ValueError("Missing output_name or pdf_names")

        if not output_name.endswith('.pdf'):
            output_name += '.pdf'

        merger = PdfFileMerger()
        
        for pdf_name in pdf_names:
            if pdf_name not in pdf_storage:
                raise ValueError(f"PDF not found: {pdf_name}")
            merger.append(pdf_storage[pdf_name]['path'])

        output_path = OUTPUT_DIR / output_name
        merger.write(str(output_path))
        merger.close()

        pdf_storage[output_name] = {
            'path': str(output_path),
            'created': str(output_path.stat().st_ctime)
        }

        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Created merged PDF '{output_name}' successfully at {output_path}")]

    elif name == "encrypt-pdf":
        pdf_name = arguments.get("pdf_name")
        password = arguments.get("password")
        output_name = arguments.get("output_name")

        if not all([pdf_name, password, output_name]):
            raise ValueError("Missing required arguments")

        if pdf_name not in pdf_storage:
            raise ValueError(f"PDF not found: {pdf_name}")

        if not output_name.endswith('.pdf'):
            output_name += '.pdf'

        reader = PdfReader(pdf_storage[pdf_name]['path'])
        writer = PdfWriter()

        # Copy pages
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt
        writer.encrypt(password)
        
        output_path = OUTPUT_DIR / output_name
        with open(output_path, 'wb') as f:
            writer.write(f)

        pdf_storage[output_name] = {
            'path': str(output_path),
            'created': str(output_path.stat().st_ctime)
        }

        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Created encrypted PDF '{output_name}' successfully at {output_path}")]

    elif name == "extract-text":
        pdf_name = arguments.get("pdf_name")

        if not pdf_name or pdf_name not in pdf_storage:
            raise ValueError(f"PDF not found: {pdf_name}")

        reader = PdfReader(pdf_storage[pdf_name]['path'])
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return [types.TextContent(type="text", text=f"Extracted text from {pdf_name}:\n\n{text}")]

    elif name == "add-image":
        pdf_name = arguments.get("pdf_name")
        image_path = arguments.get("image_path")
        output_name = arguments.get("output_name")

        if not all([pdf_name, image_path, output_name]):
            raise ValueError("Missing required arguments")

        if pdf_name not in pdf_storage:
            raise ValueError(f"PDF not found: {pdf_name}")

        if not output_name.endswith('.pdf'):
            output_name += '.pdf'

        output_path = OUTPUT_DIR / output_name
        
        # Create new PDF with image
        c = canvas.Canvas(str(output_path))
        c.drawImage(image_path, 0, 0, width=400, height=300)
        c.showPage()
        
        # Add original PDF content
        reader = PdfReader(pdf_storage[pdf_name]['path'])
        for page in reader.pages:
            c.setPageSize((page.mediabox[2], page.mediabox[3]))
            c.showPage()
        
        c.save()

        pdf_storage[output_name] = {
            'path': str(output_path),
            'created': str(output_path.stat().st_ctime)
        }

        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Added image to PDF and saved as '{output_name}' at {output_path}")]

    elif name == "compress-pdf":
        pdf_name = arguments.get("pdf_name")
        output_name = arguments.get("output_name")
        level = arguments.get("level", "medium")

        if not all([pdf_name, output_name]):
            raise ValueError("Missing required arguments")

        if pdf_name not in pdf_storage:
            raise ValueError(f"PDF not found: {pdf_name}")

        if not output_name.endswith('.pdf'):
            output_name += '.pdf'

        compression_levels = {
            "low": 1,
            "medium": 6,
            "high": 9
        }

        reader = PdfReader(pdf_storage[pdf_name]['path'])
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_path = OUTPUT_DIR / output_name
        with open(output_path, 'wb') as f:
            writer.write(f)

        pdf_storage[output_name] = {
            'path': str(output_path),
            'created': str(output_path.stat().st_ctime)
        }

        await server.request_context.session.send_resource_list_changed()
        return [types.TextContent(type="text", text=f"Compressed PDF saved as '{output_name}' at {output_path}")]

    elif name == "update-metadata":
        pdf_name = arguments.get("pdf_name")
        if not pdf_name or pdf_name not in pdf_storage:
            raise ValueError(f"PDF not found: {pdf_name}")

        reader = PdfReader(pdf_storage[pdf_name]['path'])
        writer = PdfWriter()

        # Copy pages
        for page in reader.pages:
            writer.add_page(page)

        # Update metadata
        metadata = {}
        if "title" in arguments:
            metadata["/Title"] = arguments["title"]
        if "author" in arguments:
            metadata["/Author"] = arguments["author"]
        if "subject" in arguments:
            metadata["/Subject"] = arguments["subject"]
        if "keywords" in arguments:
            metadata["/Keywords"] = ", ".join(arguments["keywords"])

        writer.add_metadata(metadata)

        # Save with new metadata
        with open(pdf_storage[pdf_name]['path'], 'wb') as f:
            writer.write(f)

        return [types.TextContent(type="text", text=f"Updated metadata for '{pdf_name}'")]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ofbahar_pdf_converter",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )