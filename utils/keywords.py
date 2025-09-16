import os
from playwright.sync_api import expect


def input_text(page, locator, input_data):
    page.fill(locator, input_data)


def click(page, locator, input_data=None):
    page.click(locator)
    if input_data and input_data.startswith("wait:"):
        success_locator = input_data[len("wait:"):]
        page.wait_for_selector(success_locator, timeout=30000)


def verify_visible(page, locator, input_data=None):
    expect(page.locator(locator)).to_be_visible()


def verify_text(page, locator, input_data):
    actual_text = page.locator(locator).inner_text().strip()
    assert input_data in actual_text, f"Expected '{input_data}' in actual '{actual_text}'"
    expect(page.locator(locator)).to_have_text(input_data)


def upload_resume(page, locator, input_data):
    import os
    file_path = os.path.abspath(input_data)
    with page.expect_file_chooser() as fc_info:
        page.click(locator)
    file_chooser = fc_info.value
    file_chooser.set_files(file_path)


def select_option(page, locator, input_data):
    page.select_option(locator, value=input_data)


KEYWORD_MAP = {
    "InputText": input_text,
    "Click": click,
    "VerifyVisible": verify_visible,
    "VerifyText": verify_text,
    "Upload": upload_resume,
    "SelectOption": select_option,
}
