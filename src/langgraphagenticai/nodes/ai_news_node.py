from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNode with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency.
        
        Args:
            state (dict): The state dictionary containing 'frequency'.
        
        Returns:
            dict: Updated state with 'news_data' key containing fetched news.
        """

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
            # include_domains=["techcrunch.com", "venturebeat.com/ai", ...]  # Uncomment and add domains if needed
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    

    def summarize_news(self, state: dict) -> dict:
                news_items = self.state['news_data']

                if not news_items:
                    state['summary'] = "No AI news articles found for the selected time period."
                    self.state['summary'] = state['summary']
                    return self.state

                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", """You are an expert tech journalist writing a **weekly AI news summary** in markdown format.

            Instructions:
            - Group news articles by their published date in **descending order** (latest first).
            - For each date, add a markdown header: `### YYYY-MM-DD`
            - Under each header, list articles as: `- [Short Title or Summary](URL)`
            - Limit summaries to 1 line.
            - Format output using valid markdown.
            - Always include the URL in a clickable [title](url) format.
            """),
                    ("user", "Articles:\n{articles}")
                ])

                articles_str = "\n\n".join([
                    f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
                    for item in news_items
                ])

                response = self.llm.invoke(
                    prompt_template.format_prompt(articles=articles_str).to_messages()
                )
                
                state['summary'] = response.content
                self.state['summary'] = state['summary']
                return self.state

    
    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state
    