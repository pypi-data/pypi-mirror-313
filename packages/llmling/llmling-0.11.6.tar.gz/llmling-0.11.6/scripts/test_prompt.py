from __future__ import annotations

import asyncio
import logging

from llmling.server.mcp_inproc_session import MCPInProcSession


# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("llmling")


async def main():
    # Use the test config which has some predefined prompts
    session = MCPInProcSession(config_path="E:/llmling/scripts/prompttest.yml")

    try:
        # Start the server
        await session.start()

        # Do handshake
        await session.do_handshake()

        # First list available prompts
        prompts = await session.list_prompts()
        print("\nAvailable prompts:", prompts)

        # Try to get a specific prompt
        if prompts:
            first_prompt = prompts[0]["name"]
            print(f"\nTrying to get prompt: {first_prompt}")
            result = await session.send_request("prompts/get", {"name": first_prompt})
            print("\nPrompt result:", result)

    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
