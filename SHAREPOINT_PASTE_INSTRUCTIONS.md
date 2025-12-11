# Copy-Paste Instructions for SharePoint Homepage

## Step 1: Get to Edit Mode
1. Go to: https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement
2. Click **Edit** (top right)
3. **Delete all existing web parts** on the page

---

## Step 2: Add Hero Banner

**Add a Text Web Part:**
1. Click **+**
2. Choose **Text**
3. Click the **</>** icon (if visible) OR just paste this directly:

```
🔒 Welcome to ETHOS ISMS Portal

Your comprehensive resource for information security policies, procedures, and compliance
```

4. Highlight the first line → Make it **Heading 1** → **Center align**
5. Highlight the second line → **Center align**
6. Click the web part settings (⚙️) → Change background to **Blue** or **#0078D4**
7. Set padding to make it taller (if option available)

---

## Step 3: Quick Actions Section

**Add Text Web Part:**
1. Click **+** below the blue section
2. Choose **Text**
3. Type: `Quick Actions`
4. Make it **Heading 2** and **center align**

**Add Quick Links Web Part:**
1. Click **+** below
2. Choose **Quick links**
3. Click **Edit web part** (pencil icon)
4. Layout: Choose **Grid** or **Tiles**
5. Add these 4 links one by one:

**Link 1:**
- Title: `Report Incident`
- Description: `Quickly report security incidents`
- URL: `mailto:security@ethos.co.im?subject=Security%20Incident%20Report`
- Icon: 🚨 (or search for "alert")

**Link 2:**
- Title: `Request Access`
- Description: `Submit system access requests`
- URL: `mailto:richard.wild@ethos.co.im?subject=Access%20Request`
- Icon: 🔐 (or search for "lock")

**Link 3:**
- Title: `Training Materials`
- Description: `Access security training resources`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/03_Training`
- Icon: 📚 (or search for "book")

**Link 4:**
- Title: `Help & Support`
- Description: `Get help and find answers`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/05_Quick_Reference`
- Icon: ❓ (or search for "help")

---

## Step 4: Document Library Section

**Add Text Web Part:**
1. Click **+**
2. Choose **Text**
3. Type: `Document Library`
4. Make it **Heading 2** and **center align**

**Add Quick Links Web Part:**
1. Click **+** below
2. Choose **Quick links**
3. Layout: **Tiles** or **Grid**
4. Add these 4 links:

**Link 1:**
- Title: `Policies`
- Description: `12 documents`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/01_Policies`
- Icon: 📄

**Link 2:**
- Title: `Procedures`
- Description: `8 documents`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/02_Procedures`
- Icon: 📝

**Link 3:**
- Title: `Training`
- Description: `Materials & Guides`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/03_Training`
- Icon: 🎓

**Link 4:**
- Title: `Forms`
- Description: `Templates`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/04_Forms_Templates`
- Icon: 📋

---

## Step 5: Essential Reading Section

**Add Text Web Part:**
1. Click **+**
2. Choose **Text**
3. Type: `Essential Reading`
4. Make it **Heading 2** and **center align**

**Add Quick Links Web Part:**
1. Click **+** below
2. Choose **Quick links**
3. Layout: **Tiles** or **Compact**
4. Add these 3 links:

**Link 1:**
- Title: `Information Security Policy`
- Description: `Core security principles for all staff`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/01_Policies/Core_Policies/ISMS_POL_001_Information_Security_Policy.html`
- Icon: 📖

**Link 2:**
- Title: `Acceptable Use Policy`
- Description: `Guidelines for IT resource usage`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/01_Policies/Core_Policies/ISMS_POL_008_Acceptable_Use_Policy.html`
- Icon: 💻

**Link 3:**
- Title: `Incident Response`
- Description: `What to do when incidents occur`
- URL: `https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared%20Documents/02_Procedures/Emergency/ISMS_PRO_002_Incident_Response_Procedure.html`
- Icon: 🆘

---

## Step 6: Publish

1. Click **Publish** (top right)
2. Done!

---

## Tips:

- **If URLs are too long**, SharePoint will still accept them - just paste the full URL
- **Icons**: Use emojis (🔒📄📚) in the title field OR use SharePoint's icon picker
- **Colors**: If Quick Links web parts allow color customization, use:
  - Primary: #0078D4
  - Secondary: #50E6FF
- **Layout**: Grid or Tiles work best for the card-style look

---

## Troubleshooting:

**If Quick Links won't accept URLs:**
- Make sure you're using the FULL URL starting with `https://`
- For mailto links, use the exact format: `mailto:email@domain.com?subject=Your%20Subject`

**If you can't find Quick Links:**
- Search for "Quick links" in the web part search
- Alternative: Use "Button" web parts instead (one button per link)

**If HTML files download when clicked:**
- This is normal for HTML files in document libraries
- Staff will need to open them after download
- OR convert all HTML files to SharePoint pages (advanced)
