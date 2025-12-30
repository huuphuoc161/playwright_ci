import pytest
import os
from pages.election_page import ElectionPage
from pages.login_page import LoginPage


#Test Case 1: Election App - Correct Password
@pytest.mark.election_app
@pytest.mark.smoke
def test_election_app_login_correct_password(page):
    """Election app login with correct credentials from .env"""
    email = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PWD")
    
    election_page = ElectionPage(page)
    election_page.goto_base_url()
    assert election_page.verify_login_page(), "Login page not displayed"
    
    election_page.login(email=email, password=password)
    page.wait_for_timeout(3000)
    
    assert election_page.verify_login_successful(), "Dashboard not displayed after login"

    # Test Case 2: Election App - Wrong Password
@pytest.mark.election_app
def test_election_app_login_wrong_password(page):
    """Election app login with wrong password"""
    email = "test@wrong.pass"
    wrong_password = os.getenv("TEST_PWD_WRONG", "wrong_password_123")
    
    election_page = ElectionPage(page)
    election_page.goto_base_url()
    assert election_page.verify_login_page(), "Login page not displayed"
    
    election_page.login(email=email, password=wrong_password)
    page.wait_for_timeout(2000)
    
    is_still_login_page = election_page.verify_login_page()
    dashboard_visible = page.locator("//h1[text()='Bầu Cử']").is_visible() if page.locator("//h1[text()='Bầu Cử']") else False
    
    assert is_still_login_page or not dashboard_visible, "Dashboard should not be displayed after wrong password"