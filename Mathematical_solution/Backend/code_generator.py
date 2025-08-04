from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew

load_dotenv()  

def generate_code(prompt: str) -> str:
    
    llm = LLM(
        model="gemini/gemini-2.0-flash",  
        temperature=0.1
    )

    
    manim_assistant = Agent(
        role="Manim Code Generating Agent",
        goal="Generate Manim code for math visualizations",
        backstory="A highly skilled agent who creates educational, clear and elegant Manim animations.",
        verbose=True,
        llm=llm
    )


    agents_task = Task(
        description=f"""Take the following prompt and generate Manim code that visualizes it.
        Use Manim ce for the newest code structure and less error
        Ensure the code is well-structured, with a clear class name and visuals.
        Prompt:
        '''{prompt}'''""",
        agent=manim_assistant,
        expected_output="A well-structured Manim code snippet with a clear class name and visuals also with least error possible.",
    )

    
    crew = Crew(
        agents=[manim_assistant],
        tasks=[agents_task],
        verbose=True
    )

    result = crew.kickoff()
    
    return str(result.tasks_output[0].raw)
