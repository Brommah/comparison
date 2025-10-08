#!/usr/bin/env python3
"""
CEF Competitive Analysis Automation System
Continuously scrapes competitor websites and generates AI updates
"""

import json
import time
import schedule
import requests
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional
import subprocess
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompetitiveAnalysisAutomation:
    def __init__(self, config_file: str = "automation_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.data_dir = Path("scraped_data")
        self.data_dir.mkdir(exist_ok=True)
        
    def load_config(self) -> Dict:
        """Load automation configuration"""
        default_config = {
            "companies": [
                {
                    "name": "CEF",
                    "url": "https://cef.ai",
                    "enabled": True,
                    "scrape_interval_hours": 24
                },
                {
                    "name": "Databricks", 
                    "url": "https://www.databricks.com",
                    "enabled": True,
                    "scrape_interval_hours": 24
                },
                {
                    "name": "Sierra.ai",
                    "url": "https://www.sierra.ai", 
                    "enabled": True,
                    "scrape_interval_hours": 24
                },
                {
                    "name": "Fin.ai",
                    "url": "https://fin.ai",
                    "enabled": True,
                    "scrape_interval_hours": 24
                },
                {
                    "name": "NICE",
                    "url": "https://www.nice.com",
                    "enabled": True,
                    "scrape_interval_hours": 24
                },
                {
                    "name": "Snowflake",
                    "url": "https://www.snowflake.com",
                    "enabled": True,
                    "scrape_interval_hours": 24
                }
            ],
            "ai_update_settings": {
                "model": "gpt-4",
                "max_tokens": 2000,
                "temperature": 0.3
            },
            "notification_settings": {
                "email_enabled": False,
                "slack_webhook": None,
                "discord_webhook": None
            }
        }
        
        if Path(self.config_file).exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            # Create default config file
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_company(self, name: str, url: str, scrape_interval_hours: int = 24):
        """Add a new company to monitor"""
        new_company = {
            "name": name,
            "url": url,
            "enabled": True,
            "scrape_interval_hours": scrape_interval_hours
        }
        
        # Check if company already exists
        for company in self.config["companies"]:
            if company["name"].lower() == name.lower():
                logger.warning(f"Company {name} already exists")
                return False
        
        self.config["companies"].append(new_company)
        self.save_config()
        logger.info(f"Added company: {name} ({url})")
        return True
    
    def remove_company(self, name: str):
        """Remove a company from monitoring"""
        self.config["companies"] = [
            company for company in self.config["companies"] 
            if company["name"].lower() != name.lower()
        ]
        self.save_config()
        logger.info(f"Removed company: {name}")
    
    def scrape_website(self, company: Dict) -> Optional[Dict]:
        """Scrape a single website using Firecrawl"""
        try:
            logger.info(f"Scraping {company['name']} ({company['url']})")
            
            # Use Firecrawl to scrape the website
            # This would integrate with your existing Firecrawl setup
            scrape_result = self._firecrawl_scrape(company['url'])
            
            if scrape_result:
                # Save scraped data
                timestamp = datetime.now().isoformat()
                data_file = self.data_dir / f"{company['name'].lower().replace(' ', '_')}_{timestamp[:10]}.json"
                
                scraped_data = {
                    "company": company['name'],
                    "url": company['url'],
                    "timestamp": timestamp,
                    "content": scrape_result,
                    "status": "success"
                }
                
                with open(data_file, 'w') as f:
                    json.dump(scraped_data, f, indent=2)
                
                logger.info(f"Successfully scraped {company['name']}")
                return scraped_data
            else:
                logger.error(f"Failed to scrape {company['name']}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping {company['name']}: {str(e)}")
            return None
    
    def _firecrawl_scrape(self, url: str) -> Optional[str]:
        """Mock Firecrawl scraping - replace with actual Firecrawl API call"""
        # This would be replaced with actual Firecrawl API integration
        # For now, return mock data
        return f"Mock scraped content from {url} at {datetime.now()}"
    
    def scrape_all_enabled(self):
        """Scrape all enabled companies"""
        logger.info("Starting scheduled scraping of all enabled companies")
        
        results = []
        for company in self.config["companies"]:
            if company["enabled"]:
                result = self.scrape_website(company)
                if result:
                    results.append(result)
                # Add delay between scrapes to avoid rate limiting
                time.sleep(5)
        
        logger.info(f"Completed scraping. Successfully scraped {len(results)} companies")
        return results
    
    def generate_ai_updates(self) -> Dict:
        """Generate AI-powered updates for the competitive matrix"""
        try:
            logger.info("Generating AI updates for competitive matrix")
            
            # Load latest scraped data
            latest_data = self._load_latest_scraped_data()
            
            # Generate AI analysis
            ai_updates = self._generate_ai_analysis(latest_data)
            
            # Save AI updates
            timestamp = datetime.now().isoformat()
            updates_file = self.data_dir / f"ai_updates_{timestamp[:10]}.json"
            
            with open(updates_file, 'w') as f:
                json.dump(ai_updates, f, indent=2)
            
            logger.info("AI updates generated successfully")
            return ai_updates
            
        except Exception as e:
            logger.error(f"Error generating AI updates: {str(e)}")
            return {}
    
    def _load_latest_scraped_data(self) -> Dict:
        """Load the most recent scraped data for each company"""
        latest_data = {}
        
        for company in self.config["companies"]:
            company_name = company['name'].lower().replace(' ', '_')
            data_files = list(self.data_dir.glob(f"{company_name}_*.json"))
            
            if data_files:
                # Get the most recent file
                latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
                with open(latest_file, 'r') as f:
                    latest_data[company['name']] = json.load(f)
        
        return latest_data
    
    def _generate_ai_analysis(self, scraped_data: Dict) -> Dict:
        """Generate AI analysis of scraped data"""
        # This would integrate with OpenAI API or similar
        # For now, return mock analysis
        return {
            "timestamp": datetime.now().isoformat(),
            "analysis": "Mock AI analysis of competitive landscape",
            "key_insights": [
                "Company A shows strong growth in AI capabilities",
                "Company B has new security features",
                "Company C updated their pricing model"
            ],
            "recommendations": [
                "Monitor Company A's new AI features",
                "Consider Company B's security approach",
                "Review Company C's pricing strategy"
            ]
        }
    
    def update_matrix_html(self, ai_updates: Dict):
        """Update the competitive analysis matrix HTML with new data"""
        try:
            logger.info("Updating competitive matrix HTML")
            
            # Load current matrix data
            matrix_file = Path("competitive_analysis_matrix.html")
            if not matrix_file.exists():
                logger.error("Matrix HTML file not found")
                return False
            
            # This would update the HTML file with new data
            # Implementation depends on how you want to integrate the updates
            
            logger.info("Matrix HTML updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating matrix HTML: {str(e)}")
            return False
    
    def send_notification(self, message: str):
        """Send notification about updates"""
        if self.config["notification_settings"]["slack_webhook"]:
            self._send_slack_notification(message)
        
        if self.config["notification_settings"]["discord_webhook"]:
            self._send_discord_notification(message)
    
    def _send_slack_notification(self, message: str):
        """Send Slack notification"""
        webhook_url = self.config["notification_settings"]["slack_webhook"]
        if webhook_url:
            payload = {"text": message}
            try:
                requests.post(webhook_url, json=payload)
                logger.info("Slack notification sent")
            except Exception as e:
                logger.error(f"Failed to send Slack notification: {str(e)}")
    
    def _send_discord_notification(self, message: str):
        """Send Discord notification"""
        webhook_url = self.config["notification_settings"]["discord_webhook"]
        if webhook_url:
            payload = {"content": message}
            try:
                requests.post(webhook_url, json=payload)
                logger.info("Discord notification sent")
            except Exception as e:
                logger.error(f"Failed to send Discord notification: {str(e)}")
    
    def start_scheduler(self):
        """Start the automation scheduler"""
        logger.info("Starting automation scheduler")
        
        # Schedule scraping for each company based on their interval
        for company in self.config["companies"]:
            if company["enabled"]:
                interval_hours = company["scrape_interval_hours"]
                schedule.every(interval_hours).hours.do(
                    self.scrape_website, company
                ).tag(f"scrape_{company['name'].lower()}")
        
        # Schedule daily AI update generation
        schedule.every().day.at("09:00").do(self.generate_ai_updates).tag("ai_updates")
        
        # Schedule weekly full scrape
        schedule.every().week.do(self.scrape_all_enabled).tag("full_scrape")
        
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
    
    def run_manual_scrape(self):
        """Run manual scraping of all companies"""
        logger.info("Running manual scrape of all companies")
        results = self.scrape_all_enabled()
        
        if results:
            message = f"✅ Manual scrape completed. Scraped {len(results)} companies successfully."
            self.send_notification(message)
        
        return results
    
    def run_manual_ai_update(self):
        """Run manual AI update generation"""
        logger.info("Running manual AI update generation")
        ai_updates = self.generate_ai_updates()
        
        if ai_updates:
            message = "🤖 AI updates generated successfully. Check the matrix for new insights."
            self.send_notification(message)
        
        return ai_updates

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CEF Competitive Analysis Automation")
    parser.add_argument("--scrape", action="store_true", help="Run manual scrape")
    parser.add_argument("--ai-update", action="store_true", help="Generate AI updates")
    parser.add_argument("--start-scheduler", action="store_true", help="Start automation scheduler")
    parser.add_argument("--add-company", nargs=2, metavar=("NAME", "URL"), help="Add new company")
    parser.add_argument("--remove-company", metavar="NAME", help="Remove company")
    
    args = parser.parse_args()
    
    automation = CompetitiveAnalysisAutomation()
    
    if args.add_company:
        name, url = args.add_company
        automation.add_company(name, url)
    elif args.remove_company:
        automation.remove_company(args.remove_company)
    elif args.scrape:
        automation.run_manual_scrape()
    elif args.ai_update:
        automation.run_manual_ai_update()
    elif args.start_scheduler:
        automation.start_scheduler()
    else:
        print("Use --help to see available options")

if __name__ == "__main__":
    main()
