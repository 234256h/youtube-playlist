# Google Drive Upload Script - Complete Summary

## What Was Created

This implementation provides a complete Google Drive upload solution with the following files:

### Main Script
- **`upload_to_google_drive.py`** - The main upload script with full functionality

### Documentation
- **`QUICKSTART_GOOGLE_DRIVE.md`** - 5-minute quick start guide
- **`GOOGLE_DRIVE_AUTH_SETUP.md`** - Detailed authentication setup guide
- **`README.md`** - Updated with complete usage documentation

### Helper Scripts
- **`zoom_to_drive.sh`** - Automated workflow script (download → upload)

### Configuration
- **`requirements.txt`** - Updated with Google Drive dependencies
- **`.gitignore`** - Updated to exclude credentials

---

## Authentication Methods Supported

### 1. OAuth 2.0 (User Authentication)

**Setup Required:**
- `client_secrets.json` - Downloaded from Google Cloud Console

**Best For:**
- ✅ Personal use
- ✅ Interactive sessions
- ✅ Uploading to your own Drive
- ✅ Simple one-time setup

**How It Works:**
1. First run opens browser for authentication
2. User grants permissions
3. Token saved in `token.json` for future use
4. Token auto-refreshes when expired

**Usage:**
```bash
python upload_to_google_drive.py ./my_folder
```

---

### 2. Service Account (Machine-to-Machine)

**Setup Required:**
- `service_account.json` - Service account key from Google Cloud Console

**Best For:**
- ✅ Automated workflows
- ✅ CI/CD pipelines
- ✅ Server environments
- ✅ No user interaction needed

**How It Works:**
1. Uses service account key (no browser needed)
2. No user interaction required
3. No token expiration
4. Files upload to service account's Drive (can share with personal account)

**Usage:**
```bash
python upload_to_google_drive.py ./my_folder --auth service_account
```

---

## Features

### Core Features
- ✅ Upload entire folders with all files
- ✅ Automatic folder creation in Google Drive
- ✅ Progress bars for each file upload
- ✅ Resumable uploads for large files
- ✅ Error handling and retry logic
- ✅ Support for all file types

### Authentication
- ✅ OAuth 2.0 (browser-based)
- ✅ Service Account (automated)
- ✅ Token refresh handling
- ✅ Custom credentials file paths

### User Experience
- ✅ Colored console output
- ✅ Progress bars (via tqdm)
- ✅ Detailed status messages
- ✅ Success/failure statistics
- ✅ Google Drive links to uploaded content

---

## Command Line Interface

### Basic Usage
```bash
python upload_to_google_drive.py <folder_path>
```

### All Options
```bash
python upload_to_google_drive.py <folder_path> \
  --drive-folder "Custom Folder Name" \
  --auth oauth|service_account \
  --credentials path/to/credentials.json \
  --token path/to/token.json \
  --no-progress
```

### Options Explained

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--drive-folder` | `-d` | Name for folder in Google Drive | Local folder name |
| `--auth` | `-a` | Authentication method | `oauth` |
| `--credentials` | `-c` | Path to credentials file | Auto-detected |
| `--token` | `-t` | Path to OAuth token file | `token.json` |
| `--no-progress` | - | Disable progress bars | Progress enabled |
| `--help` | `-h` | Show help message | - |

---

## Setup Guide

### Prerequisites
1. Python 3.7 or higher
2. Google account
3. Internet connection

### Installation Steps

#### 1. Install Dependencies
```bash
# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

#### 2. Google Cloud Console Setup

**For OAuth (Recommended for Personal Use):**

1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Google Drive API
4. Create OAuth 2.0 credentials:
   - Type: Desktop app
   - Download as `client_secrets.json`
5. Configure consent screen (add yourself as test user)

**For Service Account (For Automation):**

1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Google Drive API
4. Create Service Account
5. Create and download JSON key
6. Save as `service_account.json`

#### 3. Place Credentials
Put the credentials file in the same folder as the script:
- OAuth: `client_secrets.json`
- Service Account: `service_account.json`

---

## Usage Examples

### Example 1: Basic Upload
```bash
python upload_to_google_drive.py ./downloads/Meeting_2024_12_06
```

### Example 2: Custom Drive Folder Name
```bash
python upload_to_google_drive.py ./downloads/Meeting_2024_12_06 \
  --drive-folder "Important Meetings"
```

### Example 3: Service Account (Automation)
```bash
python upload_to_google_drive.py ./downloads/Meeting_2024_12_06 \
  --auth service_account \
  --credentials /path/to/service_account.json
```

### Example 4: Complete Workflow (Zoom → Drive)
```bash
# Download from Zoom
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"

# Upload to Drive
python upload_to_google_drive.py ./downloads/Meeting_Name \
  --drive-folder "Zoom Recordings 2024"
```

### Example 5: Automated Workflow Script
```bash
# Use the provided shell script
./zoom_to_drive.sh "https://zoom.us/rec/share/xxxxx" "My Recordings"
```

---

## Security Best Practices

### Critical Security Rules

🔒 **NEVER commit these files to Git:**
- `client_secrets.json`
- `service_account.json`
- `token.json`

These files are already added to `.gitignore`.

### Additional Security Tips

1. **Protect Service Account Keys**
   - Treat like passwords
   - Rotate periodically
   - Delete unused keys

2. **OAuth Token Security**
   - `token.json` contains access token
   - Don't share or commit
   - Delete to force re-authentication

