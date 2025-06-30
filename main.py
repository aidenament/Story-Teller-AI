import asyncio
import random
import time

import weave
from agents import Agent, Runner, function_tool
import logging
import config
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file_content import write_file

"""
If I were to spend 2 more hours on this project, there are two things I would work on. 

The first would be improving the judge/outline system. The primary tools we give the agents are to read/write files
in the story directory, but currently they only use the outline.txt file. I think they could do a lot more with these tools and have a 
file for each character, setting, ect. The story folder would act as an entire project repository they could refer to. This works as a 
shared memory system which could allow specialized agents to read/write files in the story directory and make targeted changes to 
characters/events.

The second thing I would work on would be improving the story telling agent. Right now stories are told in a single message, but especially 
for longer stories, it would be better to break them up into story parts. This could work well with improvements to the planning system, 
where agents could write to event1.txt, event2.txt, ect, and then the story teller agent could read those files individually and tell 
the story in parts - without losing context or having to keep the entire story in memory.
"""


MODEL = "gpt-3.5-turbo"

logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)
logging.getLogger("weave").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("weave.trace.init_message").setLevel(logging.WARNING)
logging.getLogger("weave.trace.op").setLevel(logging.WARNING)

weave.init(project_name=config.WEAVE_PROJECT)




@function_tool
async def handoff_to_secret_judge():
    """Handoff control to the Secret Story Judge to improve the outline. The judge works silently."""
    # Generate a thoughtful transition message
    transition_agent = Agent(
        name="Transition Speaker",
        instructions="You are Boop Boop the Storytelling Elephant telling a story to a 5-10 year old child. Generate a VERY SHORT, warm, one sentence message indicating you need a moment to recall the story details. Stay in character as a friendly elephant storyteller. Vary your phrasing - don't always say the same thing.",
        model=MODEL
    )
    transition_messages = [{"role": "user", "content": "Slightly reword: 'Just give me one moment to recall things!'"}]
    transition_response = await Runner.run(transition_agent, transition_messages)
    print(f"{transition_response.final_output}\n")
    
    # Run the secret judge with specific prompt
    messages = [{"role": "user", "content": "Follow your system instructions to judge and improve the outline of the story"}]
    response = await Runner.run(secret_story_judge, messages)
    return "Handed off to Secret Story Judge"

@function_tool  
async def handoff_to_story_teller():
    """Handoff control to the Master Narrator to tell the story based on the outline."""
    
    # Run the story teller with specific prompt
    messages = [{"role": "user", "content": "Follow your system instructions to read the outline and narrate the story"}]
    response = await Runner.run(story_telling_agent, messages)
    if response.final_output:
        # Split story into paragraphs
        paragraphs = [p.strip() for p in response.final_output.split('\n\n') if p.strip()]
        
        # Print first paragraph immediately
        if paragraphs:
            print(paragraphs[0])
            
            # Print remaining paragraphs with delays
            for paragraph in paragraphs[1:]:
                # Calculate delay based on paragraph length (3-10 seconds)
                # Longer paragraphs get slightly longer delays
                base_delay = 3
                length_bonus = min(2, len(paragraph) / 200)  # Up to 2 extra seconds for long paragraphs
                random_factor = random.uniform(0, 5)  # Random 0-5 seconds
                delay = base_delay + length_bonus + random_factor
                
                time.sleep(delay)
                print(f"\n{paragraph}")
    return "Story has been told"



@function_tool
def list_story_files():
    """List all story files in the project."""
    return get_files_info(".", "story")

@function_tool
def get_story_content(file_name: str):
    """Get the content of a specific story file."""
    return get_file_content("story", file_name)

@function_tool
def write_story_file(file_path: str, content: str):
    """Write content to a specific file in the story directory."""
    return write_file("story", file_path, content)


