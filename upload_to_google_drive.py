#!/usr/bin/env python3
"""
Google Drive Folder Upload Script

This script uploads a local folder with all its files to Google Drive.
Supports multiple authentication methods:
1. OAuth 2.0 (User authentication - recommended for personal use)
2. Service Account (Server-to-server - recommended for automation)

Author: Generated script
Date: December 2025
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional, List, Dict
import mimetypes

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Error: Required Google API packages not installed.")
    print("\nPlease install dependencies:")
    print("  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("⚠️  Warning: tqdm not installed. Progress bars will be disabled.")
    tqdm = None


# If modifying these scopes, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveUploader:
    """Handles uploading files to Google Drive with different authentication methods."""
    
    def __init__(self, auth_method: str = 'oauth', credentials_file: str = None, token_file: str = 'token.json'):
        """
        Initialize the uploader.
        
        Args:
            auth_method: 'oauth' or 'service_account'
            credentials_file: Path to credentials file
                - For OAuth: path to client_secrets.json (download from Google Cloud Console)
                - For Service Account: path to service account JSON key
            token_file: Path to store OAuth token (only used for OAuth method)
        """
        self.auth_method = auth_method
        self.credentials_file = credentials_file or self._get_default_credentials_file(auth_method)
        self.token_file = token_file
        self.service = None
        
    def _get_default_credentials_file(self, auth_method: str) -> str:
        """Get default credentials file name based on auth method."""
        if auth_method == 'oauth':
            return 'client_secrets.json'
        else:
            return 'service_account.json'
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Drive API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if self.auth_method == 'oauth':
                return self._authenticate_oauth()
            elif self.auth_method == 'service_account':
                return self._authenticate_service_account()
            else:
                print(f"❌ Error: Unknown authentication method '{self.auth_method}'")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def _authenticate_oauth(self) -> bool:
        """Authenticate using OAuth 2.0 (user authentication)."""
        creds = None
        
        # Check if we have a saved token
        if os.path.exists(self.token_file):
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            except Exception as e:
                print(f"⚠️  Warning: Could not load token file: {e}")
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️  Could not refresh token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Error: Credentials file not found: {self.credentials_file}")
                    print("\n📋 To use OAuth authentication:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create or select a project")
                    print("3. Enable the Google Drive API")
                    print("4. Create OAuth 2.0 credentials (Desktop app)")
                    print(f"5. Download the JSON file and save it as '{self.credentials_file}'")
                    return False
                
                print("🔐 Starting OAuth authentication flow...")
                print("Your browser will open for authentication.")
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"✅ Credentials saved to {self.token_file}")
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ OAuth authentication successful")
        return True
    
    def _authenticate_service_account(self) -> bool:
        """Authenticate using a Service Account."""
        if not os.path.exists(self.credentials_file):
            print(f"❌ Error: Service account file not found: {self.credentials_file}")
            print("\n📋 To use Service Account authentication:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create or select a project")
            print("3. Enable the Google Drive API")
            print("4. Create a Service Account")
            print("5. Create and download a JSON key for the service account")
            print(f"6. Save the JSON file as '{self.credentials_file}'")
            print("\n⚠️  Note: Files will be uploaded to the service account's Drive.")
            print("   To upload to your personal Drive, share a folder with the service account email.")
            return False
        
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES)
            self.service = build('drive', 'v3', credentials=creds)
            print("✅ Service Account authentication successful")
            return True
        except Exception as e:
            print(f"❌ Error loading service account credentials: {e}")
            return False
    
    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Create a folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_id: ID of the parent folder (None for root)
            
        Returns:
            Folder ID if successful, None otherwise
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name, webViewLink'
            ).execute()
            
            print(f"📁 Created folder: {folder_name}")
            print(f"   ID: {folder.get('id')}")
            print(f"   Link: {folder.get('webViewLink')}")
            
            return folder.get('id')
        except HttpError as error:
            print(f"❌ Error creating folder: {error}")
            return None
    
    def find_folder_by_name(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Find a folder by name in Google Drive.
        
        Args:
            folder_name: Name of the folder to find
            parent_id: ID of the parent folder (None for root)
            
        Returns:
            Folder ID if found, None otherwise
        """
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            return None
        except HttpError as error:
            print(f"❌ Error searching for folder: {error}")
            return None
    
    def upload_file(self, file_path: str, parent_id: Optional[str] = None, show_progress: bool = True) -> Optional[str]:
        """
        Upload a file to Google Drive.
        
        Args:
            file_path: Path to the local file
            parent_id: ID of the parent folder (None for root)
            show_progress: Whether to show progress bar
            
        Returns:
            File ID if successful, None otherwise
        """
        try:
            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            file_metadata = {'name': file_name}
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            request = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            )
            
            file_size = os.path.getsize(file_path)
            
            # Upload with progress
            response = None
            if show_progress and tqdm:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as pbar:
                    while response is None:
                        status, response = request.next_chunk()
                        if status:
                            pbar.update(status.resumable_progress - pbar.n)
            else:
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        print(f"   Uploading {file_name}: {progress}%", end='\r')
                print()  # New line after upload
            
            print(f"✅ Uploaded: {file_name}")
            return response.get('id')
            
        except HttpError as error:
            print(f"❌ Error uploading {file_path}: {error}")
            return None
    
    def upload_folder(self, local_folder: str, drive_folder_name: Optional[str] = None,
                     parent_id: Optional[str] = None, create_if_not_exists: bool = True) -> Dict[str, int]:
        """
        Upload a local folder and all its contents to Google Drive.
        
        Args:
            local_folder: Path to the local folder
            drive_folder_name: Name for the folder in Google Drive (defaults to local folder name)
            parent_id: ID of the parent folder in Drive (None for root)
            create_if_not_exists: Whether to create the folder if it doesn't exist
            
        Returns:
            Dictionary with upload statistics
        """
        local_path = Path(local_folder)
        if not local_path.exists() or not local_path.is_dir():
            print(f"❌ Error: Local folder not found or not a directory: {local_folder}")
            return {'success': 0, 'failed': 0}
        
        # Use local folder name if drive folder name not specified
        if drive_folder_name is None:
            drive_folder_name = local_path.name
        
        print(f"\n📤 Starting upload: {local_folder} -> {drive_folder_name}")
        
        # Find or create the target folder
        folder_id = self.find_folder_by_name(drive_folder_name, parent_id)
        
        if not folder_id and create_if_not_exists:
            folder_id = self.create_folder(drive_folder_name, parent_id)
        elif not folder_id:
            print(f"❌ Error: Folder '{drive_folder_name}' not found in Drive")
            return {'success': 0, 'failed': 0}
        
        if not folder_id:
            return {'success': 0, 'failed': 0}
        
        # Get all files in the folder (non-recursive for now)
        files_to_upload = [f for f in local_path.iterdir() if f.is_file()]
        
        print(f"\n📊 Found {len(files_to_upload)} file(s) to upload")
        
        stats = {'success': 0, 'failed': 0}
        
        for file_path in files_to_upload:
            file_id = self.upload_file(str(file_path), folder_id)
            if file_id:
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        print(f"\n📈 Upload complete:")
        print(f"   ✅ Success: {stats['success']}")
        print(f"   ❌ Failed: {stats['failed']}")
        
        return stats


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Upload a folder to Google Drive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Authentication Methods:
  oauth (default):      Uses OAuth 2.0 - opens browser for user authentication
                        Requires: client_secrets.json from Google Cloud Console
                        Best for: Personal use, interactive sessions
  
  service_account:      Uses Service Account - no user interaction needed
                        Requires: service_account.json from Google Cloud Console
                        Best for: Automation, server environments
                        Note: Uploads to service account's Drive by default

