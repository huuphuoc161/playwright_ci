"""
Comprehensive Login Test Suite
Tests for election app and SauceDemo login scenarios
Results are written to reports/result.txt
"""

import pytest
import os
from pages.election_page import ElectionPage
from pages.login_page import LoginPage


# Test Case 1: Election App - Correct Password
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
    email = os.getenv("TEST_USERNAME")
    wrong_password = os.getenv("TEST_PWD_WRONG", "wrong_password_123")
    
    election_page = ElectionPage(page)
    election_page.goto_base_url()
    assert election_page.verify_login_page(), "Login page not displayed"
    
    election_page.login(email=email, password=wrong_password)
    page.wait_for_timeout(2000)
    
    is_still_login_page = election_page.verify_login_page()
    dashboard_visible = page.locator("//h1[text()='Bầu Cử']").is_visible() if page.locator("//h1[text()='Bầu Cử']") else False
    
    assert is_still_login_page or not dashboard_visible, "Dashboard should not be displayed after wrong password"


# Test Case 3: SauceDemo - Standard User Login
@pytest.mark.saucedemo
@pytest.mark.smoke
def test_saucedemo_login_standard_user(page):
    """SauceDemo login with standard user"""
    login_page = LoginPage(page)
    login_page.login("standard_user", "secret_sauce")
    
    page.wait_for_timeout(1000)
    assert page.url != "https://www.saucedemo.com/", "Should be redirected from login page"


# Test Case 4: SauceDemo - Wrong Credentials
@pytest.mark.saucedemo
def test_saucedemo_login_wrong_credentials(page):
    """SauceDemo login with wrong credentials"""
    login_page = LoginPage(page)
    login_page.goto_base_url()
    
    login_page.username_input.fill("standard_user1")
    login_page.password_input.fill("secret_sauce")
    login_page.login_button.click()
    
    page.wait_for_timeout(1000)
    login_page.verify_login_failed_alert_message()


# Test Case 5: SauceDemo - Locked Out User
@pytest.mark.saucedemo
def test_saucedemo_login_locked_out_user(page):
    """SauceDemo login with locked out user"""
    login_page = LoginPage(page)
    expected_message = "Epic sadface: Sorry, this user has been locked out."
    
    login_page.goto_base_url()
    
    login_page.username_input.fill("locked_out_user")
    login_page.password_input.fill("secret_sauce")
    login_page.login_button.click()
    
    page.wait_for_timeout(1000)
    login_page.verify_login_failed_alert_message()
    login_page.verify_login_failed_content_message(expected_message)
