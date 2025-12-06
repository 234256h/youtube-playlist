# Quick Start Guide: Google Drive Upload

## TL;DR - Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Make sure you're in the project folder and virtual environment is activated
source .venv/bin/activate

# Install Google Drive packages
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Get Google Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Click "APIs & Services" → "Enable APIs and Services"
4. Search "Google Drive API" and enable it
5. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
6. If prompted, configure consent screen:
   - Choose "External"
   - Fill in app name and your email
   - Add your email as test user
7. Select "Desktop app" as application type
8. Download the JSON file
9. **Rename it to `client_secrets.json`** and put it in this folder

### Step 3: Upload to Google Drive

```bash
# Upload a folder (first time will open browser for authentication)
python upload_to_google_drive.py ./downloads/your_folder_name
```

That's it! 🎉

---

## Common Commands

### Upload with custom Drive folder name
```bash
python upload_to_google_drive.py ./downloads/Meeting_Name --drive-folder "My Recordings"
```

### Complete workflow: Download from Zoom → Upload to Drive
```bash
# Download
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"

# Upload (adjust the folder name based on what was downloaded)
python upload_to_google_drive.py ./downloads/Meeting_Title_Date --drive-folder "Zoom Recordings"
```

---

## Troubleshooting

### "Credentials file not found"
- Make sure you renamed the downloaded file to `client_secrets.json`
- Check that it's in the same folder as `upload_to_google_drive.py`

### Browser doesn't open for authentication
- Make sure you're running on a computer with a browser (not a server)
- Try running the command again
- Check your firewall settings

### "Permission denied" during authentication
- Make sure you added your email as a test user in the OAuth consent screen
- Click "Allow" when asked to grant permissions

### Can't see uploaded files in Google Drive
- Check the "My Drive" root folder
- Search for the folder name you specified
- Files are uploaded to your authenticated Google account

---

## Authentication Methods Comparison

| Feature | OAuth 2.0 | Service Account |
|---------|-----------|-----------------|
| **Setup** | Easy - browser auth | Complex - JSON key |
| **Best For** | Personal use | Automation |
| **User Interaction** | Required first time | None |
| **Files Location** | Your personal Drive | Service account Drive* |
| **Token Expiry** | Auto-refreshes | No expiry |

\* For Service Account, you need to share a folder with the service account email to upload to your personal Drive

---

## Need More Help?

- **Detailed authentication setup:** See [GOOGLE_DRIVE_AUTH_SETUP.md](GOOGLE_DRIVE_AUTH_SETUP.md)
- **Full documentation:** See [README.md](README.md)
- **Command help:** Run `python upload_to_google_drive.py --help`

---

## File Security Reminder

🔒 **NEVER commit these files to Git:**
- `client_secrets.json`
- `service_account.json`
- `token.json`

These are already in `.gitignore`, but be careful when sharing your code!

