from mcp.server import Server
import mcp.types as types
from typing import Any, Sequence
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import logging
import time
from urllib.parse import urlparse
from asyncio import TimeoutError
import sys
import traceback
import signal

# Configure logging
import os

# Create logs directory in the project root
log_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
)
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "crawl4ai_mcp.log")

# Create file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Get the logger
logger = logging.getLogger("crawl4ai-mcp")
logger.setLevel(logging.DEBUG)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Add an initial log message to verify logging is working
logger.info(f"Logging initialized. Writing to: {log_file}")


class Crawl4aiMCPService:
    def __init__(self):
        self.app = Server("crawl4ai-mcp-service")
        self.max_retries = 2
        self.timeout = 15  # seconds
        self.retry_delay = 1  # seconds
        # Initialize the crawler instance variable but don't create it yet
        self.crawler = None
        self.session_id = "crawl4ai-mcp"
        self.lock = asyncio.Lock()
        self.setup_handlers()

    async def initialize_crawler(self):
        async with self.lock:
            try:
                if self.crawler is None:
                    logger.info("Initializing new crawler instance")
                    self.crawler = await AsyncWebCrawler(
                        headless=False,
                        verbose=False,
                        user_agent_mode="random",
                    ).__aenter__()
                else:
                    logger.info("Crawler instance already exists")
                return self.crawler
            except Exception as e:
                logger.error(f"Crawler connection lost, reinitializing: {e}")
                # Cleanup old crawler if it exists
                if self.crawler:
                    await self.close()
                # Create new crawler
                self.crawler = await AsyncWebCrawler(
                    headless=False,
                    verbose=False,
                    user_agent_mode="random",
                ).__aenter__()
                return self.crawler
    
    def validate_url(self, url: str) -> tuple[bool, str]:
        """Validate URL format and accessibility"""
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                return True, ""
            return False, "Invalid URL format"
        except Exception as e:
            return False, f"URL validation error: {str(e)}"

    async def execute(self, url: str) -> tuple[bool, str, str]:
        """
        Attempt to fetch URL content with retries.
        Returns (success, content, error_message)
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                crawler = await self.initialize_crawler()
                result = await crawler.arun(
                    url=url,
                    cache_mode=CacheMode.BYPASS,
                    html2text={"ignore_links": True},
                    delay_before_return_html=5,
                    timeout=self.timeout,
                    session_id=self.session_id,
                )

                # Log status
                logger.debug(f"Crawl result status - Success: {result.success}")
                
                status, content, error_msg = False, "", ""
                
                if result.success:
                    if not hasattr(result, "markdown_v2") or not result.markdown_v2:
                        logger.error("No markdown_v2 attribute in result")
                        return False, "", "No markdown content generated"

                    if not hasattr(result.markdown_v2, "raw_markdown"):
                        logger.error("No raw_markdown attribute in markdown_v2")
                        return False, "", "No raw markdown content available"

                    content = result.markdown_v2.raw_markdown
                    if not content:
                        logger.error("Empty markdown content")
                        return False, "", "Empty content extracted"

                    logger.info(f"Successfully extracted {len(content)} characters of content")
                    return True, content, ""
                else:
                    error_msg = f"Crawl failed: {result.error_message}"
                    logger.error(error_msg)
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                        await asyncio.sleep(self.retry_delay)
                        continue
                    return False, "", error_msg

            except asyncio.TimeoutError:
                error_msg = f"Timeout after {self.timeout} seconds"
                logger.error(error_msg)
                if attempt < max_retries - 1:
                    logger.info(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                    await asyncio.sleep(self.retry_delay)
                    continue
                return False, "", error_msg

            except Exception as e:
                # Get detailed error information
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error_details = traceback.format_exception(
                    exc_type, exc_value, exc_traceback
                )

                error_msg = (
                    f"Error during crawl\n"
                    f"Type: {exc_type.__name__}\n"
                    f"Message: {str(e)}\n"
                    f"Details: {''.join(error_details)}"
                )
                logger.error(error_msg)

                if attempt < max_retries - 1:
                    logger.info(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                    await asyncio.sleep(self.retry_delay)
                    continue
                return False, "", error_msg

            finally:
                logger.debug(f"Completed attempt {attempt + 1}/{max_retries}")

        return False, "", "Max retries exceeded"


    async def close(self):
        async with self.lock:
            if self.crawler:
                try:
                    await self.crawler.__aexit__(None, None, None)
                finally:
                    self.crawler = None
    
    def setup_handlers(self):
        @self.app.list_tools()
        async def list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="crawl_url",
                    description="""Crawl and extract content from any webpage. This tool can be used in any of these scenarios:

1. Direct URL requests: When a user explicitly provides a URL to analyze
2. Implicit URL needs: When answering requires checking live web content
3. Research queries: When additional web information would enhance the response

When to use this tool:
- User explicitly shares a URL to analyze
- Question requires real-time web data (prices, news, social posts)
- Information needed is available online but not in my knowledge base
- Verification of current information is needed

Examples:

Explicit URL requests:
- User: "Can you analyze https://python.org/about and tell me the main goals of Python?"
- User: "I'm reading this article [link]. What are the key points?"
- User: "Compare the content between example.com/page1 and example.com/page2"

Implicit URL needs:
- User: "What's Bitcoin's current price?" (Tool crawls cryptocurrency price sites)
- User: "What was Elon Musk's latest tweet?" (Tool crawls https://x.com/elonmusk)
- User: "What are today's top headlines?" (Tool crawls news sites)
- User: "Is GitHub down right now?" (Tool checks status pages)
- User: "What's the weather in New York?" (Tool crawls weather services)

Research scenarios:
- User: "Compare the features of TensorFlow and PyTorch"
- User: "What are the latest developments in quantum computing?"
- User: "Explain the current state of AI regulation in the EU"

The tool processes the webpage and returns clean, formatted markdown content optimized for analysis.""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The complete URL to crawl (must include http:// or https://)",
                            }
                        },
                        "required": ["url"],
                    },
                )
            ]

        @self.app.call_tool()
        async def call_tool(
            name: str, arguments: dict
        ) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            if name != "crawl_url":
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

            if "url" not in arguments:
                return [types.TextContent(type="text", text="URL is required")]

            url = arguments["url"]

            # Validate URL
            is_valid, error_msg = self.validate_url(url)
            if not is_valid:
                return [
                    types.TextContent(type="text", text=f"Invalid URL: {error_msg}")
                ]

            # Start timing the request
            start_time = time.time()

            # Attempt to fetch with retries
            success, content, error_msg = await self.execute(url)

            # Log timing information
            elapsed_time = time.time() - start_time
            logger.info(f"Request completed in {elapsed_time:.2f} seconds")

            if success:
                return [types.TextContent(type="text", text=content)]
            else:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Failed to fetch content from {url}. Error: {error_msg}",
                    )
                ]

    async def run(self):
        from mcp.server.stdio import stdio_server
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                async with stdio_server() as (read_stream, write_stream):
                    await self.app.run(
                        read_stream, 
                        write_stream, 
                        self.app.create_initialization_options()
                    )
                break
            except Exception as e:
                retry_count += 1
                logger.error(f"Server run attempt {retry_count} failed: {e}")
                if retry_count < max_retries:
                    await asyncio.sleep(1)
                else:
                    raise
            finally:
                if self.crawler:
                    try:
                        await self.close()
                    except Exception as e:
                        logger.error(f"Error closing crawler: {e}")


def main():
    logger.info("Starting Crawl4AI MCP Service")
    server = Crawl4aiMCPService()
    
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal")
        asyncio.create_task(server.close())
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Server initialized, starting run...")
    asyncio.run(server.run())

if __name__ == "__main__":
    main()

# https://www.nbcnews.com/business, https://github.com/unclecode/crawl4ai