3. **Minimal Permissions**
   - Only grant necessary API scopes
   - Review permissions regularly
   - Use service accounts for automation

4. **Monitor Usage**
   - Check Google Cloud Console for activity
   - Review API quotas
   - Watch for unusual patterns

---

## API Quotas and Limits

### Google Drive API Limits
- Queries per day: 1,000,000,000
- Queries per 100 seconds per user: 1,000
- Queries per 100 seconds: 10,000

These limits are very generous for normal use. Most personal use cases won't hit these limits.

### Cost
- Google Drive API is **FREE**
- You only pay for Drive storage space
- Standard Google Drive storage limits apply

---

## Troubleshooting

### Common Issues

#### "Credentials file not found"
**Solution:**
- Verify file exists in script directory
- Check filename: `client_secrets.json` or `service_account.json`
- Use `--credentials` to specify custom path

#### Authentication errors
**Solution:**
- Delete `token.json` and re-authenticate
- Verify Google Drive API is enabled
- Check credentials file is valid JSON
- Add yourself as test user in OAuth consent screen

#### "Permission denied" errors
**OAuth:**
- Click "Allow" in browser
- Add your email as test user

**Service Account:**
- Share target folder with service account email
- Verify service account has Drive access

#### Files upload but not visible
**Cause:** Using Service Account authentication

**Solution:**
- Files go to service account's Drive
- Share a folder with service account email
- Or use OAuth authentication instead

#### Upload fails for large files
**Solution:**
- Check internet connection
- Verify sufficient Drive storage space
- Check firewall settings
- Large files use resumable upload (automatic)

---

## Code Structure

### Main Classes

#### `GoogleDriveUploader`
Main class handling all upload operations.

**Methods:**
- `authenticate()` - Handle authentication
- `create_folder()` - Create folder in Drive
- `find_folder_by_name()` - Search for existing folder
- `upload_file()` - Upload single file
- `upload_folder()` - Upload entire folder

### Authentication Flow

#### OAuth Flow:
```
1. Check for existing token.json
2. If valid, use it
3. If expired, refresh it
4. If none, open browser for auth
5. Save token for future use
```

#### Service Account Flow:
```
1. Load service account JSON
2. Create credentials
3. Build Drive service
4. Ready to use (no user interaction)
```

### Upload Flow:
```
1. Authenticate with Google Drive
2. Find or create target folder
3. Get list of files to upload
4. For each file:
   - Detect MIME type
   - Create file metadata
   - Upload with progress tracking
   - Report success/failure
5. Show final statistics
```

---

## Dependencies

### Required Python Packages
```
google-auth>=2.25.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.110.0
```

### Optional Packages
```
tqdm>=4.66.0  # For progress bars
```

### System Requirements
- Python 3.7+
- Internet connection
- Web browser (for OAuth only)

---

## File Structure

After setup, your project should look like:

```
youtube-playlist/
├── upload_to_google_drive.py          # Main upload script
├── download_zoom_recordings.py        # Zoom download script
├── zoom_to_drive.sh                   # Automated workflow
├── requirements.txt                   # All dependencies
├── README.md                          # Full documentation
├── QUICKSTART_GOOGLE_DRIVE.md        # Quick start guide
├── GOOGLE_DRIVE_AUTH_SETUP.md        # Auth setup guide
├── .gitignore                         # Excludes credentials
│
├── client_secrets.json               # OAuth credentials (do not commit)
├── service_account.json              # Service account key (do not commit)
├── token.json                         # OAuth token (do not commit)
│
└── downloads/                         # Downloaded files
    └── Meeting_Name/
        ├── video.mp4
        ├── audio.m4a
        └── chat.txt
```

---

## Advanced Usage

### Environment Variables

Instead of credential files, you can use environment variables:

```bash
# OAuth
export GOOGLE_CLIENT_SECRETS='{"installed":{...}}'

# Service Account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"
```

### Programmatic Usage

You can also import and use the class in your own scripts:

```python
from upload_to_google_drive import GoogleDriveUploader

# Create uploader
uploader = GoogleDriveUploader(auth_method='oauth')

# Authenticate
if uploader.authenticate():
    # Upload folder
    stats = uploader.upload_folder(
        local_folder='./my_files',
        drive_folder_name='My Files'
    )
    print(f"Uploaded {stats['success']} files")
```

---

## Future Enhancements (Potential)

These features are not currently implemented but could be added:

- [ ] Recursive folder upload (subfolders)
- [ ] Incremental uploads (skip existing files)
- [ ] Parallel uploads for faster transfer
- [ ] File deduplication
- [ ] Custom MIME type mapping
- [ ] Sharing permissions management
- [ ] Download from Google Drive
- [ ] Sync functionality (bi-directional)
- [ ] Conflict resolution
- [ ] Bandwidth throttling

---

## Getting Help

### Documentation
1. **Quick Start:** See `QUICKSTART_GOOGLE_DRIVE.md`
2. **Authentication:** See `GOOGLE_DRIVE_AUTH_SETUP.md`
3. **Full Docs:** See `README.md`

### Command Help
```bash
python upload_to_google_drive.py --help
```

### Common Resources
- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)

---

## License

Same as the main youtube-playlist project.

---

**Created:** December 2024  
**Version:** 1.0  
**Python:** 3.7+  
**Status:** Production Ready ✅

