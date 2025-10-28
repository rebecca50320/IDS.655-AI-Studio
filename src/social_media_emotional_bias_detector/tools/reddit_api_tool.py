from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import requests
import json
import time
import re
from urllib.parse import urlparse
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class RedditAPIRequest(BaseModel):
    """Input schema for Reddit API Tool."""
    source: str = Field(..., description="Subreddit name (e.g., 'politics'), username (e.g., 'username'), or direct post URL")
    source_type: str = Field(default="subreddit", description="Type of source: 'subreddit', 'user', or 'url'")
    min_words: int = Field(default=50, description="Minimum word count for posts (default: 50)")
    min_score: int = Field(default=10, description="Minimum upvotes/score for posts (default: 10)")
    sort_type: str = Field(default="hot", description="Sort type: 'hot', 'new', 'top', or 'rising' (default: 'hot')")
    limit: int = Field(default=1, description="Number of posts to fetch (default: 1)")

class RedditAPITool(BaseTool):
    """Enhanced Reddit API tool with robust error handling, fallback strategies, and improved reliability."""

    name: str = "reddit_api_tool"
    description: str = (
        "Enhanced Reddit API tool that reliably fetches Reddit posts using Reddit's public JSON API. "
        "Features robust error handling, retry logic, fallback domains, and comprehensive content validation. "
        "Supports subreddit posts, user submissions, and direct post URLs with advanced filtering options. "
        "Automatically handles rate limiting, SSL errors, and blocked endpoints with graceful degradation."
    )
    args_schema: Type[BaseModel] = RedditAPIRequest

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Request session with retry strategy
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy and robust settings."""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=2
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Standard headers - using user agent string directly
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        return session

    def _run(self, source: str, source_type: str = "subreddit", min_words: int = 50, 
             min_score: int = 10, sort_type: str = "hot", limit: int = 1) -> str:
        """
        Fetch Reddit posts with enhanced error handling and fallback strategies.
        
        Returns:
            JSON string containing post data or comprehensive error information
        """
        try:
            # Build API URLs for all domains
            api_urls = self._build_api_urls(source, source_type, sort_type)
            if not api_urls:
                return self._format_error(
                    f"Invalid source type '{source_type}' or unable to parse URL",
                    "INVALID_SOURCE",
                    "Please check your source format and try again. For subreddits, use the name without 'r/'. For users, use the username without 'u/'. For URLs, ensure they are valid Reddit post URLs."
                )

            # Try each URL with fallback strategies
            last_error = None
            for domain_url in api_urls:
                try:
                    result = self._fetch_with_fallbacks(domain_url)
                    if result:
                        # Process and filter posts
                        posts = self._extract_posts(result)
                        if posts:
                            filtered_posts = self._filter_posts(posts, min_words, min_score, limit)
                            if filtered_posts:
                                return json.dumps({
                                    "success": True,
                                    "posts": filtered_posts,
                                    "total_found": len(filtered_posts),
                                    "source": source,
                                    "source_type": source_type,
                                    "url_used": domain_url
                                })
                except Exception as e:
                    last_error = e
                    continue
                
                # Add delay between domain attempts
                time.sleep(1)

            # If we get here, all attempts failed
            return self._handle_fetch_failure(source, source_type, last_error)

        except Exception as e:
            return self._format_error(
                f"Unexpected error: {str(e)}",
                "UNEXPECTED_ERROR",
                "An unexpected error occurred. Please try again or contact support if the issue persists."
            )

    def _build_api_urls(self, source: str, source_type: str, sort_type: str) -> List[str]:
        """Build multiple API URLs with different domains for fallback."""
        urls = []
        # Use domains list locally instead of self.domains
        domains = ["www.reddit.com", "old.reddit.com"]
        
        for domain in domains:
            base_url = f"https://{domain}"
            
            if source_type == "subreddit":
                # Clean subreddit name
                subreddit = source.replace("r/", "").strip("/")
                if sort_type in ["hot", "new", "top", "rising"]:
                    urls.append(f"{base_url}/r/{subreddit}/{sort_type}.json")
                else:
                    urls.append(f"{base_url}/r/{subreddit}/hot.json")
                    
            elif source_type == "user":
                # Clean username
                username = source.replace("u/", "").strip("/")
                urls.append(f"{base_url}/user/{username}/submitted.json")
                
            elif source_type == "url":
                # Parse Reddit URL
                try:
                    parsed = urlparse(source)
                    if "reddit.com" in parsed.netloc:
                        path = parsed.path.rstrip("/")
                        urls.append(f"{base_url}{path}.json")
                except Exception:
                    continue
                    
        return urls

    def _fetch_with_fallbacks(self, api_url: str) -> Optional[Dict]:
        """Fetch data with multiple fallback strategies."""
        fallback_urls = [
            api_url,  # Original URL
            f"{api_url}?limit=25",  # With limit parameter
            f"{api_url}?sort=hot&limit=25",  # With additional parameters
        ]
        
        for url in fallback_urls:
            try:
                # Add delay to avoid rate limiting
                time.sleep(1.5)
                
                # Make request with extended timeout
                response = self.session.get(url, timeout=45, verify=True)
                
                # Handle specific HTTP errors
                if response.status_code == 200:
                    data = response.json()
                    if self._validate_response(data):
                        return data
                elif response.status_code == 403:
                    # Try with different headers - using user agent string directly
                    alt_headers = {'User-Agent': 'Mozilla/5.0 (compatible; RedditAnalyzer/1.0)'}
                    response = self.session.get(url, headers=alt_headers, timeout=45)
                    if response.status_code == 200:
                        return response.json()
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    time.sleep(5)
                    continue
                    
            except ssl.SSLError:
                # Try with SSL verification disabled
                try:
                    response = self.session.get(url, timeout=45, verify=False)
                    if response.status_code == 200:
                        return response.json()
                except Exception:
                    continue
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                continue
            except json.JSONDecodeError:
                # Try to extract JSON from HTML response
                try:
                    if response and response.text:
                        # Look for JSON data in HTML
                        json_match = re.search(r'window\\.__r = ({.*?});', response.text)
                        if json_match:
                            return json.loads(json_match.group(1))
                except Exception:
                    continue
            except Exception:
                continue
                
        return None

    def _validate_response(self, data: Any) -> bool:
        """Validate that the response contains usable post data."""
        try:
            if isinstance(data, dict):
                if "data" in data and "children" in data["data"]:
                    return len(data["data"]["children"]) > 0
                elif isinstance(data, list) and len(data) > 0:
                    return True
            return False
        except Exception:
            return False

    def _extract_posts(self, data: Dict[Any, Any]) -> List[Dict]:
        """Extract post data from Reddit API response with enhanced parsing."""
        posts = []
        
        try:
            # Handle different response formats
            if isinstance(data, dict):
                if "data" in data and "children" in data["data"]:
                    # Standard subreddit/user listing format
                    for child in data["data"]["children"]:
                        if child.get("kind") == "t3":  # t3 = link/post
                            posts.append(child["data"])
                elif "data" in data and isinstance(data["data"], dict):
                    # Single post format
                    posts.append(data["data"])
            elif isinstance(data, list) and len(data) > 0:
                # Array response format
                for item in data:
                    if "data" in item and "children" in item["data"]:
                        for child in item["data"]["children"]:
                            if child.get("kind") == "t3":
                                posts.append(child["data"])
        except (KeyError, TypeError, IndexError) as e:
            # Log parsing error but continue
            pass
            
        return posts

    def _filter_posts(self, posts: List[Dict], min_words: int, min_score: int, limit: int) -> List[Dict]:
        """Enhanced post filtering with better content extraction."""
        filtered_posts = []
        
        for post in posts:
            try:
                # Skip deleted/removed posts
                if (post.get("removed_by_category") or 
                    post.get("author") in ["[deleted]", "[removed]"] or
                    post.get("selftext") in ["[deleted]", "[removed]"]):
                    continue
                    
                # Enhanced content extraction
                title = post.get("title", "").strip()
                selftext = post.get("selftext", "").strip()
                
                # Try to extract content from link posts
                if not selftext and not post.get("is_self", False):
                    # For link posts, include URL domain info
                    url = post.get("url", "")
                    if url:
                        domain = self._extract_domain(url)
                        selftext = f"Link to: {domain}"
                
                # Combine title and content
                full_text = f"{title} {selftext}".strip()
                
                # Enhanced word counting (exclude common HTML entities and markdown)
                clean_text = re.sub(r'&[a-zA-Z]+;', ' ', full_text)  # Remove HTML entities
                clean_text = re.sub(r'[*_`#\\[\\]()]', ' ', clean_text)  # Remove markdown
                word_count = len([word for word in clean_text.split() if len(word) > 2])
                
                # Apply filters with validation
                score = max(0, post.get("score", 0))  # Ensure non-negative score
                if word_count < min_words or score < min_score:
                    continue
                
                # Build comprehensive post data
                post_data = {
                    "title": title,
                    "selftext": selftext,
                    "full_content": full_text,
                    "author": post.get("author", ""),
                    "subreddit": post.get("subreddit", ""),
                    "score": score,
                    "upvote_ratio": post.get("upvote_ratio", 0.0),
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", 0),
                    "permalink": f"https://www.reddit.com{post.get('permalink', '')}",
                    "word_count": word_count,
                    "post_type": self._determine_post_type(post),
                    "url": post.get("url", ""),
                    "domain": self._extract_domain(post.get("url", "")),
                    "is_self": post.get("is_self", False),
                    "flair": post.get("link_flair_text", ""),
                    "nsfw": post.get("over_18", False),
                    "spoiler": post.get("spoiler", False),
                    "stickied": post.get("stickied", False)
                }
                
                # Additional content validation
                if self._validate_post_content(post_data):
                    filtered_posts.append(post_data)
                    
                    # Respect limit
                    if len(filtered_posts) >= limit:
                        break
                        
            except (KeyError, TypeError, AttributeError):
                continue
        
        return filtered_posts

    def _determine_post_type(self, post: Dict[Any, Any]) -> str:
        """Enhanced post type determination."""
        if post.get("is_self", False):
            return "text"
        elif post.get("post_hint") == "image":
            return "image"
        elif post.get("post_hint") == "rich:video":
            return "video"
        elif post.get("is_video", False):
            return "video"
        elif post.get("post_hint") == "link":
            return "link"
        elif post.get("url", "").startswith("https://www.reddit.com"):
            return "crosspost"
        else:
            return "other"

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            if url and url.startswith("http"):
                parsed = urlparse(url)
                return parsed.netloc
        except Exception:
            pass
        return ""

    def _validate_post_content(self, post_data: Dict) -> bool:
        """Validate that post has meaningful content for analysis."""
        # Must have title
        if not post_data.get("title", "").strip():
            return False
            
        # Check for minimum meaningful content
        full_content = post_data.get("full_content", "").strip()
        if len(full_content) < 10:  # Very short posts probably not useful
            return False
            
        # Check for common spam patterns
        spam_indicators = ["[removed]", "[deleted]", "this post was removed", "comment deleted"]
        if any(indicator in full_content.lower() for indicator in spam_indicators):
            return False
            
        return True

    def _handle_fetch_failure(self, source: str, source_type: str, last_error: Exception) -> str:
        """Handle complete fetch failure with comprehensive error reporting."""
        if isinstance(last_error, requests.exceptions.Timeout):
            return self._format_error(
                "All requests timed out after multiple attempts",
                "TIMEOUT_ERROR",
                "Reddit's servers are responding slowly. Try again in a few minutes, or consider using manual copy/paste as a backup method."
            )
        elif isinstance(last_error, requests.exceptions.ConnectionError):
            return self._format_error(
                "Unable to connect to Reddit servers",
                "CONNECTION_ERROR", 
                "Network connection issue. Check your internet connection or try again later."
            )
        elif "403" in str(last_error) or "Forbidden" in str(last_error):
            return self._format_error(
                f"Access to '{source}' is forbidden",
                "ACCESS_FORBIDDEN",
                f"The {source_type} '{source}' may be private, banned, or restricted. Try a different {source_type} or use manual copy/paste method."
            )
        elif "404" in str(last_error) or "Not Found" in str(last_error):
            return self._format_error(
                f"'{source}' does not exist",
                "NOT_FOUND",
                f"The {source_type} '{source}' was not found. Check the spelling and try again."
            )
        elif "429" in str(last_error) or "rate limit" in str(last_error).lower():
            return self._format_error(
                "Rate limited by Reddit after multiple attempts",
                "RATE_LIMITED",
                "Reddit is blocking requests due to high traffic. Wait 10-15 minutes before trying again, or use manual copy/paste as an alternative."
            )
        else:
            # No valid posts found after all attempts
            return self._format_error(
                f"No posts found meeting criteria after trying all fallback methods",
                "NO_VALID_CONTENT",
                f"No posts in '{source}' meet your criteria (min_words: {50}, min_score: {10}). Try lowering the thresholds or choosing a different {source_type}."
            )

    def _format_error(self, error_msg: str, error_code: str, user_guidance: str) -> str:
        """Format comprehensive error response."""
        return json.dumps({
            "success": False,
            "error": error_msg,
            "error_code": error_code,
            "user_guidance": user_guidance,
            "fallback_suggestion": "As a backup, you can manually copy/paste Reddit content and provide it directly for analysis.",
            "timestamp": time.time()
        })