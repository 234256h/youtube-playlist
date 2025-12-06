# youtube-playlist

https://234256h.github.io/youtube-playlist/

https://234256h.github.io/youtube-playlist/playlist-v2.html

---

## Zoom Recording Downloader

A Python script to download all files from Zoom recording URLs with support for password-protected recordings.

### Features

- 🔒 **Password Protection Support**: Automatically detects and prompts for password if needed
- 📁 **Smart Organization**: Downloads files into a folder named after the meeting title
- 📊 **Progress Tracking**: Visual progress bars for each file download
- 🎥 **All File Types**: Downloads videos, audio, chat logs, transcripts, and more
- 🛡️ **Error Handling**: Graceful handling of network issues and invalid URLs
- 🤖 **Browser Automation**: Uses Playwright for reliable page interaction

### Installation

#### Option 1: Using uv (Recommended - much faster!)

```bash
# FIRST TIME SETUP ONLY - Create a virtual environment
uv venv

# Activate the virtual environment (do this every time you open a new terminal)
source .venv/bin/activate  # macOS/Linux
# or on Windows: .venv\Scripts\activate

# Install dependencies with uv
uv pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium
```

**Next time:** Just run `source .venv/bin/activate` to activate the existing environment.

#### Option 2: Using pip

```bash
# FIRST TIME SETUP ONLY - Create a virtual environment
python -m venv .venv

# Activate the virtual environment (do this every time you open a new terminal)
source .venv/bin/activate  # macOS/Linux
# or on Windows: .venv\Scripts\activate

# Install dependencies with pip
pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium
```

**Next time:** Just run `source .venv/bin/activate` to activate the existing environment.

**Note:** If you don't have `uv` installed yet:
```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### Usage

#### Basic Usage

Download a public Zoom recording:
```bash
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"
```

#### Password-Protected Recordings

If the recording requires a password, the script will automatically detect this and prompt you:
```bash
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"
# You'll see: 🔒 Password required for this recording.
# Please enter the password: ****
```

#### Show Browser Window

To see what the script is doing (useful for debugging):
```bash
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx" --visible
```

### How It Works

1. Opens the Zoom recording URL in a browser
2. Detects if a password is required
3. Prompts for password if needed and authenticates
4. Extracts the meeting title from the page
5. Finds all downloadable files (video, audio, chat, transcripts, etc.)
6. Creates a folder named after the meeting
7. Downloads all files with progress bars
8. Reports success/failure for each file

### Output

Files are saved in a `downloads` folder with subfolders for each meeting:
```
downloads/
├── Meeting_Title_2024_12_06/
│   ├── video.mp4
│   ├── audio.m4a
│   ├── chat.txt
│   └── transcript.vtt
└── Another_Meeting/
    └── recording.mp4
```

### Requirements

- Python 3.7 or higher
- Internet connection
- ~500MB disk space for Playwright browser

### Troubleshooting

#### "No download links found"
- The recording may not be available for download
- Try running with `--visible` to see the page
- Check if the URL is correct and accessible

#### "Timeout loading page"
- Check your internet connection
- The Zoom servers might be slow, try again
- Verify the URL is correct

#### "Incorrect password"
- Double-check the password
- Make sure there are no extra spaces
- Try accessing the link in a regular browser first

#### Import errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

### Dependencies

- **playwright**: Browser automation framework
- **tqdm**: Progress bar library
- **requests**: HTTP library for file downloads

### License

Same as the main youtube-playlist project.

---

## Google Drive Upload Script

A Python script to upload folders and their contents to Google Drive with support for multiple authentication methods.

### Features

- 📤 **Folder Upload**: Upload entire folders with all files to Google Drive
- 🔐 **Multiple Auth Methods**: OAuth 2.0 (personal) or Service Account (automation)
- 📊 **Progress Tracking**: Visual progress bars for each file upload
- 🎯 **Smart Folder Management**: Automatically creates or finds folders in Drive
- 🛡️ **Error Handling**: Graceful handling of upload failures
- 🔄 **Resumable Uploads**: Support for large files with resumable upload protocol

### Authentication Methods

#### 1. OAuth 2.0 (Recommended for Personal Use)
- **Best for:** Interactive use, personal Google accounts
- **Setup:** Browser-based authentication, requires `client_secrets.json`
- **Files upload to:** Your personal Google Drive

#### 2. Service Account (Recommended for Automation)
- **Best for:** Automated workflows, CI/CD, server environments
- **Setup:** No user interaction, requires `service_account.json`
- **Files upload to:** Service account's Drive (can share folder with your account)

### Installation

```bash
# Activate your virtual environment (if not already activated)
source .venv/bin/activate  # macOS/Linux
# or on Windows: .venv\Scripts\activate

