from playwright.sync_api import sync_playwright
from colorama import init, Fore, Style

init(autoreset=True)

valid_credentials = [
    ("standard_user", "secret_sauce","visible"),
    ("problem_user", "secret_sauce","visible"),
    ("performance_glitch_user", "secret_sauce","visible"),
    ("visual_user", "secret_sauce","visible"),
    ("error_user", "secret_sauce","visible"),
]

error_credentials = [
    ("locked_out_user", "secret_sauce","no visible")        
]

invalid_credentials = [
    ("unknown_user", "secret_sauce","no visible"),          
    ("visual_user", "123456","no visible"),                 
    ("hacker", "hack123","no visible"),                     
]

def run_test(playwright, username, password, visible):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")

    page.fill("[data-test=\"username\"]", username)
    page.fill("[data-test=\"password\"]", password)
    page.click("[data-test=\"login-button\"]")

    print(f"Usuario: {username}, Contraseña: {password}")

    try:
        header = page.locator(".header_secondary_container")
        assert header.is_visible(), "Encabezado no se ve."
        if visible=="visible":
            print(Fore.GREEN + "PASS: Login exitoso")
    except Exception as e:
        if visible == "no visible":
            print(Fore.YELLOW + "PASS: Login fallido esperado")
        else:
            print(Fore.RED + f"FAIL: {e}")

    # Limpieza
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        for group_name, creds in [
            ("Valid: éxito esperado", valid_credentials),
            ("Error: login fallido esperado", error_credentials),
            ("Invalid: datos totalmente inválidos", invalid_credentials),
        ]:
            print(f"\n=== Probando grupo '{group_name}' ===")
            for user, pwd, visible in creds:
                run_test(pw, user, pwd, visible)
