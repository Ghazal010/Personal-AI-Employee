#!/usr/bin/env python3
"""
LinkedIn Posting Automation for Personal AI Employee

WARNING: This uses LinkedIn automation which may violate LinkedIn Terms of Service.
Use at your own risk. For production, use LinkedIn API with proper authorization.

SETUP REQUIRED:
1. Install Playwright: pip install playwright
2. Install browsers: playwright install chromium
3. First run will require LinkedIn login
4. Session will be saved for future use
"""

import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
APPROVED_PATH = VAULT_PATH / "Approved"
DONE_PATH = VAULT_PATH / "Done"
SESSION_PATH = Path(__file__).parent / "credentials" / "linkedin_session"


def log(message: str):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def extract_post_content(filepath: Path) -> dict:
    """Extract post content from markdown file"""
    content = filepath.read_text()

    # Extract post content between ## Post Content and ---
    start_marker = "## Post Content"
    end_marker = "---"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        return None

    post_text = content[start_idx + len(start_marker):end_idx].strip()

    return {
        'text': post_text,
        'filename': filepath.name
    }


def post_to_linkedin(post_data):
    """Post content to LinkedIn"""
    log(f"Posting to LinkedIn: {post_data['filename']}")

    SESSION_PATH.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_PATH),
                headless=False,  # Set to True after first login
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to LinkedIn
            log("Navigating to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/')

            # Wait for login or feed
            try:
                # Check if already logged in
                page.wait_for_selector('[data-test-id="feed-tab"]', timeout=5000)
                log("Already logged in to LinkedIn")
            except PlaywrightTimeout:
                log("Please log in to LinkedIn")
                log("Waiting for login...")
                page.wait_for_selector('[data-test-id="feed-tab"]', timeout=60000)
                log("Successfully logged in")

            # Click "Start a post" button
            log("Opening post composer...")
            start_post_button = page.query_selector('[data-test-id="share-box-open"]')
            if start_post_button:
                start_post_button.click()
                time.sleep(2)
            else:
                log("ERROR: Could not find 'Start a post' button")
                return False

            # Type post content
            log("Typing post content...")
            editor = page.query_selector('[data-placeholder="What do you want to talk about?"]')
            if editor:
                editor.click()
                editor.type(post_data['text'], delay=50)
                time.sleep(2)
            else:
                log("ERROR: Could not find post editor")
                return False

            # Click Post button
            log("Publishing post...")
            post_button = page.query_selector('[data-test-id="share-actions__primary-action"]')
            if post_button:
                post_button.click()
                time.sleep(3)
                log("✅ Post published successfully!")
                return True
            else:
                log("ERROR: Could not find Post button")
                return False

    except Exception as e:
        log(f"ERROR posting to LinkedIn: {e}")
        return False


def check_and_post():
    """Check for approved LinkedIn posts and publish them"""
    log("Checking for approved LinkedIn posts...")

    # Find approved LinkedIn posts
    approved_posts = list(APPROVED_PATH.glob("LINKEDIN-POST-*.md"))

    if not approved_posts:
        log("No approved LinkedIn posts found")
        return

    log(f"Found {len(approved_posts)} approved posts")

    for post_file in approved_posts:
        log(f"Processing: {post_file.name}")

        # Extract content
        post_data = extract_post_content(post_file)
        if not post_data:
            log(f"ERROR: Could not extract content from {post_file.name}")
            continue

        # Post to LinkedIn
        success = post_to_linkedin(post_data)

        if success:
            # Move to Done
            done_file = DONE_PATH / post_file.name
            post_file.rename(done_file)
            log(f"Moved to Done: {post_file.name}")
        else:
            log(f"Failed to post: {post_file.name}")
            # Leave in Approved for retry


if __name__ == "__main__":
    check_and_post()