Examples:
  # Upload with OAuth (default)
  python upload_to_google_drive.py ./downloads/my_folder

  # Upload with custom Google Drive folder name
  python upload_to_google_drive.py ./downloads/my_folder --drive-folder "My Recordings"

  # Upload with Service Account
  python upload_to_google_drive.py ./downloads/my_folder --auth service_account

  # Upload with custom credentials file
  python upload_to_google_drive.py ./downloads/my_folder --credentials my_creds.json

Setup Instructions:
  1. Go to https://console.cloud.google.com/
  2. Create a new project or select existing
  3. Enable the Google Drive API
  4. Create credentials:
     - For OAuth: Create "OAuth client ID" (Desktop app)
     - For Service Account: Create "Service Account" and download JSON key
  5. Download the credentials JSON file
  6. Save as client_secrets.json (OAuth) or service_account.json (Service Account)
        """
    )
    
    parser.add_argument('folder', help='Path to the local folder to upload')
    parser.add_argument('--drive-folder', '-d', help='Name for the folder in Google Drive (defaults to local folder name)')
    parser.add_argument('--auth', '-a', choices=['oauth', 'service_account'], default='oauth',
                       help='Authentication method (default: oauth)')
    parser.add_argument('--credentials', '-c', help='Path to credentials file (default: client_secrets.json or service_account.json)')
    parser.add_argument('--token', '-t', default='token.json',
                       help='Path to OAuth token file (default: token.json, only used for OAuth)')
    parser.add_argument('--no-progress', action='store_true', help='Disable progress bars')
    
    args = parser.parse_args()
    
    # Create uploader
    uploader = GoogleDriveUploader(
        auth_method=args.auth,
        credentials_file=args.credentials,
        token_file=args.token
    )
    
    # Authenticate
    if not uploader.authenticate():
        print("\n❌ Authentication failed. Cannot proceed with upload.")
        sys.exit(1)
    
    # Upload folder
    stats = uploader.upload_folder(
        local_folder=args.folder,
        drive_folder_name=args.drive_folder
    )
    
    # Exit with appropriate code
    if stats['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

