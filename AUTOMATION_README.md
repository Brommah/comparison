# CEF Competitive Analysis Automation System

## Overview

This automation system continuously scrapes competitor websites and generates AI-powered updates for your competitive analysis matrix. With the press of a button, you can generate comprehensive AI insights and keep your competitive intelligence up-to-date.

## Features

### 🤖 Automated Scraping
- **Continuous Monitoring**: Scrapes competitor websites on scheduled intervals
- **Smart Scheduling**: Configurable scrape intervals (6h, 12h, daily, weekly)
- **Rate Limiting**: Built-in delays to avoid overwhelming target sites
- **Error Handling**: Automatic retries and graceful failure handling

### 🧠 AI-Powered Updates
- **One-Click Generation**: Generate AI insights with a single button press
- **Competitive Analysis**: AI analyzes scraped content for strategic insights
- **Key Findings**: Automatically identifies trends, gaps, and opportunities
- **Recommendations**: Provides actionable competitive intelligence

### 📊 Web Interface
- **Dashboard**: Real-time system status and monitoring
- **Company Management**: Add/remove competitors easily
- **Quick Actions**: One-click scraping and AI generation
- **Live Logs**: Real-time system activity monitoring

### 🔄 Integration
- **Matrix Updates**: Automatically updates your competitive analysis matrix
- **Data Export**: Export scraped data and AI insights to Excel
- **Notifications**: Slack/Discord webhook support for alerts

## Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Start the System
```bash
./start_automation.sh
```

### 3. Access Web Interface
Open your browser and navigate to: `http://localhost:5000`

## Usage

### Adding New Competitors
1. Open the web interface
2. Go to "Company Management" section
3. Enter company name and website URL
4. Set scrape interval (default: daily)
5. Click "Add Company"

### Manual Scraping
1. Click "🔄 Scrape All Now" button
2. System will scrape all enabled companies
3. Progress is shown in real-time logs
4. Completion notification will appear

### Generating AI Updates
1. Click "🤖 Generate AI Updates" button
2. AI will analyze latest scraped data
3. Insights are generated and saved
4. Matrix is automatically updated

### Scheduled Automation
The system runs automatically in the background:
- **Daily Scraping**: All companies scraped every 24 hours
- **AI Updates**: Generated every morning at 9:00 AM
- **Weekly Full Scrape**: Comprehensive scraping every Sunday

## Configuration

### Company Settings
Edit `automation_config.json` to modify:
- Company URLs and names
- Scrape intervals
- Enable/disable companies

### AI Settings
Configure AI analysis parameters:
- Model selection (GPT-4, GPT-3.5, etc.)
- Token limits
- Temperature settings

### Notifications
Set up webhooks for:
- Slack notifications
- Discord alerts
- Email notifications

## API Endpoints

### Companies
- `GET /api/companies` - List all monitored companies
- `POST /api/companies` - Add new company
- `DELETE /api/companies/<name>` - Remove company

### Actions
- `POST /api/scrape` - Run manual scraping
- `POST /api/ai-updates` - Generate AI updates
- `POST /api/update-matrix` - Update competitive matrix

### Data
- `GET /api/export` - Export data as Excel
- `GET /api/status` - Get system status
- `GET /api/logs` - Get system logs

## File Structure

```
├── automation_system.py          # Core automation logic
├── automation_server.py          # Flask web server
├── automation_web_interface.html # Web dashboard
├── automation_config.json        # Configuration file
├── requirements.txt              # Python dependencies
├── start_automation.sh           # Startup script
├── scraped_data/                 # Scraped data storage
├── logs/                         # System logs
└── AUTOMATION_README.md          # This file
```

## Troubleshooting

### Common Issues

**System won't start:**
- Check Python 3 installation
- Verify all dependencies are installed
- Check port 5000 is available

**Scraping fails:**
- Verify website URLs are accessible
- Check rate limiting settings
- Review error logs

**AI updates not generating:**
- Ensure scraped data exists
- Check AI API configuration
- Verify model access

### Logs
- System logs: `automation.log`
- Web interface logs: Browser console
- Server logs: Terminal output

## Security Considerations

- **API Keys**: Store securely in environment variables
- **Webhooks**: Use HTTPS for webhook URLs
- **Data Storage**: Encrypt sensitive scraped data
- **Access Control**: Implement authentication for production use

## Scaling

### Production Deployment
- Use production WSGI server (Gunicorn)
- Set up reverse proxy (Nginx)
- Implement database for data storage
- Add monitoring and alerting

### Cloud Deployment
- Deploy to AWS/GCP/Azure
- Use managed databases
- Implement auto-scaling
- Set up monitoring dashboards

## Support

For issues or questions:
1. Check the logs for error messages
2. Review configuration settings
3. Test with a single company first
4. Contact the development team

## License

This automation system is proprietary to CEF and contains confidential competitive intelligence data.
