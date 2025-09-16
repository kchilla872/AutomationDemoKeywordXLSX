import os


def save_page_screenshot(page, name):
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    filepath = os.path.join(screenshots_dir, f"{name}.png")
    page.screenshot(path=filepath, full_page=True)
    return filepath
