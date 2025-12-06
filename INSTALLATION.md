# 🚀 Google Drive Upload Script - Installation & First Run

## ✅ What You Have

The following files have been created:

### 📜 Scripts
1. **`upload_to_google_drive.py`** - Main upload script (executable)
2. **`zoom_to_drive.sh`** - Automated workflow script (executable)

### 📚 Documentation
1. **`QUICKSTART_GOOGLE_DRIVE.md`** - 5-minute quick start
2. **`GOOGLE_DRIVE_AUTH_SETUP.md`** - Detailed auth setup
3. **`AUTH_METHODS_COMPARISON.md`** - Visual comparison of auth methods
4. **`GOOGLE_DRIVE_SUMMARY.md`** - Complete reference guide
5. **`README.md`** - Updated with full documentation

### ⚙️ Configuration
1. **`requirements.txt`** - Updated with Google Drive dependencies
2. **`.gitignore`** - Updated to exclude credentials

---

## 🎯 First Time Setup (3 Steps)

### Step 1: Install Python Dependencies

```bash
# Make sure you're in the project directory
cd /Users/rkyo/cursor/youtube-playlist

# Activate virtual environment (if not already)
source .venv/bin/activate

# Install Google Drive packages
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Verify installation
python upload_to_google_drive.py --help
```

**Expected output:** Help message showing all available options

---

### Step 2: Get Google Credentials

#### Option A: OAuth 2.0 (Recommended for Personal Use)

1. **Open:** https://console.cloud.google.com/
2. **Create:** New project (or select existing)
3. **Enable:** Google Drive API
   - Go to "APIs & Services" → "Library"
   - Search "Google Drive API"
   - Click "Enable"
4. **Create Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure consent screen:
     - User Type: External
     - App name: "Drive Upload Script"
     - Your email for support
     - Add yourself as test user
   - Application type: **Desktop app**
   - Click "Create"
5. **Download:** Click download icon (⬇️)
6. **Rename:** Save as `client_secrets.json` in project folder

#### Option B: Service Account (For Automation)

1. **Open:** https://console.cloud.google.com/
2. **Create:** New project (or select existing)
3. **Enable:** Google Drive API (same as above)
4. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name: "drive-upload-service"
   - Click "Create and Continue" → "Done"
5. **Create Key:**
   - Click on your service account
   - "Keys" tab → "Add Key" → "Create new key"
   - Type: JSON
   - Click "Create"
6. **Save:** Rename as `service_account.json` in project folder

---

### Step 3: First Upload

#### With OAuth (Browser-based)

```bash
# This will open your browser for authentication
python upload_to_google_drive.py ./downloads/your_folder_name
```

**What happens:**
1. Browser opens
2. Sign in to Google
3. Click "Allow"
4. Files upload to your Drive
5. Token saved for next time

#### With Service Account (No browser)

```bash
python upload_to_google_drive.py ./downloads/your_folder_name --auth service_account
```

