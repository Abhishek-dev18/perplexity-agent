from playwright.sync_api import sync_playwright
import urllib.parse
import time
import re

def fetch_perplexity_direct(prompt: str, timeout: int = 30000) -> str:
    """
    Fetch answer from Perplexity using direct URL approach (bypassing search input)
    This method is more reliable than trying to find and fill search elements
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, 
            args=[
                "--no-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        try:
            page = browser.new_page()
            
            # Set timeout and user agent
            page.set_default_timeout(timeout)
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            # Encode the prompt for URL
            encoded_prompt = urllib.parse.quote(prompt)
            search_url = f"https://www.perplexity.ai/search?q={encoded_prompt}"
            
            print(f"Navigating to: {search_url}")
            
            # Navigate directly to search results page
            page.goto(search_url, wait_until="networkidle")
            
            # Wait for AI response to generate (this is crucial)
            print("Waiting for AI response to generate...")
            time.sleep(8)  # Give AI time to generate the response
            
            # Try multiple strategies to extract the answer content
            result_selectors = [
                # July 2025 updated selectors
                ".prose.text-pretty",                    # Current answer container
                "[data-testid*='answer']",              # Generic answer testid
                ".answer-container",                     # Generic answer class
                "main article",                          # Semantic HTML
                "[role='main'] div:has-text('.')",      # Main content with text
                "main div:has-text('.')"                # Fallback main content
            ]
            
            answer_text = None
            
            for selector in result_selectors:
                try:
                    element = page.wait_for_selector(selector, timeout=5000)
                    if element:
                        text = element.inner_text().strip()
                        if len(text) > 100:  # Ensure we have substantial content
                            print(f"Found answer with selector: {selector}")
                            answer_text = text
                            break
                except:
                    continue
            
            # Fallback: Extract all visible text and clean it up
            if not answer_text:
                print("Using fallback content extraction...")
                content = page.evaluate("""
                    () => {
                        // Remove navigation, headers, footers, ads
                        const elementsToRemove = [
                            'nav', 'header', 'footer', '.ad', '.ads', 
                            '.navigation', '.menu', '[data-testid*="nav"]',
                            'script', 'style', 'noscript'
                        ];
                        
                        elementsToRemove.forEach(selector => {
                            const elements = document.querySelectorAll(selector);
                            elements.forEach(el => el.remove());
                        });
                        
                        // Get main content area
                        const main = document.querySelector('main') || 
                                   document.querySelector('[role="main"]') || 
                                   document.body;
                        
                        return main.innerText;
                    }
                """)
                
                # Clean up the extracted content
                lines = content.split('\n')
                relevant_lines = []
                
                for line in lines:
                    line = line.strip()
                    # Filter out navigation, UI elements, and very short lines
                    if (len(line) > 20 and 
                        not line.startswith(('Sign', 'Log', 'Try', 'Upgrade', 'Pro', 'Free')) and
                        not re.match(r'^[A-Z][a-z]+$', line) and  # Single words
                        not line.startswith('•') and
                        'perplexity.ai' not in line.lower()):
                        relevant_lines.append(line)
                
                # Take the most relevant content (usually the first substantial paragraphs)
                answer_text = '\n\n'.join(relevant_lines[:10])  # First 10 relevant lines
            
            if not answer_text or len(answer_text.strip()) < 50:
                raise Exception("Could not extract meaningful content from the page")
            
            return answer_text.strip()
            
        finally:
            browser.close()

def fetch_perplexity_answer(prompt: str, timeout: int = 30000) -> str:
    """
    Main function that uses the direct URL approach
    This replaces the old selector-based method
    """
    return fetch_perplexity_direct(prompt, timeout)

# Alternative simplified version for testing
def fetch_perplexity_simple(prompt: str) -> str:
    """
    Ultra-simple version that just gets page content after direct navigation
    Use this if the main function has issues
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        
        try:
            page = browser.new_page()
            
            # Direct search URL approach
            encoded_prompt = urllib.parse.quote(prompt)
            search_url = f"https://www.perplexity.ai/search?q={encoded_prompt}"
            
            page.goto(search_url, wait_until="networkidle")
            time.sleep(10)  # Wait longer for AI response
            
            # Get all visible text
            content = page.evaluate("() => document.body.innerText")
            
            # Basic cleanup to extract relevant content
            lines = content.split('\n')
            relevant_lines = [line.strip() for line in lines 
                            if len(line.strip()) > 30 and 
                            not line.strip().startswith(('Sign', 'Log', 'Try', 'Upgrade', 'Pro', 'Free'))]
            
            return '\n'.join(relevant_lines[:8])  # Return first 8 relevant lines
            
        finally:
            browser.close()
