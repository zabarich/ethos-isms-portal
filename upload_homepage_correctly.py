#!/usr/bin/env python3
"""
Upload the custom homepage to the correct location in SharePoint
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
TENANT_ID = os.getenv('SHP_TENANT_ID')
CLIENT_ID = os.getenv('SHP_ID_APP')
CLIENT_SECRET = os.getenv('SHP_ID_APP_SECRET')
SITE_URL = os.getenv('SHP_SITE_URL')

def upload_homepage():
    """Upload homepage to the Quick Reference folder where we have access"""

    print("🔐 Authenticating...")

    # Authenticate
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    access_token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}

    # Get site and drive IDs (we know these work)
    from urllib.parse import urlparse
    parsed = urlparse(SITE_URL)
    hostname = parsed.netloc
    site_path = parsed.path.lstrip('/')

    site_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{site_path}"
    response = requests.get(site_url, headers=headers)
    response.raise_for_status()
    site_id = response.json().get('id')

    drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    response = requests.get(drives_url, headers=headers)
    response.raise_for_status()

    drives = response.json().get('value', [])
    drive_id = None
    for drive in drives:
        if 'Document' in drive.get('name', ''):
            drive_id = drive.get('id')
            break

    if not drive_id and drives:
        drive_id = drives[0].get('id')

    print(f"✅ Connected to SharePoint")
    print(f"📁 Using drive: {drive_id}")

    # Create a simple but beautiful homepage HTML
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ETHOS ISMS Portal</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f3f2f1;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #0078D4 0%, #0063B1 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 40px;
            box-shadow: 0 5px 20px rgba(0,120,212,0.3);
        }
        .hero h1 {
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 15px;
        }
        .hero p {
            font-size: 1.2em;
            opacity: 0.95;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Quick Actions */
        .section-title {
            color: #0078D4;
            font-size: 1.8em;
            margin: 40px 0 25px;
            text-align: center;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,120,212,0.2);
        }
        .card-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .card h3 {
            color: #323130;
            margin-bottom: 8px;
            font-size: 1.2em;
        }
        .card p {
            color: #605E5C;
            font-size: 0.9em;
        }

        /* Document Categories */
        .doc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }
        .doc-tile {
            background: linear-gradient(135deg, #0078D4, #0063B1);
            color: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: block;
            transition: transform 0.2s;
        }
        .doc-tile:hover {
            transform: scale(1.05);
        }
        .doc-tile.procedures {
            background: linear-gradient(135deg, #50E6FF, #0078D4);
        }
        .doc-tile.training {
            background: linear-gradient(135deg, #107C10, #0B5C0B);
        }
        .doc-tile.forms {
            background: linear-gradient(135deg, #FFB900, #FF8C00);
        }
        .doc-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .doc-tile h4 {
            margin: 0;
            font-size: 1.1em;
        }
        .doc-tile p {
            margin: 5px 0 0;
            font-size: 0.85em;
            opacity: 0.9;
        }

        /* Announcements */
        .announcement {
            background: linear-gradient(135deg, rgba(80,230,255,0.1), rgba(0,120,212,0.1));
            border-left: 4px solid #0078D4;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .announcement h3 {
            color: #0078D4;
            margin-bottom: 15px;
        }
        .notice {
            background: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .notice h4 {
            color: #323130;
            margin-bottom: 8px;
        }
        .notice p {
            color: #605E5C;
            margin-bottom: 10px;
        }
        .notice a {
            color: #0078D4;
            font-weight: 600;
            text-decoration: none;
        }

        /* Footer */
        .footer {
            background: #323130;
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-top: 60px;
            border-radius: 10px;
        }
        .footer a {
            color: #50E6FF;
            text-decoration: none;
        }

        @media (max-width: 768px) {
            .hero h1 { font-size: 1.8em; }
            .cards { grid-template-columns: 1fr; }
            .doc-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1>🔒 Welcome to ETHOS ISMS Portal</h1>
            <p>Your comprehensive resource for information security policies, procedures, and compliance</p>
        </div>

        <!-- Quick Actions -->
        <h2 class="section-title">Quick Actions</h2>
        <div class="cards">
            <a href="mailto:security@ethos.co.im?subject=Security%20Incident%20Report" class="card">
                <div class="card-icon">🚨</div>
                <h3>Report Incident</h3>
                <p>Quickly report security incidents</p>
            </a>
            <a href="mailto:richard.wild@ethos.co.im?subject=Access%20Request" class="card">
                <div class="card-icon">🔐</div>
                <h3>Request Access</h3>
                <p>Submit system access requests</p>
            </a>
            <a href="03_Training/Staff_Training/ISMS_TRN_001_Security_Awareness_Training_Framework.html" class="card">
                <div class="card-icon">📚</div>
                <h3>Training Materials</h3>
                <p>Access security training resources</p>
            </a>
            <a href="05_Quick_Reference/Welcome_Guide.html" class="card">
                <div class="card-icon">❓</div>
                <h3>Help & Support</h3>
                <p>Get help and find answers</p>
            </a>
        </div>

        <!-- Announcements -->
        <div class="announcement">
            <h3>📢 Important Updates</h3>
            <div class="notice">
                <h4>🎓 Annual Security Training Due Q1 2025</h4>
                <p>All staff must complete the Security Awareness Training by end of Q1.</p>
                <a href="../Lists/Training%20Records">Check your training status →</a>
            </div>
            <div class="notice">
                <h4>🔄 Remote Working Policy Updated</h4>
                <p>New security requirements have been added to the Remote Working Policy.</p>
                <a href="01_Policies/Core_Policies/ISMS_POL_009_Remote_Working_Policy.html">Review the policy →</a>
            </div>
        </div>

        <!-- Document Library -->
        <h2 class="section-title">Document Library</h2>
        <div class="doc-grid">
            <a href="01_Policies" class="doc-tile">
                <div class="doc-icon">📄</div>
                <h4>Policies</h4>
                <p>12 documents</p>
            </a>
            <a href="02_Procedures" class="doc-tile procedures">
                <div class="doc-icon">📝</div>
                <h4>Procedures</h4>
                <p>8 documents</p>
            </a>
            <a href="03_Training" class="doc-tile training">
                <div class="doc-icon">🎓</div>
                <h4>Training</h4>
                <p>Materials & Guides</p>
            </a>
            <a href="04_Forms_Templates" class="doc-tile forms">
                <div class="doc-icon">📋</div>
                <h4>Forms</h4>
                <p>Templates</p>
            </a>
        </div>

        <!-- Key Documents -->
        <h2 class="section-title">Essential Reading</h2>
        <div class="cards">
            <a href="01_Policies/Core_Policies/ISMS_POL_001_Information_Security_Policy.html" class="card">
                <div class="card-icon">📖</div>
                <h3>Information Security Policy</h3>
                <p>Core security principles for all staff</p>
            </a>
            <a href="01_Policies/Core_Policies/ISMS_POL_008_Acceptable_Use_Policy.html" class="card">
                <div class="card-icon">💻</div>
                <h3>Acceptable Use Policy</h3>
                <p>Guidelines for IT resource usage</p>
            </a>
            <a href="02_Procedures/Emergency/ISMS_PRO_002_Incident_Response_Procedure.html" class="card">
                <div class="card-icon">🆘</div>
                <h3>Incident Response</h3>
                <p>What to do when incidents occur</p>
            </a>
        </div>

        <!-- Footer -->
        <div class="footer">
            <h3>Need Help?</h3>
            <p style="margin: 20px 0;">
                📧 Email: <a href="mailto:security@ethos.co.im">security@ethos.co.im</a> |
                💬 Teams: #security-help |
                📞 Emergency: Contact IT Support
            </p>
            <p style="opacity: 0.8; font-size: 0.9em;">
                © 2025 ETHOS Ltd. Information Security Management System
            </p>
        </div>
    </div>
</body>
</html>"""

    # Upload to the Shared Documents root (where we have permission)
    upload_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/ISMS_Portal_Home.html:/content"

    upload_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/html'
    }

    print("\n📤 Uploading custom homepage...")
    response = requests.put(upload_url, headers=upload_headers, data=html_content.encode('utf-8'))

    if response.status_code in [200, 201]:
        print("✅ Custom homepage uploaded successfully!")
        print(f"\n🌐 Access your beautiful portal at:")
        print(f"{SITE_URL}/Shared Documents/ISMS_Portal_Home.html")
        print(f"\n📝 To use this as your homepage:")
        print("1. Navigate to the file in SharePoint")
        print("2. Open it in the browser")
        print("3. Bookmark it for quick access")
        print("4. Share this link with staff")
        return True
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return False

if __name__ == '__main__':
    upload_homepage()