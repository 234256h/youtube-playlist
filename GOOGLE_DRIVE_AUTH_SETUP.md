# Google Drive Upload Script - Authentication Setup Guide

This guide explains how to set up authentication for the Google Drive upload script.

## Authentication Methods

The script supports two authentication methods:

### 1. OAuth 2.0 (Recommended for Personal Use)

**Best for:** Interactive use, personal accounts, one-time uploads

**Pros:**
- Simple browser-based authentication
- Works with personal Google accounts
- Files upload to your own Google Drive

**Cons:**
- Requires manual browser interaction
- Token expires and needs refresh

**Setup Instructions:**

1. **Go to Google Cloud Console**
   - Visit https://console.cloud.google.com/

2. **Create or Select a Project**
   - Click "Select a project" at the top
   - Click "New Project"
   - Enter a name (e.g., "Drive Upload Script")
   - Click "Create"

3. **Enable Google Drive API**
   - In the left sidebar, go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click on it and click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure the OAuth consent screen:
     - User Type: External (for personal use)
     - App name: "Drive Upload Script" (or any name)
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue"
     - Scopes: Skip this (click "Save and Continue")
     - Test users: Add your email address
     - Click "Save and Continue"
   - Back at "Create OAuth client ID":
     - Application type: "Desktop app"
     - Name: "Drive Upload Client"
     - Click "Create"

5. **Download Credentials**
   - Click the download icon (⬇️) next to your newly created OAuth 2.0 Client ID
   - Save the JSON file as `client_secrets.json` in the same folder as the script

6. **First Run**
   - When you first run the script, it will open your browser
   - Sign in with your Google account
   - Click "Allow" to grant permissions
   - The script will save a token for future use

### 2. Service Account (Recommended for Automation)

**Best for:** Automation, server environments, CI/CD pipelines

**Pros:**
- No user interaction needed
- Doesn't expire (as long as the key is valid)
- Perfect for automated workflows

**Cons:**
- More complex setup
- Files upload to service account's Drive (not your personal Drive)
- Need to share folders with service account email to access your Drive

**Setup Instructions:**

1. **Go to Google Cloud Console**
   - Visit https://console.cloud.google.com/

2. **Create or Select a Project**
   - Same as OAuth method above

3. **Enable Google Drive API**
   - Same as OAuth method above

4. **Create Service Account**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Service account name: "drive-upload-service"
   - Service account ID: (auto-generated)
   - Click "Create and Continue"
   - Role: "Basic" > "Editor" (or skip this step)
   - Click "Continue" then "Done"

5. **Create Service Account Key**
   - In the "Service Accounts" list, click on your newly created service account
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"
   - Key type: JSON
   - Click "Create"
   - The JSON key file will be downloaded

6. **Save the Key**
   - Save the downloaded JSON file as `service_account.json` in the same folder as the script
   - **IMPORTANT:** Keep this file secure! Anyone with this file can access your Drive

7. **Sharing Folders (Optional)**
   - If you want to upload to your personal Drive:
     1. Open the `service_account.json` file
     2. Find the "client_email" field (e.g., `drive-upload-service@project-id.iam.gserviceaccount.com`)
     3. In Google Drive, share the target folder with this email address
     4. Give it "Editor" permissions

## File Structure

After setup, your folder should look like this:

```
youtube-playlist/
├── upload_to_google_drive.py       # The upload script
├── client_secrets.json             # OAuth credentials (if using OAuth)
├── service_account.json            # Service account key (if using Service Account)
├── token.json                      # OAuth token (auto-generated, do not commit)
└── requirements.txt                # Python dependencies
```

## Security Best Practices

### ⚠️ DO NOT COMMIT CREDENTIALS TO GIT

Add these to your `.gitignore`:

```
# Google Drive credentials
client_secrets.json
service_account.json
token.json
*.json
!package.json
```

### Additional Security Tips

1. **OAuth Token:** The `token.json` file contains your access token. Keep it secure.
2. **Service Account Key:** Never share the `service_account.json` file. Treat it like a password.
3. **Rotate Keys:** Periodically delete and recreate service account keys
4. **Minimal Permissions:** Only grant necessary permissions to service accounts
5. **Monitor Usage:** Check Google Cloud Console for any unusual API activity

## Environment Variables (Alternative)

Instead of keeping credentials in files, you can use environment variables:

### For OAuth:
```bash
export GOOGLE_CLIENT_SECRETS='{"installed":{"client_id":"...","client_secret":"..."}}'
```

### For Service Account:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"
```

## Troubleshooting

### "Credentials file not found"
- Make sure the credentials file is in the same folder as the script
- Check the filename matches exactly: `client_secrets.json` or `service_account.json`
- Use `--credentials` flag to specify a custom path

### "OAuth consent screen required"
- Your app needs to be verified if used by many users
- For personal use, add your email to "Test users"
- For public use, submit for verification in Cloud Console

### "Permission denied" or "403 Forbidden"
- Make sure you enabled the Google Drive API in Cloud Console
- Check that OAuth consent screen is configured
- Verify the service account has proper permissions

### "Token expired"
- Delete `token.json` and authenticate again
- The script will automatically refresh expired tokens

### "Files appear in service account's Drive, not mine"
- This is expected behavior for service accounts
- Share a folder with the service account email
- Or use OAuth authentication instead

## API Quotas

Google Drive API has usage quotas:

- **Queries per day:** 1,000,000,000
- **Queries per 100 seconds per user:** 1,000
- **Queries per 100 seconds:** 10,000

These limits are very generous for personal use. If you hit them, you can request an increase in the Cloud Console.

## Cost

The Google Drive API is **FREE** for reasonable usage. You only pay for storage space in your Google Drive account.

