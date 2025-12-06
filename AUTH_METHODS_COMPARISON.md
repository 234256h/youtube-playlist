# Google Drive Upload - Authentication Methods Comparison

## Quick Decision Guide

```
Do you need automated/unattended uploads?
│
├─ YES → Use Service Account
│   ├─ Setup: More complex
│   ├─ File: service_account.json
│   └─ Best for: CI/CD, cron jobs, servers
│
└─ NO → Use OAuth 2.0
    ├─ Setup: Simple
    ├─ File: client_secrets.json
    └─ Best for: Personal use, one-time uploads
```

---

## Method 1: OAuth 2.0 (User Authentication)

### Visual Flow

```
┌─────────────┐
│   You run   │
│  the script │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Browser    │
│  opens      │ ← First time only
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  You sign   │
│  in & allow │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Token      │
│  saved      │ ← token.json
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Upload to  │
│ YOUR Drive  │ ← Your personal Google Drive
└─────────────┘
```

### Setup Steps

```
1. Google Cloud Console
   └─ Create Project

2. Enable APIs
   └─ Google Drive API ✓

3. Create Credentials
   └─ OAuth 2.0 Client ID (Desktop app)

4. Download JSON
   └─ Save as: client_secrets.json

5. Run Script
   └─ Browser opens → Sign in → Done!
```

### Files Created

```
your-project/
├── client_secrets.json    ← You download this
└── token.json            ← Auto-created after first login
```

### Command

```bash
python upload_to_google_drive.py ./my_folder
```

---

## Method 2: Service Account (Machine Authentication)

### Visual Flow

```
┌─────────────┐
│   You run   │
│  the script │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Script     │
│  reads key  │ ← service_account.json
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Automatic  │
│  auth       │ ← No browser needed
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Upload to  │
│  SA Drive   │ ← Service Account's Drive*
└─────────────┘

* To use YOUR Drive: Share folder with service account email
```

### Setup Steps

```
1. Google Cloud Console
   └─ Create Project

2. Enable APIs
   └─ Google Drive API ✓

3. Create Service Account
   └─ Create new service account

4. Create Key
   └─ Add Key → Create new key → JSON

5. Download JSON
   └─ Save as: service_account.json

6. (Optional) Share Folder
   └─ Share your Drive folder with service account email
```

### Files Created

```
your-project/
└── service_account.json   ← You download this
                           ← No token.json needed
```

### Command

```bash
python upload_to_google_drive.py ./my_folder --auth service_account
```

---

## Side-by-Side Comparison

| Feature | OAuth 2.0 | Service Account |
|---------|-----------|-----------------|
| **Setup Difficulty** | ⭐ Easy | ⭐⭐⭐ Complex |
| **First Time Use** | Opens browser | Silent |
| **User Interaction** | Required once | Never |
| **Best For** | Personal use | Automation |
| **Files Upload To** | Your Drive | Service Account Drive* |
| **Token Management** | Auto-refresh | No token needed |
| **Suitable for CI/CD** | ❌ No | ✅ Yes |
| **Suitable for Laptop** | ✅ Yes | ✅ Yes |
| **Expiration** | Token refreshes | No expiration |

\* Service Account uploads to its own Drive unless you share a folder

---

## When to Use Each Method

### Use OAuth 2.0 When:
- ✅ You're uploading files manually
- ✅ You want files in YOUR Google Drive
- ✅ You're okay with browser authentication
- ✅ You're using your personal computer
- ✅ You need simple setup
- ✅ You upload occasionally

### Use Service Account When:
- ✅ You're automating uploads (cron, CI/CD)
- ✅ No browser is available (server environment)
- ✅ You need zero user interaction
- ✅ You're okay with sharing folders
- ✅ You're building a service
- ✅ You upload programmatically

---

## Common Scenarios

### Scenario 1: Personal Zoom Recordings
**Recommendation:** OAuth 2.0

```bash
# Once in a while, upload recordings
python download_zoom_recordings.py "https://zoom.us/..."
python upload_to_google_drive.py ./downloads/meeting_name
```

**Why:** Simple, uploads to your Drive, minimal setup

---

### Scenario 2: Daily Automated Backups
**Recommendation:** Service Account

```bash
# In crontab or CI/CD
0 2 * * * /path/to/upload_to_google_drive.py /backups --auth service_account
```

**Why:** No user interaction, reliable for automation

---

### Scenario 3: Development/Testing
**Recommendation:** OAuth 2.0

**Why:** Quick to set up, easy to test, uses your account

---

### Scenario 4: Production Server
**Recommendation:** Service Account

**Why:** No browser, no user interaction, secure

---

## Authentication Flow Diagrams

