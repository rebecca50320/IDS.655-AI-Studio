from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import requests
import time
import json

class SimpleRedditScrapeRequest(BaseModel):
    """Input schema for Simple Reddit Scrape Tool."""
    source: str = Field(
        description="The subreddit name (without r/) or a specific Reddit URL to scrape"
    )
    sort_type: Optional[str] = Field(
        default="hot",
        description="Sorting method: hot, new, top, rising (default: hot)"
    )
    limit: Optional[int] = Field(
        default=10,
        description="Number of posts to retrieve (default: 10, max: 25)"
    )

class SimpleRedditScrapeTool(BaseTool):
    """Tool for scraping Reddit posts from subreddits using basic HTTP requests."""

    name: str = "simple_reddit_scrape_tool"
    description: str = (
        "Scrapes Reddit posts from subreddits using the Reddit JSON API. "
        "Supports different sorting methods (hot, new, top, rising) and returns "
        "formatted post information including titles, scores, authors, and content."
    )
    args_schema: Type[BaseModel] = SimpleRedditScrapeRequest

    def _run(self, source: str, sort_type: str = "hot", limit: int = 10) -> str:
        try:
            # Validate and sanitize inputs
            limit = min(max(1, limit), 25)  # Ensure limit is between 1 and 25
            sort_type = sort_type.lower() if sort_type else "hot"
            
            if sort_type not in ["hot", "new", "top", "rising"]:
                sort_type = "hot"
            
            # Clean source input (remove r/ if present)
            source = source.strip()
            if source.startswith("r/"):
                source = source[2:]
            elif source.startswith("/r/"):
                source = source[3:]
            
            # Construct Reddit JSON API URL
            url = f"https://www.reddit.com/r/{source}/{sort_type}.json"
            
            # Set headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Add limit parameter
            params = {'limit': limit}
            
            # Make the request with basic timeout
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            # Check HTTP status
            if response.status_code == 404:
                return f"Error: Subreddit 'r/{source}' not found or doesn't exist."
            elif response.status_code == 403:
                return f"Error: Access denied to subreddit 'r/{source}'. It may be private or banned."
            elif response.status_code != 200:
                return f"Error: HTTP {response.status_code} - Unable to fetch data from Reddit."
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                return "Error: Invalid JSON response from Reddit API."
            
            # Extract posts from response
            if 'data' not in data or 'children' not in data['data']:
                return "Error: Unexpected response format from Reddit API."
            
            posts = data['data']['children']
            
            if not posts:
                return f"No posts found in r/{source} with sorting '{sort_type}'."
            
            # Format the results
            result_lines = [
                f"Reddit Posts from r/{source} (sorted by {sort_type})",
                "=" * 50,
                ""
            ]
            
            for i, post in enumerate(posts[:limit], 1):
                post_data = post['data']
                
                # Extract post information safely
                title = post_data.get('title', 'No title')
                score = post_data.get('score', 0)
                num_comments = post_data.get('num_comments', 0)
                author = post_data.get('author', 'Unknown')
                subreddit = post_data.get('subreddit', source)
                
                # Get post content (selftext for text posts, url for link posts)
                selftext = post_data.get('selftext', '').strip()
                post_url = post_data.get('url', '')
                permalink = f"https://www.reddit.com{post_data.get('permalink', '')}"
                
                # Create content preview
                if selftext:
                    content_preview = selftext[:200] + "..." if len(selftext) > 200 else selftext
                    content_type = "Text Post"
                elif post_url and post_url != permalink:
                    content_preview = f"Link: {post_url}"
                    content_type = "Link Post"
                else:
                    content_preview = "No content preview available"
                    content_type = "Post"
                
                # Format post information
                post_info = [
                    f"Post #{i}:",
                    f"Title: {title}",
                    f"Author: u/{author}",
                    f"Subreddit: r/{subreddit}",
                    f"Score: {score} points",
                    f"Comments: {num_comments}",
                    f"Type: {content_type}",
                    f"Content: {content_preview}",
                    f"Reddit Link: {permalink}",
                    "-" * 40
                ]
                
                result_lines.extend(post_info)
                result_lines.append("")
                
                # Basic rate limiting - small delay between processing posts
                if i < len(posts):
                    time.sleep(0.1)
            
            result_lines.append(f"Successfully scraped {len(posts[:limit])} posts from r/{source}")
            
            return "\n".join(result_lines)
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Reddit may be slow or unavailable."
        except requests.exceptions.ConnectionError:
            return "Error: Unable to connect to Reddit. Check your internet connection."
        except requests.exceptions.RequestException as e:
            return f"Error: Network request failed - {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"