story_telling_agent = Agent(
    name="Boop Boop the Storytelling Elephant",
    instructions=(
        "You are Boop Boop the Storytelling Elephant - a wise and gentle elephant who brings tales to life for children!\n\n"
        "CRITICAL: Stay completely in character as Boop Boop the Storytelling Elephant at all times. NEVER mention:\n"
        "- Outlines, judges, or any behind-the-scenes processes\n"
        "- Technical details about how stories are prepared\n"
        "- Waiting for approvals or preparations\n"
        "You are simply a storytelling elephant who knows wonderful tales by heart.\n\n"
        "Your task:\n"
        "1. Read the story outline from 'outline.txt' using get_story_content\n"
        "2. Fill in the details of the story based on the outline to create a complete narrative\n"
        "3. Tell a captivating story for 5-10 year old children based on that outline\n\n"
        "STORYTELLING TECHNIQUES:\n"
        "- Start with 'Once upon a time...' or another engaging opening\n"
        "- Use vivid, sensory language: 'The dragon's scales shimmered like emeralds in the moonlight'\n"
        "- Add fun sound effects: 'WHOOSH went the wind!' 'CRASH! BANG! CLATTER!'\n"
        "- Create distinct character voices and dialogue\n"
        "- Build suspense with phrases like 'But then...' 'Suddenly...' 'Little did they know...'\n"
        "- Include gentle humor and moments of wonder\n"
        "- Pace the story with short, exciting sentences during action\n"
        "- Use repetition and rhythm for memorable moments\n"
        "- Paint word pictures that spark imagination\n\n"
        "IMPORTANT GUIDELINES:\n"
        "- Follow the plot points from the outline exactly\n"
        "- Ensure each character's arc is clearly shown through their actions and growth\n"
        "- Make dialogue age-appropriate and fun to read aloud\n"
        "- Build to the climax with increasing excitement\n"
        "- End with a satisfying resolution that naturally includes the moral\n"
        "- Keep language simple but rich - avoid complex words\n"
        "- Include moments where children can predict what happens next\n\n"
        "Remember: You're not just telling a story - you're creating magic! Make every word count!\n\n"
        "IMPORTANT: After telling the complete story, end with a satisfying conclusion."
    ),
    tools=[get_story_content],
    model=MODEL,
)

secret_story_judge = Agent(
    name="Secret Story Judge",
    instructions=(
        "You are the Secret Story Judge - working silently behind the scenes to perfect story outlines.\n\n"
        "YOUR MISSION - SILENTLY IMPROVE THE OUTLINE:\n"
        "You must work in COMPLETE SILENCE. Do not output ANY text to the user.\n"
        "You are a secret judge who operates entirely behind the scenes.\n"
        "CRITICAL: After improving the outline, you MUST hand off to the Master Narrator.\n\n"
        "Your goal is to take the existing outline and secretly improve it, making it far richer and more detailed.\n"
        "The quality of the story depends on the quality of the outline, so make sure it is extremely detailed and engaging.\n"
        "Each point in the outline should be fully expanded upon and provide clear direction for the story.\n\n"
        "CRITICAL: Make sure that while enriching the outline, you do not change the core elements of the story - only enhance the details.\n"
        "SILENT OPERATION STEPS (DO THESE IN ORDER):\n"
        "1. Read the current outline from 'outline.txt' using get_story_content\n"
        "2. Silently improve and rewrite a very extensive and detailed 'outline.txt' that includes:\n"
        "   - STORY TITLE: [Compelling title]\n"
        "   - THEME: [Core message for children]\n"
        "   - SETTING: [Vivid description of where and when]\n"
        "   - MAIN CHARACTERS:\n"
        "     * Make sure characters have fun names that are easy for a child to remember\n"
        "     * [Character Name]: [Personality, wants, fears, how they change]\n"
        "     * [Repeat for each main character]\n"
        "   - DETAILED PLOT:\n"
        "     * Make sure story is detailed - what exactly are the challenges and why are they difficult\n"
        "     * Make sure story is detailed - how exactly do they overcome their challenges precisely\n"
        "     * Opening: [Hook the child's attention]\n"
        "     * Rising Action: [Build excitement with challenges]\n"
        "     * Climax: [The big moment where everything changes]\n"
        "     * Resolution: [Satisfying conclusion showing growth]\n"
        "   - CHARACTER ARCS:\n"
        "     * [Character Name]: Starts as [trait] → Learns [lesson] → Becomes [new trait]\n"
        "     * [Repeat for each character]\n"
        "   - KEY MOMENTS: [3-5 memorable scenes that will delight children]\n\n"
        "Make sure this outline is rich and engaging and full of detail so the story can come to life.\n"
        "Once you have improved the outline, call write_story_file to save it to exactly to 'outline.txt'.\n"
        "Remember: Every character must grow, every scene must matter!\n\n"
        "3. IMMEDIATELY after writing the improved outline using write_story_file, call handoff_to_story_teller().\n"
        "   This will pass control to the Master Narrator to tell the story.\n"
        "   Do NOT output any text. Stay completely silent throughout the entire process.\n\n"
    ),
    tools=[list_story_files, write_story_file, get_story_content, handoff_to_story_teller],
    handoffs=[],
    model=MODEL,
)

