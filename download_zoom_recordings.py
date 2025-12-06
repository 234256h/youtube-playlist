#!/usr/bin/env python3
"""
Zoom Recording Downloader
Downloads all files from a Zoom recording URL with password support.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from urllib.parse import urlparse, urljoin
import time

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    from tqdm import tqdm
except ImportError as e:
    print(f"Error: Missing required dependency - {e}")
    print("\nPlease install dependencies:")
    print("  pip install -r requirements.txt")
    print("  playwright install chromium")
    sys.exit(1)


def sanitize_filename(filename):
    """Remove invalid characters from filename/folder name."""
    # Remove or replace invalid characters for filesystem
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length to avoid filesystem issues
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized if sanitized else "zoom_recording"


def get_meeting_title(page):
    """Extract meeting title from the Zoom recording page."""
    try:
        # Try different selectors for meeting title
        selectors = [
            'h1.meeting-topic',
            '.meeting-topic',
            'h1',
            '.topic',
            '[class*="topic"]',
            '[class*="title"]'
        ]
        
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    title = element.inner_text().strip()
                    if title and len(title) > 3:
                        return title
            except:
                continue
        
        # Fallback: use page title
        title = page.title()
        if title and title != "Zoom":
            return title
            
        return "zoom_recording"
    except Exception as e:
        print(f"Warning: Could not extract meeting title: {e}")
        return "zoom_recording"


def check_and_handle_password(page):
    """Check if password is required and handle authentication."""
    try:
        # Wait a bit for page to load
        page.wait_for_load_state('networkidle', timeout=10000)
        
        # Check for password input field
        password_selectors = [
            'input[type="password"]',
            'input#password',
            'input[name="password"]',
            '.password-input'
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    password_input = element
                    break
            except:
                continue
        
        if password_input:
            print("\n🔒 Password required for this recording.")
            password = input("Please enter the password: ").strip()
            
            if not password:
                print("Error: Password cannot be empty.")
                return False
            
            # Fill password
            password_input.fill(password)
            
            # Find and click submit button
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Submit")',
                'button:has-text("Continue")',
                'input[type="submit"]',
                '.submit-btn'
            ]
            
            for selector in submit_selectors:
                try:
                    button = page.locator(selector).first
                    if button.is_visible(timeout=2000):
                        button.click()
                        break
                except:
                    continue
            
            # Wait for page to load after authentication
            print("Authenticating...")
            time.sleep(2)  # Give it a moment to process
            page.wait_for_load_state('networkidle', timeout=15000)
            
            # Check if still on password page (wrong password)
            # Look for error messages or if password field is still prominently displayed
            try:
                # Check for error message
                error_selectors = [
                    '.error-message',
                    '[class*="error"]',
                    '[class*="invalid"]',
                    'text="Incorrect password"',
                    'text="Invalid password"'
                ]
                for selector in error_selectors:
                    try:
                        error = page.locator(selector).first
                        if error.is_visible(timeout=1000):
                            print("Error: Incorrect password.")
                            return False
                    except:
                        continue
                
                # If password field is still there and form didn't submit, likely wrong password
                password_field = page.locator('input[type="password"]').first
                if password_field.is_visible(timeout=2000):
                    # Check if it's empty (form was submitted and reloaded with error)
                    value = password_field.input_value()
                    if not value:  # Field was cleared, means error
                        print("Error: Incorrect password or authentication failed.")
                        return False
            except:
                pass  # Password field not visible anymore, good!
            
            print("✓ Authentication successful!")
            return True
        
        # No password required
        return True
        
    except PlaywrightTimeoutError:
        print("Warning: Timeout waiting for page to load")
        return True  # Continue anyway
    except Exception as e:
        print(f"Warning during password check: {e}")
        return True  # Continue anyway


def find_download_links(page):
    """Find all download links on the page."""
    download_links = []
    
    try:
        # Wait for content to load
        page.wait_for_load_state('networkidle', timeout=10000)
        
        # Common selectors for Zoom download buttons/links
        download_selectors = [
            'a[download]',
            'a[href*="download"]',
            'button:has-text("Download")',
            '.download-btn',
            '[class*="download"]',
            'a[href$=".mp4"]',
            'a[href$=".m4a"]',
            'a[href$=".vtt"]',
            'a[href$=".txt"]'
        ]
        
        seen_urls = set()
        
        for selector in download_selectors:
            try:
                elements = page.locator(selector).all()
                for element in elements:
                    try:
                        if not element.is_visible():
                            continue
                        
                        # Get href or onclick download URL
                        href = element.get_attribute('href')
                        if href and href not in seen_urls:
                            # Make absolute URL
                            absolute_url = urljoin(page.url, href)
                            
                            # Get filename from download attribute or URL
                            filename = element.get_attribute('download')
                            if not filename:
                                filename = os.path.basename(urlparse(absolute_url).path)
                            
                            # Get file type from text content if available
                            text = element.inner_text().strip()
                            
                            download_links.append({
                                'url': absolute_url,
                                'filename': filename,
                                'type': text if text else filename
                            })
                            seen_urls.add(href)
                    except:
                        continue
            except:
                continue
        
        return download_links
        
    except Exception as e:
        print(f"Error finding download links: {e}")
        return []


def download_file(url, filepath, description="Downloading"):
    """Download a file with progress bar."""
    import requests
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
                return True
            
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=description) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        return True
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Download all files from a Zoom recording URL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://zoom.us/rec/share/xxxxx
  %(prog)s "https://zoom.us/rec/play/xxxxx"
        """
    )
    parser.add_argument('url', help='Zoom recording URL')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode (default: True)')
    parser.add_argument('--visible', action='store_true',
                       help='Show browser window (opposite of headless)')
    
    args = parser.parse_args()
    
    zoom_url = args.url.strip()
    headless = not args.visible if args.visible else args.headless
    
    # Validate URL
    if not zoom_url.startswith('http'):
        print(f"Error: Invalid URL. Must start with http:// or https://")
        sys.exit(1)
    
    if 'zoom.us' not in zoom_url.lower():
        print(f"Warning: URL doesn't appear to be a Zoom link")
    
    print(f"🎥 Zoom Recording Downloader")
    print(f"📍 URL: {zoom_url}\n")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            print("🚀 Starting browser...")
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # Navigate to URL
            print(f"📂 Loading recording page...")
            page.goto(zoom_url, wait_until='domcontentloaded', timeout=30000)
            
            # Handle password if needed
            if not check_and_handle_password(page):
                print("\n❌ Failed to authenticate. Exiting.")
                browser.close()
                sys.exit(1)
            
            # Get meeting title
            print("\n📝 Extracting meeting information...")
            meeting_title = get_meeting_title(page)
            folder_name = sanitize_filename(meeting_title)
            print(f"Meeting: {meeting_title}")
            
            # Create downloads directory structure: downloads/meeting_name/
            downloads_base = Path("downloads")
            downloads_base.mkdir(exist_ok=True)
            download_folder = downloads_base / folder_name
            download_folder.mkdir(exist_ok=True)
            print(f"📁 Download folder: {download_folder.absolute()}")
            
            # Find all download links
            print("\n🔍 Finding downloadable files...")
            download_links = find_download_links(page)
            
            if not download_links:
                print("\n⚠️  No download links found on the page.")
                print("\nPossible reasons:")
                print("  • Download is disabled by the host/administrator")
                print("  • Recording is view-only (streaming only)")
                print("  • You may need to log in with your Zoom account (not just meeting password)")
                print("  • The page structure is different than expected")
                print("\n💡 Troubleshooting:")
                print("  1. Open the URL in a regular browser")
                print("  2. Check if you can see any 'Download' buttons")
                print("  3. Try running with --visible to see what the script sees:")
                print(f"     python download_zoom_recordings.py \"{zoom_url}\" --visible")
                browser.close()
                sys.exit(1)
            
            print(f"✓ Found {len(download_links)} file(s) to download\n")
            
            # Download each file
            successful = 0
            failed = 0
            
            for i, link in enumerate(download_links, 1):
                filename = sanitize_filename(link['filename'])
                if not filename:
                    filename = f"file_{i}"
                
                filepath = download_folder / filename
                file_type = link['type'][:50] if link['type'] else filename
                
                print(f"\n[{i}/{len(download_links)}] {file_type}")
                print(f"  → {filename}")
                
                if download_file(link['url'], filepath, description=f"  Downloading"):
                    print(f"  ✓ Saved to {filepath}")
                    successful += 1
                else:
                    print(f"  ✗ Failed to download")
                    failed += 1
            
            browser.close()
            
            # Summary
            print("\n" + "="*60)
            print(f"📊 Download Summary:")
            print(f"  ✓ Successful: {successful}")
            if failed > 0:
                print(f"  ✗ Failed: {failed}")
            print(f"  📁 Location: {download_folder.absolute()}")
            print("="*60)
            
            if failed > 0:
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user.")
        sys.exit(130)
    except PlaywrightTimeoutError:
        print("\n❌ Error: Timeout loading page. Please check the URL and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

