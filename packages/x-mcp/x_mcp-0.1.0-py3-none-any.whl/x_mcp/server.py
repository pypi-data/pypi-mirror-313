import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Any, Sequence
from dotenv import load_dotenv
import tweepy
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    LoggingLevel,
    EmptyResult,
)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("x_mcp")

# Get Twitter API credentials from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise ValueError("Twitter API credentials are required")

# Initialize Tweepy client with OAuth 2.0
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Create the MCP server instance
server = Server("x_mcp")

# Implement tool handlers
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for interacting with Twitter/X."""
    return [
        Tool(
            name="create_draft_tweet",
            description="Create a draft tweet",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the tweet",
                    },
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="create_draft_thread",
            description="Create a draft tweet thread",
            inputSchema={
                "type": "object",
                "properties": {
                    "contents": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "An array of tweet contents for the thread",
                    },
                },
                "required": ["contents"],
            },
        ),
        Tool(
            name="list_drafts",
            description="List all draft tweets and threads",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="publish_draft",
            description="Publish a draft tweet or thread",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft_id": {
                        "type": "string",
                        "description": "ID of the draft to publish",
                    },
                },
                "required": ["draft_id"],
            },
        ),
        Tool(
            name="delete_draft",
            description="Delete a draft tweet or thread",
            inputSchema={
                "type": "object",
                "properties": {
                    "draft_id": {
                        "type": "string",
                        "description": "ID of the draft to delete",
                    },
                },
                "required": ["draft_id"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls for creating Twitter/X drafts."""
    if name == "create_draft_tweet":
        return await handle_create_draft_tweet(arguments)
    elif name == "create_draft_thread":
        return await handle_create_draft_thread(arguments)
    elif name == "list_drafts":
        return await handle_list_drafts(arguments)
    elif name == "publish_draft":
        return await handle_publish_draft(arguments)
    elif name == "delete_draft":
        return await handle_delete_draft(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_create_draft_tweet(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "content" not in arguments:
        raise ValueError("Invalid arguments for create_draft_tweet")
    content = arguments["content"]
    try:
        # Simulate creating a draft by storing it locally
        draft = {"content": content, "timestamp": datetime.now().isoformat()}
        # Ensure drafts directory exists
        os.makedirs("drafts", exist_ok=True)
        # Save the draft to a file
        draft_id = f"draft_{int(datetime.now().timestamp())}.json"
        with open(os.path.join("drafts", draft_id), "w") as f:
            json.dump(draft, f, indent=2)
        logger.info(f"Draft tweet created: {draft_id}")
        return [
            TextContent(
                type="text",
                text=f"Draft tweet created with ID {draft_id}",
            )
        ]
    except Exception as e:
        logger.error(f"Error creating draft tweet: {str(e)}")
        raise RuntimeError(f"Error creating draft tweet: {str(e)}")

async def handle_create_draft_thread(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "contents" not in arguments:
        raise ValueError("Invalid arguments for create_draft_thread")
    contents = arguments["contents"]
    if not isinstance(contents, list) or not all(isinstance(item, str) for item in contents):
        raise ValueError("Invalid contents for create_draft_thread")
    try:
        draft = {"contents": contents, "timestamp": datetime.now().isoformat()}
        # Ensure drafts directory exists
        os.makedirs("drafts", exist_ok=True)
        # Save the draft to a file
        draft_id = f"thread_draft_{int(datetime.now().timestamp())}.json"
        with open(os.path.join("drafts", draft_id), "w") as f:
            json.dump(draft, f, indent=2)
        logger.info(f"Draft thread created: {draft_id}")
        return [
            TextContent(
                type="text",
                text=f"Draft thread created with ID {draft_id}",
            )
        ]
    except Exception as e:
        logger.error(f"Error creating draft thread: {str(e)}")
        raise RuntimeError(f"Error creating draft thread: {str(e)}")

async def handle_list_drafts(arguments: Any) -> Sequence[TextContent]:
    try:
        drafts = []
        if os.path.exists("drafts"):
            for filename in os.listdir("drafts"):
                filepath = os.path.join("drafts", filename)
                with open(filepath, "r") as f:
                    draft = json.load(f)
                drafts.append({"id": filename, "draft": draft})
        return [
            TextContent(
                type="text",
                text=json.dumps(drafts, indent=2),
            )
        ]
    except Exception as e:
        logger.error(f"Error listing drafts: {str(e)}")
        raise RuntimeError(f"Error listing drafts: {str(e)}")

async def handle_publish_draft(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "draft_id" not in arguments:
        raise ValueError("Invalid arguments for publish_draft")
    draft_id = arguments["draft_id"]
    filepath = os.path.join("drafts", draft_id)
    if not os.path.exists(filepath):
        raise ValueError(f"Draft {draft_id} does not exist")
    try:
        with open(filepath, "r") as f:
            draft = json.load(f)
        if "content" in draft:
            # Single tweet
            content = draft["content"]
            response = client.create_tweet(text=content)
            tweet_id = response.data['id']
            logger.info(f"Published tweet ID {tweet_id}")
            # Delete the draft after publishing
            os.remove(filepath)
            return [
                TextContent(
                    type="text",
                    text=f"Draft {draft_id} published as tweet ID {tweet_id}",
                )
            ]
        elif "contents" in draft:
            # Thread
            contents = draft["contents"]
            # Publish the thread
            last_tweet_id = None
            for content in contents:
                if last_tweet_id is None:
                    response = client.create_tweet(text=content)
                else:
                    response = client.create_tweet(text=content, in_reply_to_tweet_id=last_tweet_id)
                last_tweet_id = response.data['id']
                await asyncio.sleep(1)  # Avoid hitting rate limits
            logger.info(f"Published thread starting with tweet ID {last_tweet_id}")
            # Delete the draft after publishing
            os.remove(filepath)
            return [
                TextContent(
                    type="text",
                    text=f"Draft {draft_id} published as thread starting with tweet ID {last_tweet_id}",
                )
            ]
        else:
            raise ValueError(f"Invalid draft format for {draft_id}")
    except tweepy.TweepError as e:
        logger.error(f"Twitter API error: {e}")
        raise RuntimeError(f"Error publishing draft {draft_id}: {e}")
    except Exception as e:
        logger.error(f"Error publishing draft {draft_id}: {str(e)}")
        raise RuntimeError(f"Error publishing draft {draft_id}: {str(e)}")


async def handle_delete_draft(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "draft_id" not in arguments:
        raise ValueError("Invalid arguments for delete_draft")
    
    draft_id = arguments["draft_id"]
    filepath = os.path.join("drafts", draft_id)
    
    try:
        if not os.path.exists(filepath):
            raise ValueError(f"Draft {draft_id} does not exist")
        
        os.remove(filepath)
        logger.info(f"Deleted draft: {draft_id}")
        
        return [
            TextContent(
                type="text",
                text=f"Successfully deleted draft {draft_id}",
            )
        ]
    except Exception as e:
        logger.error(f"Error deleting draft {draft_id}: {str(e)}")
        raise RuntimeError(f"Error deleting draft {draft_id}: {str(e)}")
# Implement the main function
async def main():
    import mcp
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())