**What happens:**
1. Script authenticates silently
2. Files upload immediately
3. Check your Drive (or service account's Drive)

---

## 📋 Quick Command Reference

### Basic Commands

```bash
# Upload with OAuth (default)
python upload_to_google_drive.py ./my_folder

# Upload with custom Drive folder name
python upload_to_google_drive.py ./my_folder --drive-folder "My Files"

# Upload with Service Account
python upload_to_google_drive.py ./my_folder --auth service_account

# Show help
python upload_to_google_drive.py --help
```

### Complete Workflow

```bash
# 1. Download from Zoom
python download_zoom_recordings.py "https://zoom.us/rec/share/xxxxx"

# 2. Upload to Google Drive
python upload_to_google_drive.py ./downloads/Meeting_Name --drive-folder "Zoom Recordings"

# Or use the automated script
./zoom_to_drive.sh "https://zoom.us/rec/share/xxxxx" "Zoom Recordings"
```

---

## 🧪 Testing the Installation

### Test 1: Check Script Help

```bash
python upload_to_google_drive.py --help
```

**Expected:** Help message showing all options

**If you see an error:** Dependencies not installed, run Step 1 again

---

### Test 2: Check Credentials

```bash
# For OAuth
ls -la client_secrets.json

# For Service Account
ls -la service_account.json
```

**Expected:** File exists and shows size

**If file not found:** Complete Step 2

---

### Test 3: Test Authentication (OAuth)

```bash
# This will test authentication without uploading
python -c "
from upload_to_google_drive import GoogleDriveUploader
uploader = GoogleDriveUploader(auth_method='oauth')
if uploader.authenticate():
    print('✅ Authentication successful!')
else:
    print('❌ Authentication failed')
"
```

**Expected:** Browser opens, you authenticate, see success message

---

### Test 4: Create Test Upload

```bash
# Create test folder with a file
mkdir -p test_upload
echo "Hello Google Drive!" > test_upload/test.txt

# Upload it
python upload_to_google_drive.py ./test_upload --drive-folder "Test Upload"

# Check your Google Drive for "Test Upload" folder

# Clean up
rm -rf test_upload
```

**Expected:** File appears in your Google Drive

---

## 🔧 Troubleshooting

### ❌ "Required Google API packages not installed"

**Solution:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### ❌ "Credentials file not found"

**Problem:** Missing `client_secrets.json` or `service_account.json`

**Solution:**
1. Check file exists: `ls -la *.json`
2. Verify filename exactly matches
3. Re-download from Google Cloud Console if needed

---

### ❌ "Permission denied" during OAuth

**Solution:**
1. Make sure you added yourself as test user in OAuth consent screen
2. Click "Allow" when browser asks for permissions
3. If stuck, delete `token.json` and try again

---

### ❌ Browser doesn't open (OAuth)

**Possible causes:**
- Running on a server (use Service Account instead)
- Firewall blocking
- Wrong environment

**Solution:**
```bash
# Try Service Account instead
python upload_to_google_drive.py ./folder --auth service_account
```

---

### ❌ "Can't see uploaded files" (Service Account)

**Problem:** Files uploaded to service account's Drive, not yours

**Solution:**
1. Open `service_account.json`
2. Find "client_email" field
3. In Google Drive, share a folder with that email
4. Upload to that shared folder

**Or use OAuth instead:**
```bash
python upload_to_google_drive.py ./folder --auth oauth
```

---

### ❌ "Timeout" or "Connection error"

**Solution:**
- Check internet connection
- Try again (network might be slow)
- Check firewall settings
- Verify Google services are accessible

---

## 📁 Expected File Structure

After complete setup:

```
youtube-playlist/
├── upload_to_google_drive.py          ✅ Created
├── zoom_to_drive.sh                   ✅ Created
├── requirements.txt                   ✅ Updated
├── .gitignore                         ✅ Updated
├── README.md                          ✅ Updated
│
├── QUICKSTART_GOOGLE_DRIVE.md        ✅ Created
├── GOOGLE_DRIVE_AUTH_SETUP.md        ✅ Created
├── AUTH_METHODS_COMPARISON.md        ✅ Created
├── GOOGLE_DRIVE_SUMMARY.md           ✅ Created
│
├── client_secrets.json               ⚠️  YOU need to download this
├── service_account.json              ⚠️  YOU need to download this (optional)
└── token.json                         ⚠️  Auto-created after first OAuth login
```

---

## 🎓 Learning Path

### Beginner: Start Here
1. Read: `QUICKSTART_GOOGLE_DRIVE.md`
2. Setup: OAuth authentication
3. Try: Upload a test folder

### Intermediate: Understand More
1. Read: `AUTH_METHODS_COMPARISON.md`
2. Try: Both OAuth and Service Account
3. Explore: Command line options

### Advanced: Full Features
1. Read: `GOOGLE_DRIVE_SUMMARY.md`
2. Setup: Automated workflows
3. Integrate: Into your own scripts

---

## 🔐 Security Checklist

Before sharing your code or committing to Git:

- [ ] `client_secrets.json` is in `.gitignore`
- [ ] `service_account.json` is in `.gitignore`
- [ ] `token.json` is in `.gitignore`
- [ ] No credentials in code comments
- [ ] No credentials in commit messages
- [ ] No credentials in screenshots

**Check what would be committed:**
```bash
git status
git diff
```

**If you accidentally committed credentials:**
```bash
# Remove from Git history (careful!)
git rm --cached client_secrets.json
git rm --cached service_account.json
git rm --cached token.json
git commit -m "Remove credentials"

# Then regenerate credentials in Google Cloud Console
```

---

## 🚀 You're Ready!

You now have:
- ✅ Complete upload script with progress bars
- ✅ Two authentication methods (OAuth + Service Account)
- ✅ Comprehensive documentation
- ✅ Automated workflow script
- ✅ Security best practices
- ✅ Troubleshooting guides

**Next steps:**
1. Install dependencies (Step 1)
2. Get credentials (Step 2)
3. Try your first upload (Step 3)

**Need help?**
- Quick: `QUICKSTART_GOOGLE_DRIVE.md`
- Auth: `GOOGLE_DRIVE_AUTH_SETUP.md`
- Comparison: `AUTH_METHODS_COMPARISON.md`
- Full docs: `GOOGLE_DRIVE_SUMMARY.md`

---

**Happy uploading! 🎉**

