Pymon is a Discord assistant bot inspired by Paimon, the character known for serving as the Traveler's companion throughout their journey across Teyvat – the vast open world in which Genshin Impact takes place. Our bot answers questions about the game’s lore, mechanics, quests, characters, items etc., using a combination of vector database queries and web search.

## Features

The `vdb_search.py` module is what interacts with the Qdrant solution. Through VDB search, Pymon gains entry to a vector database synchronized with the [Genshin Impact Wiki Fandom](https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki). 

On the other hand, the `web_search.py` module utilizes DuckDuckGo Search API to scrape the internet for content relevant to the user's prompt, leveraging the results with external data with web results.

Merging both these search results, they are formatted and added to Pymon’s prompt using the RAG approach, to provide both accurate and up-to-date information.

## Code structure

1. `bot.py`:
    - This file contains the main event loop for the Discord bot, it handles incoming messages from users.
    - Utilizes triggers defined in `triggers.py` in order to determine when to respond to users’ messages.
    - The bot's responses are generated using the functions from `chat.py`, which interacts with the Gemini API.
2. `chat.py`:
    - Implements the main chatbot functionality using the Gemini API.
    - The `chat` function processes user queries by generating prompts for the Gemini API based on the query and search results.
    - It manages conversation history and uses the Gemini model to generate responses.
3. `vdb_search.py`:
    - Implements database search functionality using Qdrant for vector database search.
    - The `search_vdb` function queries a vector database using Qdrant and retrieves relevant results.
    - It formats the database search results into a markdown string for display.
4. `web_search.py`:
    - Provides functions for web search using DuckDuckGo.
    - The `search_DDG` function sends a query to DuckDuckGo and retrieves search results.
    - Formats them into a list containing the content and the link.
    - Then formats the search result list into a markdown string for display.

## Technologies

- Google Generative AI (Gemini) API
- Sentence Transformers
- DuckDuckGo Search API
- Qdrant
- HuggingFace Hub
- Discord.py
- Docker

## How to use

1. Invite Pymon to your Discord server using this [link](https://discord.com/oauth2/authorize?client_id=950329569758568498&permissions=395137071168&scope=bot).
2. Send your query to Pymon by either : 
    1. Pinging her in your question.
    2. Start your message with “tell me Pymon …”.
    3. Replying to her messages (inputs the last exchange into history).

## Installation

### Locally

1. Clone this repository to your local machine.
2. Install the required dependencies `pip install -r requirements.txt`.
3. Set up your environment variables by creating a `.env` file following the `.env.example` file and adding the necessary tokens and keys.
4. Run the main file `run.py` to start the bot.

### Docker container

1. Clone this repository to your local machine.
2. Set up your environment variables by creating a `.env` file following the `.env.example` file and adding the necessary tokens and keys.
3. Build the image using the `Dockerfile` with the following command:

```bash
docker build -t pymon .
```

1. Build and run the container using the `compose.yaml` file to deploy and start the bot in a container with the following command:

```bash
docker compose up
```

## Contributing

Contributions to Pymon are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to submit an issue or a pull request.

## **License**

This project is licensed under the MIT License - see the `LICENSE` file for details.