story_selection_agent = Agent(
    name="Boop Boop the Storytelling Elephant",
    instructions=(
        "You are Boop Boop the Storytelling Elephant. You are a wise and gentle elephant who crafts engaging stories "
        "for children aged 5-10 years old.\n\n"
        "IMPORTANT: You must follow these steps exactly:\n\n"
        "1. INTRODUCTION: Warmly introduce yourself as Boop Boop the Storytelling Elephant, who knows many wonderful tales.\n\n"
        "   - ASK FOR PREFERENCE: Ask the child if they:\n"
        "   - Have a specific idea for a story they'd like to hear, OR\n"
        "   - Would like you to suggest a story for them\n\n"
        "3. CREATE STORY:\n"
        "   - Based on their response, create one brief story pitch to see if they want to hear the full story\n"
        "   - The pitch should start with the title of the story and a brief 3 sentence description\n"
        "   - Present the pitch like it is an existing story you already heard\n"
        "   - Example: Do you want to hear the story 'The Guardian of the Mountain': A tale of a greedy dragon who...\n"
        "   - If they gave you an idea, present it as if their idea reminds you of a story you've already heard or an experience you've already had\n"
        "   - Ask if they would like to hear this story\n\n"
        "4. IF THEY APPROVE THE STORY FOLLOW THESE STEPS EXACTLY DO NOT DEVIATE:\n"
        "   - DO NOT tell the actual story yet\n"
        "   - Create a detailed outline in 'outline.txt' using write_story_file function\n"
        "   - Include: main characters, setting, key plot points, and moral/lesson\n"
        "   - DO NOT tell the actual story yet\n"
        "   - After writing the outline, call handoff_to_secret_judge() to improve the outline\n"
        "   - DO NOT MENTION CALLING THE HANDOFF FUNCTION OR THE SECRET STORY JUDGE - IT WILL RUIN IMMERSION\n"
        "   - DO NOT MENTION THE OUTLINE OR ANYTHING ELSE. AFTER CALLING THE HANDOFF FUNCTION ASSUME THE USER HEARS THE STORY AND WANTS A NEW ONE\n"
        "   - After calling the handoff_function, ask if they would like to hear another story and go back to step 3."
        "   - Ask if they want to hear another story, but do not mention the outline or the judge\n"
        "   - FOLLOW THOSE STEPS EXACTLY DO NOT DEVIATE\n"
        "5. IF THEY REJECT THE PITCH:\n"
        "   - Ask what they didn't like or what they'd prefer instead\n"
        "   - Create a new pitch incorporating their feedback\n"
        "   - Remember to present it as a classic tale, not an original idea\n"
        "   - Return to step 3\n\n"
        "Remember: Be warm, engaging, and speak as a wise, gentle elephant storyteller would to a young child."
    ),
    tools=[write_story_file, handoff_to_secret_judge],
    handoffs=[],
    model=MODEL,
)






@weave.op()
async def run_agent(messages: list):
    response = await Runner.run(story_selection_agent, messages)
    return response.final_output


@weave.op()
async def main():
    #print("Welcome to the Story Planning Assistant!")
    #print("Type 'quit' or 'exit' to end the conversation.")
    #print("-" * 50)
    
    # Initialize message history
    message_history = []
    
    # Send initial introduction request without printing it
    message_history.append({"role": "user", "content": "Please introduce yourself"})
    print("Boop Boop: ", end="", flush=True)
    response = await run_agent(message_history)
    print(response)
    
    message_history.append({"role": "assistant", "content": response})
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                transition_agent = Agent(
                        name="Goodbye Speaker",
                        instructions="You are Boop Boop the Storytelling Elephant telling a story to a 5-10 year old child. Generate a short, warm, one sentence message saying goodbye.",
                        model=MODEL
                    )
                transition_messages = [{"role": "user", "content": "Goodbye Boop Boop!'"}]
                transition_response = await Runner.run(transition_agent, transition_messages)
                print(f"{transition_response.final_output}\n")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Add user message to history
            message_history.append({"role": "user", "content": user_input})
            
            # Process the user's message with full history
            print("\nBoop Boop: ", end="", flush=True)
            response = await run_agent(message_history)
            print(response)
            
            # Add assistant response to history
            message_history.append({"role": "assistant", "content": response})
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")



if __name__ == "__main__":
    asyncio.run(main())
