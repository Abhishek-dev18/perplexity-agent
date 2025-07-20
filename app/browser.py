from playwright.sync_api import sync_playwright

QUERY_BOX  = "textarea[data-testid='search-box']"
ANSWER_DIV = "div[data-testid='answer-content']"

def fetch_perplexity_answer(prompt: str, timeout: int = 20000) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page    = browser.new_page()
        page.goto("https://www.perplexity.ai")
        page.fill(QUERY_BOX, prompt)
        page.press(QUERY_BOX, "Enter")
        page.wait_for_selector(ANSWER_DIV, timeout=timeout)
        answer = page.inner_text(ANSWER_DIV)
        browser.close()
        return answer
