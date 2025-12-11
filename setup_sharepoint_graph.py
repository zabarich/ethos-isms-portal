#!/usr/bin/env python3
"""
ETHOS ISMS SharePoint Site Setup using Microsoft Graph API
Cross-platform setup script for SharePoint site configuration
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Configuration from .env
TENANT_ID = os.getenv('SHP_TENANT_ID')
CLIENT_ID = os.getenv('SHP_ID_APP')
CLIENT_SECRET = os.getenv('SHP_ID_APP_SECRET')
SITE_URL = os.getenv('SHP_SITE_URL')

# Validate configuration
if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, SITE_URL]):
    print("❌ Missing SharePoint configuration in .env file")
    sys.exit(1)


class SharePointSetup:
    """Setup SharePoint site structure using Microsoft Graph API"""

    def __init__(self):
        self.access_token = None
        self.site_id = None
        self.drive_id = None
        self.headers = {}

        # Tech Innovation theme colors
        self.theme_colors = {
            "primary": "#0078D4",
            "secondary": "#50E6FF",
            "accent": "#0063B1",
            "success": "#107C10",
            "warning": "#FFB900",
            "danger": "#E81123",
            "background": "#F3F2F1",
            "card": "#FFFFFF",
            "text_primary": "#323130",
            "text_secondary": "#605E5C",
            "border": "#D0CCCB"
        }

    def authenticate(self):
        """Get access token from Azure AD"""
        print("🔐 Authenticating with Azure AD...")

        url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': 'https://graph.microsoft.com/.default',
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.access_token = response.json().get('access_token')
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            print("✅ Authentication successful")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def get_site_info(self):
        """Get SharePoint site ID and drive ID"""
        print("\n📍 Getting site information...")

        # Parse site URL
        from urllib.parse import urlparse
        parsed = urlparse(SITE_URL)
        hostname = parsed.netloc
        site_path = parsed.path.lstrip('/')

        # Get site ID
        url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{site_path}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            site_info = response.json()
            self.site_id = site_info.get('id')
            print(f"✅ Site ID: {self.site_id}")

            # Get default document library (drive)
            drives_url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives"
            response = requests.get(drives_url, headers=self.headers)
            response.raise_for_status()

            drives = response.json().get('value', [])
            for drive in drives:
                if drive.get('name') == 'Shared Documents' or 'Documents' in drive.get('name', ''):
                    self.drive_id = drive.get('id')
                    print(f"✅ Drive ID: {self.drive_id}")
                    return True

            # Use first drive if specific one not found
            if drives:
                self.drive_id = drives[0].get('id')
                print(f"✅ Using default drive: {self.drive_id}")
                return True

        except Exception as e:
            print(f"❌ Failed to get site info: {e}")
            return False

    def create_folder_structure(self):
        """Create the document library folder structure"""
        print("\n📁 Creating folder structure...")

        folders = [
            "01_Policies",
            "01_Policies/Core_Policies",
            "01_Policies/Supporting_Policies",
            "02_Procedures",
            "02_Procedures/Operational",
            "02_Procedures/Emergency",
            "03_Training",
            "03_Training/Staff_Training",
            "03_Training/Contractor_Materials",
            "03_Training/Assessments",
            "04_Forms_Templates",
            "04_Forms_Templates/Access_Requests",
            "04_Forms_Templates/Incident_Reports",
            "04_Forms_Templates/Change_Requests",
            "05_Quick_Reference",
            "05_Quick_Reference/FAQ",
            "05_Quick_Reference/Contacts",
            "06_Archive",
            "06_Archive/Previous_Versions"
        ]

        created_count = 0
        for folder_path in folders:
            if self.create_folder(folder_path):
                created_count += 1
                print(f"  ✅ Created: {folder_path}")
            else:
                print(f"  ⚠️  Exists or skipped: {folder_path}")

        print(f"✅ Created {created_count} folders")
        return True

    def create_folder(self, folder_path: str):
        """Create a single folder in SharePoint"""
        url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root:/{folder_path}:/children"

        # For nested folders, ensure parent exists first
        if '/' in folder_path:
            parent_path = '/'.join(folder_path.split('/')[:-1])
            folder_name = folder_path.split('/')[-1]
            url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root:/{parent_path}:/children"
        else:
            folder_name = folder_path
            url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root/children"

        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "fail"
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 201:
                return True
            elif response.status_code == 409:  # Already exists
                return False
            else:
                return False
        except:
            return False

    def create_lists(self):
        """Create SharePoint lists for tracking"""
        print("\n📋 Creating SharePoint lists...")

        # Create Training Records list
        list_definition = {
            "displayName": "Training Records",
            "description": "Track staff security training completion and compliance",
            "list": {
                "template": "genericList"
            },
            "columns": [
                {
                    "name": "StaffMember",
                    "displayName": "Staff Member",
                    "text": {}
                },
                {
                    "name": "TrainingCourse",
                    "displayName": "Training Course",
                    "text": {}
                },
                {
                    "name": "CompletionDate",
                    "displayName": "Completion Date",
                    "dateTime": {}
                },
                {
                    "name": "NextReviewDate",
                    "displayName": "Next Review Date",
                    "dateTime": {}
                },
                {
                    "name": "Score",
                    "displayName": "Score (%)",
                    "number": {}
                },
                {
                    "name": "Status",
                    "displayName": "Status",
                    "choice": {
                        "choices": ["Not Started", "In Progress", "Completed", "Expired"]
                    }
                },
                {
                    "name": "Notes",
                    "displayName": "Notes",
                    "text": {
                        "allowMultipleLines": True
                    }
                }
            ]
        }

        try:
            # Create the list
            url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/lists"
            response = requests.post(url, headers=self.headers, json=list_definition)

            if response.status_code == 201:
                print("✅ Training Records list created")
                return True
            elif response.status_code == 409:
                print("⚠️  Training Records list already exists")
                return True
            else:
                print(f"❌ Failed to create list: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error creating list: {e}")
            return False

    def upload_welcome_document(self):
        """Upload a welcome document to the Quick Reference folder"""
        print("\n📄 Creating welcome document...")

        welcome_content = f"""
