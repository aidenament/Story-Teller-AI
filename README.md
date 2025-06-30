# Story Teller 🐘

An interactive AI-powered storytelling application featuring Boop Boop the Storytelling Elephant, designed to create and narrate engaging stories for children aged 5-10 years old. This is an interview project for Hippocratic AI.

## Overview

Story Teller is a multi-agent AI system that creates personalized, age-appropriate stories through an interactive conversation with children. The application uses a sophisticated orchestration of AI agents to generate, refine, and tell stories that capture children's imagination. The default model for this project is gpt-3.5-turbo.

## Features

- **Interactive Story Creation**: Children can request specific story ideas or let Boop Boop suggest one
- **Multi-Agent System**: 
  - **Story Selection Agent**: Warmly interacts with children to understand their story preferences
  - **Secret Story Judge**: Works behind the scenes to enhance story outlines with rich details
  - **Story Telling Agent**: Brings stories to life with vivid narration and engaging language
- **Age-Appropriate Content**: Stories are carefully crafted for 5-10 year olds with simple yet rich language
- **Engaging Narration**: Uses sound effects, vivid descriptions, and pacing to keep children engaged
- **Educational Value**: Each story includes a moral or lesson naturally woven into the narrative

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aidenament/story_teller.git
cd story_teller
```

2. Make a virtual enviornment
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root. Add your OpenAI API and Weights and Biases keys:
```
OPENAI_API_KEY=your_api_key_here
WANDB_API_KEY=your_api_key_here_again
```

## Usage

Run the application:
```bash
python main.py
```

The application will:
1. Introduce Boop Boop the Storytelling Elephant
2. Ask if you have a specific story idea or would like a suggestion
3. Create a story outline based on your preferences
4. Tell the complete story with engaging details and pacing

To exit the application, type `quit`, `exit`, or `bye`.


## How It Works

![Block Diagram](Diagram.png)

1. **Story Selection**: Boop Boop interacts with the child to understand their story preferences
2. **Outline Creation**: Based on the child's input, a detailed story outline is created
3. **Outline Enhancement**: The Secret Story Judge silently improves the outline with rich details
4. **Story Narration**: Boop Boop reads the enhanced outline and tells a complete, engaging story
5. **Paced Delivery**: The story is delivered in paragraphs with natural pacing for better engagement

## Future Enhancements

If I were to spend 2 more hours on this project, there are two things I would work on. 

1. Improve the judge/outline system. The primary tools we give the agents are to read/write files in the story directory, but currently they only use the outline.txt file. I think they could do a lot more with these tools and have a file for each character, setting, ect. The story folder would act as an entire project repository they could refer to. This folder works as a shared memory system which could allow specialized agents to read/write files in the story directory and make targeted changes to characters/events.

2. Improve the story telling agent. Right now stories are told in a single message, but especially for longer stories, it would be better to break them up into story parts. This could work well with improvements to the planning system, where agents could write to event1.txt, event2.txt, ect, and then the story teller agent could read those files individually and tell the story in parts - without losing context or having to keep the entire story in memory.

## Requirements
- OpenAI API key
- Weights and Biases API key (for using weave)
- Dependencies listed in `requirements.txt`
