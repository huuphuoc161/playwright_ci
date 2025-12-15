from playwright.sync_api import Page, expect, ElementHandle
from pages.base_page import Base

class ElectionPage(Base):
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "https://election-ht.vercel.app/"

    @property
    def email_input(self) -> ElementHandle:
        return self.page.locator("//input[@id='email']")

    @property
    def password_input(self) -> ElementHandle:
        return self.page.locator("//input[@id='password']")

    @property
    def login_button(self) -> ElementHandle:
        return self.page.locator("//button[@type='submit']")

    @property
    def dashboard_header(self) -> ElementHandle:
        return self.page.locator("//h1[text()='Bầu Cử']")

    def goto_base_url(self):
        self.page.goto(self.base_url)

    def verify_login_page(self):
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        return True

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def verify_login_successful(self):
        """Verify user is logged in by checking dashboard is visible"""
        expect(self.dashboard_header).to_be_visible()
        return True
