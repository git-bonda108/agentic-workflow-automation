#!/usr/bin/env python3
"""
Run the Producer agent from the command line.
Usage: python run_agent.py "Create a task for Mango Pod: longform edit for Client Alpha, due Friday"

Requires OPENAI_API_KEY. ClickUp is optional (demo mode if not set).
"""
import asyncio
import sys

from agents import Runner

from role_agents.producer_agent import get_producer_agent


async def main() -> None:
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "List ClickUp lists for Mango Pod."
    agent = get_producer_agent()
    result = await Runner.run(agent, message)
    print(result.final_output)
    if result.run_items:
        print("\n--- Tool calls ---")
        for item in result.run_items:
            if hasattr(item, "tool_name") and item.tool_name:
                print(f"  {item.tool_name}: {getattr(item, 'result', '')}")


if __name__ == "__main__":
    asyncio.run(main())
