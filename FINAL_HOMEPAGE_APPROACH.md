# FINAL SOLUTION: Native SharePoint Homepage

## The Problem
SharePoint security policies prevent:
- ❌ Setting HTML files as welcome pages
- ❌ Embedding HTML files from document libraries in iframes
- ❌ Programmatic site page creation with app-only permissions

## The Solution: Recreate the Portal as a Native SharePoint Page

Instead of fighting SharePoint, let's **recreate your beautiful ISMS portal design using native SharePoint web parts**.

### Manual Steps (10 minutes):

1. **Go to the homepage and click Edit**
   - URL: https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement

2. **Delete all existing web parts**

3. **Add Hero Web Part (for the blue banner)**
   - Click `+` → Search "Hero"
   - Choose layout: 1 tile
   - Configure:
     - Title: "🔒 Welcome to ETHOS ISMS Portal"
     - Description: "Your comprehensive resource for information security policies, procedures, and compliance"
     - Background: Choose a blue color or upload a blue gradient image

4. **Add Text Web Part (Section Title)**
   - Add text: "Quick Actions"
   - Format as Heading 2

5. **Add Quick Links Web Part (for the 4 action cards)**
   - Click `+` → "Quick links"
   - Layout: Choose "Grid" or "Tiles"
   - Add 4 links:
     1. Title: "🚨 Report Incident" | URL: `mailto:security@ethos.co.im?subject=Security%20Incident%20Report`
     2. Title: "🔐 Request Access" | URL: `mailto:richard.wild@ethos.co.im?subject=Access%20Request`
     3. Title: "📚 Training Materials" | URL: `../03_Training/Staff_Training/ISMS_TRN_001_Security_Awareness_Training_Framework.html`
     4. Title: "❓ Help & Support" | URL: `../05_Quick_Reference/Welcome_Guide.html`

6. **Add another Text Web Part**
   - Text: "Document Library"
   - Format as Heading 2

7. **Add Quick Links Web Part (for document categories)**
   - Layout: Choose "Tiles" with icons
   - Add links:
     1. Title: "📄 Policies" | URL: `../01_Policies`
     2. Title: "📝 Procedures" | URL: `../02_Procedures`
     3. Title: "🎓 Training" | URL: `../03_Training`
     4. Title: "📋 Forms" | URL: `../04_Forms_Templates`

8. **Add another Text Web Part (Essential Reading)**
   - Text: "Essential Reading"
   - Format as Heading 2

9. **Add final Quick Links Web Part**
   - Add key document links:
     1. "📖 Information Security Policy" → Policy document
     2. "💻 Acceptable Use Policy" → Policy document
     3. "🆘 Incident Response" → Procedure document

10. **Publish the page**

---

## Why This Works Better

✅ **Native SharePoint** - no security blocks
✅ **Mobile responsive** - automatic
✅ **Easy to maintain** - click to edit
✅ **Search indexed** - better findability
✅ **Looks professional** - modern SharePoint design
✅ **No downloads** - everything just works

---

## Alternative: Direct Link Approach

If you don't want to rebuild the homepage, just:

1. **Share the direct link** with staff to bookmark:
   ```
   https://ethosltduk.sharepoint.com/sites/InformationSecurityManagement/Shared Documents/ISMS_Portal_Home.html
   ```

2. **Add to Quick Launch navigation** (left sidebar):
   - Settings → Site Settings → Navigation
   - Add link: "ISMS Portal" pointing to the HTML file
   - Staff will see it in every page's sidebar

3. **Pin in Microsoft Teams**:
   - Add as a tab in your Security channel
   - Staff access it from Teams directly

---

## My Recommendation

**Use the native SharePoint approach** - it takes 10 minutes but solves all the technical issues and gives you a maintainable, professional homepage that works exactly how SharePoint expects it to.

Your custom HTML was beautiful, but SharePoint's security model is designed to prevent exactly what we're trying to do. Working with SharePoint instead of against it will save hours of frustration.