# Install Google Drive dependencies
uv pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Or with regular pip
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Setup

**For detailed authentication setup instructions, see [GOOGLE_DRIVE_AUTH_SETUP.md](GOOGLE_DRIVE_AUTH_SETUP.md)**

Quick setup:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google Drive API
3. Create credentials:
   - **OAuth:** Create "OAuth client ID" (Desktop app) → download as `client_secrets.json`
   - **Service Account:** Create service account → download key as `service_account.json`
4. Place the credentials file in the same folder as the script

### Usage

#### Basic Upload with OAuth (Default)

```bash
python upload_to_google_drive.py ./downloads/Meeting_Name
```

On first run, your browser will open for authentication. Grant permissions and the script will save your token for future use.

#### Upload with Custom Google Drive Folder Name

```bash
python upload_to_google_drive.py ./downloads/Meeting_Name --drive-folder "My Zoom Recordings"
```

#### Upload with Service Account (No Browser Interaction)

```bash
python upload_to_google_drive.py ./downloads/Meeting_Name --auth service_account
```

#### Upload with Custom Credentials File

```bash
python upload_to_google_drive.py ./downloads/Meeting_Name --credentials my_creds.json
```

#### Disable Progress Bars

```bash
python upload_to_google_drive.py ./downloads/Meeting_Name --no-progress
```

### Command Line Options

```
python upload_to_google_drive.py [OPTIONS] FOLDER

Arguments:
  FOLDER                    Path to the local folder to upload

Options:
  -d, --drive-folder NAME   Name for the folder in Google Drive 
                           (defaults to local folder name)
  -a, --auth METHOD         Authentication method: oauth or service_account
                           (default: oauth)
  -c, --credentials FILE    Path to credentials file
                           (default: client_secrets.json or service_account.json)
  -t, --token FILE         Path to OAuth token file
                           (default: token.json, only used for OAuth)
  --no-progress            Disable progress bars
  -h, --help               Show help message
```

### Complete Workflow: Download from Zoom → Upload to Google Drive

```bash
# 1. Download Zoom recording
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"

# 2. Upload to Google Drive
python upload_to_google_drive.py ./downloads/Meeting_Title_2024_12_06 --drive-folder "Zoom Recordings"
```

### Output

The script will:
1. Authenticate with Google Drive
2. Find or create the specified folder in Drive
3. Upload all files from the local folder
4. Show progress for each file
5. Report success/failure statistics

Example output:
```
🔐 Starting OAuth authentication flow...
✅ OAuth authentication successful

📤 Starting upload: ./downloads/Meeting_Name -> Zoom Recordings
📁 Created folder: Zoom Recordings
   ID: 1a2b3c4d5e6f7g8h9i0j
   Link: https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j

📊 Found 3 file(s) to upload
video.mp4: 100%|████████████████████| 45.2M/45.2M [00:15<00:00, 2.89MB/s]
✅ Uploaded: video.mp4
chat.txt: 100%|█████████████████████| 1.2K/1.2K [00:01<00:00, 890B/s]
✅ Uploaded: chat.txt
transcript.vtt: 100%|████████████████| 8.5K/8.5K [00:01<00:00, 5.2KB/s]
✅ Uploaded: transcript.vtt

📈 Upload complete:
   ✅ Success: 3
   ❌ Failed: 0
```

### Security

**⚠️ IMPORTANT:** Do not commit credential files to Git!

Add to your `.gitignore`:
```
client_secrets.json
service_account.json
token.json
```

### Troubleshooting

#### "Credentials file not found"
- Make sure you've downloaded credentials from Google Cloud Console
- Check the filename: `client_secrets.json` (OAuth) or `service_account.json` (Service Account)
- Use `--credentials` to specify a custom path

#### Authentication errors
- Delete `token.json` and try again
- Check that Google Drive API is enabled in Cloud Console
- Verify credentials file is valid JSON

#### "Permission denied" errors
- For OAuth: Make sure you clicked "Allow" in the browser
- For Service Account: Share the target folder with the service account email

#### Files upload but can't see them in my Drive
- This happens with Service Account authentication
- Files go to the service account's Drive, not yours
- Solution: Share a folder with the service account email, or use OAuth instead

For detailed troubleshooting, see [GOOGLE_DRIVE_AUTH_SETUP.md](GOOGLE_DRIVE_AUTH_SETUP.md)

### Requirements

- Python 3.7 or higher
- Google account
- Google Cloud project with Drive API enabled
- Internet connection

### Dependencies

- **google-auth**: Google authentication library
- **google-auth-oauthlib**: OAuth 2.0 support
- **google-auth-httplib2**: HTTP library for Google auth
- **google-api-python-client**: Google Drive API client
- **tqdm**: Progress bar library (optional, for progress display)