# ETHOS Information Security Management System
## Staff Portal User Guide

Welcome to the ETHOS ISMS Staff Portal. This portal provides access to all security policies, procedures, and training materials that staff need to maintain our information security standards.

---

## 📁 Portal Structure

### 1. Policies (Folder: 01_Policies)
Contains all information security policies including:
- Information Security Policy (ISMS-POL-001)
- Access Control Policy (ISMS-POL-002)
- Acceptable Use Policy (ISMS-POL-008)
- Remote Working Policy (ISMS-POL-009)
- And more...

### 2. Procedures (Folder: 02_Procedures)
Step-by-step guides for:
- Incident Response (ISMS-PRO-002)
- Change Management (ISMS-PRO-003)
- Access Requests (ISMS-PRO-001)
- Business Continuity (ISMS-PRO-004)

### 3. Training (Folder: 03_Training)
- Security awareness materials
- Training assessments
- Contractor briefings

### 4. Forms & Templates (Folder: 04_Forms_Templates)
- Access request forms
- Incident report templates
- Change request forms

### 5. Quick Reference (Folder: 05_Quick_Reference)
- This guide
- FAQ documents
- Contact information

---

## 🎯 Quick Actions

**Report a Security Incident**
Email: security@ethos.co.im
Phone: [Emergency Contact Number]

**Request System Access**
Use the Access Request Form in Forms & Templates

**Complete Training**
Check the Training folder for required materials

---

## 📊 Training Records

Your training completion is tracked in the Training Records list. You can:
- View your completion status
- See upcoming training due dates
- Download certificates

---

## 🔒 Security Reminders

1. **Protect sensitive information** - Follow the Information Security Policy
2. **Report incidents immediately** - Use the Incident Report Form
3. **Keep passwords secure** - Never share credentials
4. **Complete training on time** - Check your Training Records regularly
5. **Follow procedures** - Use the documented procedures for all security tasks

---

## ❓ Need Help?