### OAuth 2.0 Flow (First Time)

```
Script Start
    ↓
Check token.json → Not found
    ↓
Open browser
    ↓
User signs in
    ↓
User grants permissions
    ↓
Token received
    ↓
Save to token.json
    ↓
Upload files
    ↓
Done ✓
```

### OAuth 2.0 Flow (Subsequent Times)

```
Script Start
    ↓
Check token.json → Found!
    ↓
Token valid? → Yes → Upload files → Done ✓
    ↓
   No
    ↓
Refresh token
    ↓
Upload files
    ↓
Done ✓
```

### Service Account Flow (Always the Same)

```
Script Start
    ↓
Read service_account.json
    ↓
Create credentials
    ↓
Upload files
    ↓
Done ✓
```

---

## Security Comparison

### OAuth 2.0 Security

**Credentials File:** `client_secrets.json`
- Contains: Client ID and Client Secret
- Risk Level: Medium (public client)
- Can be shared: Technically yes, but not recommended
- If leaked: Attacker still needs user authorization

**Token File:** `token.json`
- Contains: Access token and refresh token
- Risk Level: High
- Can be shared: NO - NEVER
- If leaked: Attacker can access YOUR Drive

### Service Account Security

**Credentials File:** `service_account.json`
- Contains: Private key
- Risk Level: Very High
- Can be shared: NO - NEVER
- If leaked: Full access to service account's Drive

**Best Practices:**
- Never commit credential files
- Use environment variables in production
- Rotate service account keys regularly
- Delete unused keys
- Enable audit logging

---

## File Location Comparison

### OAuth 2.0
```
Your Google Drive
└── My Drive/
    └── Uploaded Folder/  ← Files appear here
        ├── file1.pdf
        ├── file2.mp4
        └── file3.txt
```

### Service Account (Default)
```
Service Account's Drive (Not visible to you!)
└── My Drive/
    └── Uploaded Folder/  ← Files are here, but you can't see them
        ├── file1.pdf
        ├── file2.mp4
        └── file3.txt
```

### Service Account (With Shared Folder)
```
1. You create folder in YOUR Drive: "Shared Uploads"
2. You share "Shared Uploads" with: service-account@project.iam.gserviceaccount.com
3. Service account uploads to "Shared Uploads"
4. You can see files in YOUR Drive!

Your Google Drive
└── My Drive/
    └── Shared Uploads/  ← Service account uploads here
        └── Uploaded Folder/
            ├── file1.pdf
            ├── file2.mp4
            └── file3.txt
```

---

## Cost Comparison

Both methods are **FREE** for the API usage!

You only pay for:
- Google Drive storage space (same pricing regardless of auth method)
- Nothing else!

**Note:** Google Drive API has very generous free quotas that most users will never hit.

---

## Switching Between Methods

### From OAuth to Service Account
```bash
# Old command (OAuth)
python upload_to_google_drive.py ./folder

# New command (Service Account)
python upload_to_google_drive.py ./folder --auth service_account
```

### From Service Account to OAuth
```bash
# Old command (Service Account)
python upload_to_google_drive.py ./folder --auth service_account

# New command (OAuth)
python upload_to_google_drive.py ./folder --auth oauth
```

You can have both credential files and switch as needed!

---

## Troubleshooting Decision Tree

```
Upload not working?
│
├─ Using OAuth?
│   ├─ Browser doesn't open?
│   │   └─ Check: Running on machine with browser?
│   │
│   ├─ Permission denied?
│   │   └─ Delete token.json and try again
│   │
│   └─ Can't see files?
│       └─ Check: Signed in to correct Google account?
│
└─ Using Service Account?
    ├─ Authentication error?
    │   └─ Check: service_account.json is valid JSON
    │
    └─ Can't see uploaded files?
        └─ Share a folder with service account email!
```

---

## Quick Reference Commands

### OAuth (Default)
```bash
# Basic
python upload_to_google_drive.py ./folder

# Custom Drive folder name
python upload_to_google_drive.py ./folder -d "My Files"

# Custom credentials
python upload_to_google_drive.py ./folder -c my_oauth.json
```

### Service Account
```bash
# Basic
python upload_to_google_drive.py ./folder -a service_account

# Custom credentials
python upload_to_google_drive.py ./folder -a service_account -c my_sa.json

# With custom Drive folder
python upload_to_google_drive.py ./folder -a service_account -d "Backups"
```

---

## Summary

**For most users:** Start with **OAuth 2.0** - it's simpler and files go to your Drive.

**For automation:** Use **Service Account** - it's perfect for unattended operation.

**Can't decide?** Use OAuth 2.0 first, switch to Service Account later if needed.

Both methods are fully supported and work great! 🚀

