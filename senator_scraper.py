import asyncio
import json
import os
from typing import Dict, List
from firecrawl import FirecrawlApp  # Corrected import

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class SenatorScraper:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Firecrawl API key not found in environment variables.  Please set the FIRECRAWL_API_KEY environment variable or define it in a .env file.")

        self.crawler = FirecrawlApp(  # Corrected class name
            api_key=api_key,
            # max_concurrent_requests=5, #These are not valid parameters for FireCrawlApp
            # request_delay=1.0,  # Be respectful with rate limiting
            # user_agent='CongressWebsite/1.0 (Research Project)' #invalid parameter
        )
        self.data_dir = Path('congress-website/src/data')
        self.data_dir.mkdir(exist_ok=True)

    async def scrape_senator_platform(self, name: str, website_url: str) -> Dict:
        """Scrape a senator's website for platform data."""
        platform_data = {
            'name': name,
            'website': website_url,
            'platform': []
        }

        try:
            # Scrape main page
            crawl_status = self.crawler.crawl_url(
                website_url,
                params={'limit': 100, 'scrapeOptions': {'formats': ['markdown', 'html']}},
                poll_interval=30
            )
            
            # Extract platform information
            if crawl_status and crawl_status.result and crawl_status.result.data:
                # Access the scraped data from the CrawlResult object
                scraped_data = crawl_status.result.data
                platform_data['platform'] = [scraped_data]  # Save the scraped data to the platform list
            else:
                platform_data['platform'] = ["No data found"]

        except Exception as e:
            print(f"Error scraping {name}'s website: {e}")
            platform_data['platform'] = ["Error occurred during scraping"]

        return platform_data

    async def save_data(self, senator_data: Dict):
        """Save scraped data to JSON file."""
        file_path = self.data_dir / f"{senator_data['name'].lower().replace(' ', '_')}.json"
        with open(file_path, 'w') as f:
            json.dump(senator_data, f, indent=2)

async def main():
    scraper = SenatorScraper()
    # Load senators from the JSON file
    with open('congress-website/src/data/senators_list.json', 'r') as f:
        senators_data = json.load(f)
    
    # Process each senator
    for senator in senators_data['senators']:
        data = await scraper.scrape_senator_platform(senator['name'], senator['website'])
        await scraper.save_data(data)

if __name__ == '__main__':
    asyncio.run(main())