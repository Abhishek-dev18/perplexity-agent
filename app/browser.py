from playwright.sync_api import sync_playwright
import time

def fetch_perplexity_answer(prompt: str, timeout: int = 30000) -> str:
    """
    Fetch answer from Perplexity using multiple selector strategies
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
            
            # Set longer timeout and user agent
            page.set_default_timeout(timeout)
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            page.goto("https://www.perplexity.ai", wait_until="networkidle")
            
            # Wait a moment for dynamic content to load
            time.sleep(2)
            
            # --- NEW search selector list (July 2025 optimized) -----------------
            search_selectors = [
                "textarea[placeholder*='Ask']",          # primary 2025-07-UI
                "textarea[data-lexical-text='true']",    # lexical editor flag
                "textarea[class*='resize-none']",        # CSS class fallback
                "textarea",                              # generic fallback
                "input[type='text']"                     # legacy fallback
            ]
            # --------------------------------------------------------------------
            
            search_element = None
            for selector in search_selectors:
                try:
                    search_element = page.wait_for_selector(selector, timeout=5000)
                    if search_element:
                        print(f"Found search element with selector: {selector}")
                        break
                except:
                    continue
            
            if not search_element:
                raise Exception("Could not find search input element with any selector")
            
            # Fill the search input
            search_element.fill(prompt)
            
            # Multiple ways to submit the search
            try:
                # Try pressing Enter
                search_element.press("Enter")
            except:
                # Fallback: look for submit button
                submit_selectors = [
                    "button[type='submit']",
                    "button:has-text('Search')",
                    "button:has-text('Ask')", 
                    "[data-testid*='submit']",
                    ".submit-button"
                ]
                
                for selector in submit_selectors:
                    try:
                        page.click(selector)
                        break
                    except:
                        continue
            
            # --- NEW result selector list (July 2025 optimized) ----------------
            result_selectors = [
                "[data-testid*='answer']",
                ".prose.text-pretty",            # new July-2025 container
                ".answer-container",
                "main article",
                "div:has-text('.')"
            ]
            # --------------------------------------------------------------------
            
            result_element = None
            for selector in result_selectors:
                try:
                    result_element = page.wait_for_selector(selector, timeout=10000)
                    if result_element and len(result_element.inner_text().strip()) > 50:
                        print(f"Found result with selector: {selector}")
                        break
                except:
                    continue
            
            if not result_element:
                # Fallback: get all visible text from main content area
                try:
                    result_text = page.evaluate("""
                        () => {
                            const main = document.querySelector('main') || document.body;
                            return main.innerText;
                        }
                    """)
                    return result_text.strip()
                except:
                    raise Exception("Could not extract any results from the page")
            
            answer = result_element.inner_text().strip()
            
            if len(answer) < 10:
                raise Exception("Retrieved answer is too short or empty")
            
            return answer
            
        finally:
            browser.close()

# Alternative simplified version for testing
def fetch_perplexity_simple(prompt: str) -> str:
    """
    Simplified version that just gets page content after search
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        
        try:
            page = browser.new_page()
            
            # Direct search URL approach
            import urllib.parse
            encoded_prompt = urllib.parse.quote(prompt)
            search_url = f"https://www.perplexity.ai/search?q={encoded_prompt}"
            
            page.goto(search_url, wait_until="networkidle")
            time.sleep(5)  # Wait for AI response
            
            # Get all visible text
            content = page.evaluate("() => document.body.innerText")
            
            # Basic cleanup to extract relevant content
            lines = content.split('\n')
            relevant_lines = [line.strip() for line in lines 
                            if len(line.strip()) > 20 and 
                            not line.strip().startswith(('Sign', 'Log', 'Try', 'Upgrade'))]
            
            return '\n'.join(relevant_lines[:10])  # Return first 10 relevant lines
            
        finally:
            browser.close()
