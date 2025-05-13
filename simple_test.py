from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True para no ver el navegador
        page = browser.new_page()
        page.goto("https://operaciones.energiademisiones.com.ar/sist-desp-develop/public/board_despacho")
        print(page.title())
        browser.close()

run()
