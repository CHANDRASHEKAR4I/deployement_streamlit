from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
import streamlit as st

# Initialize the language model (ChatGroq)
llm = ChatGroq(api_key="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", 
               model="llama3-70b-8192")

# Initialize the search tool (DUCKDUCKGO)
search_tool = DuckDuckGoSearchRun()

def Finance_assistance(age, work, information):

#                               ***AGENT SECTION***         

    
    # Define the Finance Researcher
    Researcher = Agent(
        role='Researcher',
        goal=""" 
            Conducting thorough research of financial markets, generating new knowledge through original research,
            identifying investment opportunities, managing risks, analyzing financial policies, forecasting market trends, 
            effectively communicating findings, and continuously learning and improving. 
            """,
        backstory='Extract and list out the required details for financial knowledge',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool],
    )

    # Define the mentor agent
    Analyst = Agent(
        role='Analyser',
        goal='Utilize data to provide informed mentoring',
        backstory='Analyze data and provide insights and assistance',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool],
    )

   #                          *** TASK SECTION ***                   
  
    # Define the task for the Researcher
    task1 = Task(
        description="Involves creating financial models, evaluating investment options, and assessing various types of risk.",
        agent=Researcher,
        expected_output=""" 
                        Explanation: short summary 
                        Bullet points only
                        """
    )

    # Define the task for the Analyst
    task2 = Task(
        description=f"By considering {age}, {work}, and {information}, analyze and provide assistance for their goals and personal circumstances.",
        agent=Analyst,
        expected_output=" Summarize and prioritize with points ",
        input_method="response"  # Input for this task comes from the response 
    )

    # Add the agents and tasks to the Crew
    crew = Crew(agents=[Researcher, Analyst], tasks=[task1, task2], verbose=2)

    # Get the crew to work
    result = crew.kickoff()
    json_result = {
        "result": result,
    }

    return json_result

    #return result     # facing error




# """                      STREAMLIT UI                    """

st.subheader("Let AI agents assist your Queries", divider="rainbow", anchor=False)

with st.sidebar:
    st.header("  Enter your details 👇")
    with st.form("my_form"):
        age = st.text_input("Please enter your age", placeholder="15")
        work = st.text_input("What are you doing?", placeholder= "Student/Self-employed/Working professional")
        information = st.text_area("Do you want to tell me something?", placeholder= " financial tips ", height=100)
        submitted = st.form_submit_button("Submit")

if submitted:
    with st.status("🤖 **Agents at work...**", state="running", expanded=False) as status:
        with st.container(height=500, border=False):
            result = Finance_assistance(age, work, information)
        status.update(label=" Done✅! check it ", state="complete", expanded=False)

    st.subheader("Here is my answer", anchor=False, divider="rainbow")
    st.json(result)



# tools need to be added - youtube and artcile