import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
import io

# Adjust the following imports based on your project structure
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

load_dotenv()

async def process_chunk(chunk, start_idx, total_records, model_client, termination_condition):
    """
    Process a single batch of data:
      - Convert the batch data into a dictionary format.
      - Create a prompt requesting agents to analyze the batch data
        and provide recommendations for basketball beginners.
      - Use the MultimodalWebSurfer agent to search for the latest
        basketball-related information (e.g., matches, rules, equipment),
        and integrate the search results into the recommendations.
      - Collect all response messages and return them.
    """
    # Convert data to dictionary format
    chunk_data = chunk.to_dict(orient='records')
    prompt = (
        f"Currently processing records {start_idx} to {start_idx + len(chunk) - 1} out of {total_records} total records.\n"
        f"Here is the batch data:\n{chunk_data}\n\n"
        "Please analyze the data above and provide comprehensive recommendations."
        "Pay special attention to:\n"
        "  1. Analyzing the benefits of basketball and why it is popular;\n"
        "  2. Using MultimodalWebSurfer to search external websites for the latest basketball information "
        "     (such as matches, rules, equipment) and integrating the search results into the response;\n"
        "  3. Providing specific recommendations and relevant reference information.\n"
        "Please collaborate to provide a complete and valuable recommendation."
    )
    
    # Create new agent and team instances for each batch
    local_data_agent = AssistantAgent("data_agent", model_client)
    local_web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    local_assistant = AssistantAgent("assistant", model_client)
    local_user_proxy = UserProxyAgent("user_proxy")
    local_team = RoundRobinGroupChat(
        [local_data_agent, local_web_surfer, local_assistant, local_user_proxy],
        termination_condition=termination_condition
    )
    
    messages = []
    async for event in local_team.run_stream(task=prompt):
        if isinstance(event, TextMessage):
            # Print which agent is currently running for tracking purposes
            print(f"[{event.source}] => {event.content}\n")
            messages.append({
                "batch_start": start_idx,
                "batch_end": start_idx + len(chunk) - 1,
                "source": event.source,
                "content": event.content,
                "type": event.type,
                "prompt_tokens": event.models_usage.prompt_tokens if event.models_usage else None,
                "completion_tokens": event.models_usage.completion_tokens if event.models_usage else None
            })
    return messages

async def main():
    try:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            print("Please check the GEMINI_API_KEY in the .env file.")
            return

        model_client = OpenAIChatCompletionClient(
            model="gemini-2.0-flash",
            api_key=gemini_api_key,
        )

        termination_condition = TextMentionTermination("exit")

        csv_file_path = "basketball_info.csv"
        chunk_size = 1000
        chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
        
        tasks = list(map(
            lambda idx_chunk: process_chunk(
                idx_chunk[1],
                idx_chunk[0] * chunk_size,
                len(chunks) * chunk_size,
                model_client,
                termination_condition
            ),
            enumerate(chunks)
        ))

        results = await asyncio.gather(*tasks)
        all_messages = [msg for batch in results for msg in batch]

        df_log = pd.DataFrame(all_messages)
        output_file = "all_conversation_log.csv"
        df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"All conversation logs have been saved to {output_file}")

    finally:
        # Ensure any necessary cleanup is performed here
        await model_client.close()  # Example cleanup if applicable

if __name__ == '__main__':
    asyncio.run(main())
