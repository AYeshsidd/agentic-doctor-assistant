import chainlit as cl
from agents import Runner, SQLiteSession ,enable_verbose_stdout_logging
from main import Main_agent, config  
session = SQLiteSession("chat_user","conversations.db")
enable_verbose_stdout_logging()

@cl.on_message
async def message(message: cl.Message):
    user_input = message.content

    try:
         response = await Runner.run(Main_agent, user_input, run_config=config,session=session)
         
         await cl.Message( content=f"🤖AI Response: {response.final_output}").send()
    
    except Exception as e:
        await cl.Message(content=f"⚠️ Error occur: {str(e)}").send()

@cl.on_chat_start

async def chat_history():
    await cl.Message(content=f"### 🤖🩺 Meet Your AI Health & Greeting Duo — Ask a Medical Question or Just Say Hi!\n").send()
   
