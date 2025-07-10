import os
import uuid
import chainlit as cl

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    FilePurpose,
    ThreadMessageOptions,
    MessageRole,
    FileSearchTool
)
from azure.identity import DefaultAzureCredential

# 1) When the session starts, we initialize the state and send a prompt
@cl.on_chat_start
async def start():
    cl.user_session.set("session_id", str(uuid.uuid4()))
    cl.user_session.set("agent_id", None)
    cl.user_session.set("thread_id", None)
    cl.user_session.set("vector_store_id", None)
    await cl.Message(
        content="👋 Hello! To get started, upload a document (PDF, DOCX or TXT) using the clip 📎 or by dragging it."
    ).send()

# 2) Every message - whether text or file - comes through here
@cl.on_message
async def handler(msg: cl.Message):
    session_id       = cl.user_session.get("session_id")
    agent_id         = cl.user_session.get("agent_id")
    thread_id        = cl.user_session.get("thread_id")
    vector_store_id  = cl.user_session.get("vector_store_id")

    client = AgentsClient(
        endpoint=os.getenv("PROJECT_ENDPOINT"),
        credential=DefaultAzureCredential(),
    )

    # --- Case A: user has attached one or more files ---
    if msg.elements:
        await cl.Message(content="🗂️ Processing document(s)…").send()
        for file in msg.elements:
            # Upload file to Azure AI
            uploaded = client.files.upload_and_poll(
                file_path=file.path,
                purpose=FilePurpose.AGENTS
            )
            # If vector store doesn't exist yet, create it and the agent
            if not vector_store_id:
                vs = client.vector_stores.create_and_poll(
                    file_ids=[uploaded.id],
                    name=f"vs_{session_id}"
                )
                vector_store_id = vs.id
                cl.user_session.set("vector_store_id", vs.id)
                # Create agent pointing to the vector store
                fs_tool = FileSearchTool(vector_store_ids=[vs.id])
                agent = client.create_agent(
                    model=os.getenv("MODEL_NAME"),
                    name=f"agent_{session_id}",
                    instructions="You are an assistant that responds using the uploaded documents.",
                    tools=fs_tool.definitions,
                    tool_resources=fs_tool.resources,
                )
                cl.user_session.set("agent_id", agent.id)
                await cl.Message(content="✅ Agent created. You can now ask questions!").send()
            else:
                # Add the file to the existing vector store
                client.vector_store_file_batches.create_and_poll(
                    vector_store_id=vector_store_id,
                    file_ids=[uploaded.id]
                )
                await cl.Message(content="📄 Document added to existing vector store.").send()
        return

    # --- Case B: it's a text question ---
    # 1) If there's no agent, ask to upload a document first
    if not agent_id:
        await cl.Message(
            content="To get started, please upload at least one document first."
        ).send()
        return

    # 2) If there's no conversation thread, create thread + run
    if not thread_id:
        run = client.create_thread_and_process_run(
            agent_id=agent_id,
            thread={"messages": [
                ThreadMessageOptions(role="user", content=msg.content)
            ]}
        )
        thread_id = run.thread_id
        cl.user_session.set("thread_id", thread_id)
    else:
        # 3) Subsequent questions: insert message and process run
        client.messages.create(
            thread_id=thread_id,
            role=MessageRole.USER,
            content=msg.content
        )
        client.runs.create_and_process(
            thread_id=thread_id,
            agent_id=agent_id,
            additional_messages=[
                ThreadMessageOptions(role="user", content=msg.content)
            ]
        )

    # 4) Retrieve and send the agent's response
    text_content = client.messages.get_last_message_text_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT
    )
    await cl.Message(content=text_content.text.value).send()