- **Security Team**: security@ethos.co.im
- **IT Support**: support@mtg.im
- **CISO**: richard.wild@ethos.co.im

---

*Last Updated: {datetime.now().strftime('%B %d, %Y')}*
*Version: 1.0*
*Classification: Internal Use*
        """

        # Convert to HTML for better SharePoint rendering
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ISMS Portal Welcome Guide</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; color: {self.theme_colors['text_primary']}; }}
        h1 {{ color: {self.theme_colors['primary']}; }}
        h2 {{ color: {self.theme_colors['accent']}; }}
        h3 {{ color: {self.theme_colors['text_primary']}; }}
        .highlight {{ background: linear-gradient(135deg, rgba(0,120,212,0.1), rgba(80,230,255,0.1)); padding: 15px; border-left: 4px solid {self.theme_colors['primary']}; margin: 20px 0; }}
        .footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid {self.theme_colors['border']}; color: {self.theme_colors['text_secondary']}; }}
    </style>
</head>
<body>
    {welcome_content.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('---', '<hr>')}
</body>
</html>
        """

        try:
            # Upload to Quick Reference folder
            url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root:/05_Quick_Reference/Welcome_Guide.html:/content"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'text/html'
            }

            response = requests.put(url, headers=headers, data=html_content.encode('utf-8'))

            if response.status_code in [200, 201]:
                print("✅ Welcome guide uploaded")
                return True
            else:
                print(f"⚠️  Welcome guide upload issue: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error uploading welcome guide: {e}")
            return False

    def create_sample_training_record(self):
        """Create a sample training record for demonstration"""
        print("\n📊 Creating sample training record...")

        # First, get the Training Records list ID
        try:
            url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/lists"
            response = requests.get(url, headers=self.headers)
            lists = response.json().get('value', [])

            training_list_id = None
            for lst in lists:
                if lst.get('displayName') == 'Training Records':
                    training_list_id = lst.get('id')
                    break

            if not training_list_id:
                print("⚠️  Training Records list not found")
                return False

            # Create sample record
            sample_record = {
                "fields": {
                    "Title": "Sample: Security Awareness Training 2025",
                    "StaffMember": "All Staff",
                    "TrainingCourse": "Annual Security Awareness",
                    "CompletionDate": datetime.now().isoformat(),
                    "NextReviewDate": "2026-01-01T00:00:00Z",
                    "Score": 85,
                    "Status": "Completed",
                    "Notes": "This is a sample record. Staff should create their own entries."
                }
            }

            url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/lists/{training_list_id}/items"
            response = requests.post(url, headers=self.headers, json=sample_record)

            if response.status_code == 201:
                print("✅ Sample training record created")
                return True
            else:
                print(f"⚠️  Could not create sample record: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error creating sample record: {e}")
            return False

    def setup_site(self):
        """Main setup orchestration"""
        print("\n" + "="*50)
        print("   ETHOS ISMS SHAREPOINT SITE SETUP")
        print("="*50)
        print(f"Site: {SITE_URL}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")

        # Step 1: Authenticate
        if not self.authenticate():
            return False

        # Step 2: Get site information
        if not self.get_site_info():
            return False

        # Step 3: Create folder structure
        self.create_folder_structure()

        # Step 4: Create lists
        self.create_lists()

        # Step 5: Upload welcome document
        self.upload_welcome_document()

        # Step 6: Create sample training record
        self.create_sample_training_record()

        print("\n" + "="*50)
        print("✅ SHAREPOINT SETUP COMPLETE!")
        print("="*50)
        print("\nNext steps:")
        print("1. Run sync_confluence_to_sharepoint.py to upload content")
        print("2. Configure Microsoft Forms for training quiz")
        print("3. Add staff members to appropriate security groups")
        print("4. Test the site with a few pilot users")
        print("5. Schedule staff training on using the portal")
        print("\n📌 Site URL:", SITE_URL)
        print("📧 Support: security@ethos.co.im")
        print("\n" + "="*50 + "\n")

        return True


def main():
    """Main execution function"""
    setup = SharePointSetup()

    try:
        success = setup.setup_site()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⛔ Setup cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()