from agents import Agent , SQLiteSession ,  AsyncOpenAI ,  OpenAIChatCompletionsModel , RunConfig ,set_tracing_disabled 
import os 
from dotenv import load_dotenv

load_dotenv()
# enable_verbose_stdout_logging()
set_tracing_disabled(True)
groq_key = os.getenv('GROQ_API_KEY')
Base_url = os.getenv('BASE_URL_GROQ')

client = AsyncOpenAI(
    api_key=groq_key,
    base_url=Base_url,
)

model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=client
)

config = RunConfig(
  model=model,
  tracing_disabled = True,
  model_provider=client
  
)
doctor_agent: Agent = Agent( 
  name="professional doctor",
  model=model,
  handoff_description="you are experienced and expert health advisor",
   instructions=""" 
 - You are a senior doctor.
 - Your answer should not exceed to 8 lines  
 - DO NOT reply if the question is not related to health or sickness. 
 - Do NOT generate answer if question are other then health or medical advice you can simply say I cant say anything". 
   """ )

greeting_agent:Agent = Agent(
name="welcome agent", 
instructions="""
    - You are an excellent agent in handling greetings messages.
    - Your answer should not exceed to 2 linee
    - Only generate your answer when question OR prompt is related to greeting's
    - Your answer should be in a sweet and professional tone
    - you will handle messages like short conversations
    """,
handoff_description= 
       "Speacialist in handling prompts of greetings or normal conversations ",
model=model, 
)

Main_agent = Agent( 
    name="General Agent",
    instructions="""
    You are a helpful assistant that delegates tasks based on user queries.
    - Hand off to the Doctor Agent if the query is related to health or medicine.
    - Hand off to the Greeting Agent if the query involves greetings or small talk.
    - Answer directly if the user asks about chat history.
    - If none of the above applies, respond: "Sorry, I'm not trained for that topic."  
    """,

  handoffs=[doctor_agent,greeting_agent],
  handoff_description="You are helpfull assistatnt delegate task according to given query",
  model=model
)
session = SQLiteSession("USER_1","conversations.db")

# while True:
#   prompt= input("Hello, how can i hep you: ")
#   if prompt in ("exit","quiet"):
#      break
#   async def run_():
#    agent_Response  = await Runner.run(Main_agent,prompt,run_config = config,session=session) 
#    print(agent_Response.final_output)
#   asyncio.run(run_())
