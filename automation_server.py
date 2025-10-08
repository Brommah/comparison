#!/usr/bin/env python3
"""
Flask server for CEF Competitive Analysis Automation
Provides web interface and API endpoints
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import subprocess
import threading
import time
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Global automation instance
automation = None

def init_automation():
    """Initialize automation system"""
    global automation
    try:
        from automation_system import CompetitiveAnalysisAutomation
        automation = CompetitiveAnalysisAutomation()
        return True
    except Exception as e:
        print(f"Error initializing automation: {e}")
        return False

@app.route('/')
def index():
    """Serve the main automation interface"""
    with open('automation_web_interface.html', 'r') as f:
        return f.read()

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get list of monitored companies"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    return jsonify(automation.config["companies"])

@app.route('/api/companies', methods=['POST'])
def add_company():
    """Add a new company to monitor"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    data = request.get_json()
    name = data.get('name')
    url = data.get('url')
    scrape_interval_hours = data.get('scrape_interval_hours', 24)
    
    if not name or not url:
        return jsonify({"error": "Name and URL required"}), 400
    
    success = automation.add_company(name, url, scrape_interval_hours)
    if success:
        return jsonify({"message": "Company added successfully"}), 201
    else:
        return jsonify({"error": "Company already exists"}), 409

@app.route('/api/companies/<name>', methods=['DELETE'])
def remove_company(name):
    """Remove a company from monitoring"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    automation.remove_company(name)
    return jsonify({"message": "Company removed successfully"}), 200

@app.route('/api/scrape', methods=['POST'])
def run_scrape():
    """Run manual scraping"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    # Run scraping in background thread
    def scrape_background():
        try:
            results = automation.run_manual_scrape()
            print(f"Scraping completed: {len(results)} companies scraped")
        except Exception as e:
            print(f"Scraping error: {e}")
    
    thread = threading.Thread(target=scrape_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Scraping started"}), 202

@app.route('/api/ai-updates', methods=['POST'])
def generate_ai_updates():
    """Generate AI updates"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    # Run AI generation in background thread
    def ai_background():
        try:
            updates = automation.run_manual_ai_update()
            print(f"AI updates generated: {len(updates)} insights")
        except Exception as e:
            print(f"AI generation error: {e}")
    
    thread = threading.Thread(target=ai_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "AI updates generation started"}), 202

@app.route('/api/update-matrix', methods=['POST'])
def update_matrix():
    """Update the competitive matrix HTML"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    try:
        # Load latest AI updates
        latest_updates = automation._load_latest_scraped_data()
        ai_updates = automation.generate_ai_updates()
        
        # Update matrix HTML
        success = automation.update_matrix_html(ai_updates)
        
        if success:
            return jsonify({"message": "Matrix updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update matrix"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export')
def export_data():
    """Export data as Excel file"""
    try:
        # Create Excel file with current data
        import pandas as pd
        
        # Load scraped data
        data_dir = Path("scraped_data")
        if not data_dir.exists():
            return jsonify({"error": "No data to export"}), 404
        
        # Collect all data
        all_data = []
        for file in data_dir.glob("*.json"):
            with open(file, 'r') as f:
                data = json.load(f)
                all_data.append({
                    'Company': data['company'],
                    'URL': data['url'],
                    'Timestamp': data['timestamp'],
                    'Status': data['status'],
                    'Content_Length': len(data['content']) if data['content'] else 0
                })
        
        # Create DataFrame and export
        df = pd.DataFrame(all_data)
        excel_file = f"competitive_analysis_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(excel_file, index=False)
        
        return send_file(excel_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def get_status():
    """Get system status"""
    if not automation:
        return jsonify({"error": "Automation not initialized"}), 500
    
    try:
        # Count companies
        companies_count = len(automation.config["companies"])
        
        # Get last scrape time
        data_dir = Path("scraped_data")
        last_scrape = "Never"
        if data_dir.exists():
            files = list(data_dir.glob("*.json"))
            if files:
                latest_file = max(files, key=lambda x: x.stat().st_mtime)
                last_scrape = datetime.fromtimestamp(latest_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        
        # Count AI updates
        ai_updates_count = len(list(data_dir.glob("ai_updates_*.json"))) if data_dir.exists() else 0
        
        return jsonify({
            "companies_count": companies_count,
            "last_scrape": last_scrape,
            "ai_updates_count": ai_updates_count,
            "system_health": "Healthy"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get system logs"""
    try:
        log_file = Path("automation.log")
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = f.readlines()
            return jsonify({"logs": logs[-50:]})  # Last 50 lines
        else:
            return jsonify({"logs": []})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Initializing CEF Competitive Analysis Automation Server...")
    
    if init_automation():
        print("✅ Automation system initialized successfully")
        print("🚀 Starting web server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize automation system")
        print("Please check your configuration and dependencies")
