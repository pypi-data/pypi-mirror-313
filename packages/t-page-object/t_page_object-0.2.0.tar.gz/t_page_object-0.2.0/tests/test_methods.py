#!/usr/bin/env python
"""Tests for component methods."""
from .t_test_app import TestApp, AlertApp
from t_object import ThoughtfulObject
import os
from time import sleep


class Article(ThoughtfulObject):
    """Article class."""

    title: str = ""
    category: str = ""


class User(ThoughtfulObject):
    """User class."""

    username: str = "test user"
    password: str = "test password"


class TestMethods:
    """Test methods."""

    @classmethod
    def setup_class(self):
        """Setup class."""
        self.remote_url = os.getenv("SELENIUM_GRID_URL")

        # We need this var for bitbucket pipelines sucessfull run
        self.executable_path = os.path.join(os.getcwd(), "chromedriver")
        if not os.path.exists(self.executable_path):
            self.executable_path = None

    def setup_method(self):
        """Setup method."""
        self.app = TestApp()
        self.alert_app = AlertApp()

    def teardown_method(self):
        """Teardown method."""
        self.app.browser.close_browser()

    def test_ui_elements(self):
        """Test UI elements in browser instance."""
        self.app.browser.open_browser(
            browser="chrome",
            url=self.app.ui_test_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.app.ui_test_page.visit()
        self.app.ui_test_page.continue_button.format_xpath(name="Continue")
        self.app.ui_test_page.continue_button.click()
        self.app.ui_test_page.search_button.click()
        self.app.ui_test_page.search_input.input_text_and_check("Robot")
        self.app.ui_test_page.search_go.click()
        self.app.ui_test_page.image.download_image()
        self.app.ui_test_page.article.get_text_values(Article)
        self.app.ui_test_page.section_button.click()
        self.app.ui_test_page.arts_cb.select()
        self.app.ui_test_page.sort_by_dd.click_and_select_option("Sort by Newest")
        assert "newest" == self.app.ui_test_page.sort_by_dd.get_selected_option()

        self.app.select_page.visit()
        self.app.select_page.select_dropdown.click_and_select_option("2")

    def test_table_elements(self):
        """Test Table elements."""
        self.app.browser.open_browser(
            browser="chrome",
            url=self.app.table_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.app.table_page.visit()
        self.app.table_page.table.get_table_data()
        self.app.table_page.table.get_table_data("horizontal")
        self.app.table_page.table.get_summary_table_data()
        self.app.table_page.table_row.get_row_values()

    def test_endpoint_elements(self):
        """Test Endpoint elements."""
        self.app.endpoint_test_page.get_endpoint.get()
        self.app.endpoint_test_page.post_endpoint.post(data={"data": "Test Post Data"})
        self.app.endpoint_test_page.put_endpoint.put(data={"data": "Test Put Data"})
        self.app.endpoint_test_page.delete_endpoint.delete()

    def test_container_element(self):
        """Test container element."""
        self.app.browser.open_browser(
            browser="chrome",
            url=self.app.login_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.app.login_page.visit()
        self.app.login_page.login_container.set_text_values(User())
        assert self.app.login_page.login_container.check_if_all_elements_contain_value()

    def test_alert_popup(self):
        """Test alert popup."""
        self.alert_app.browser.open_browser(
            browser="chrome",
            url=self.alert_app.alert_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.alert_app.alert_page.visit()
        self.alert_app.alert_page.alert_box_button.click()
        self.alert_app.alert_page.confirm_alert_button.click()
        self.alert_app.alert_page.promp_alert_button.click()

    def test_modal(self):
        """Test modal."""
        self.app.browser.open_browser(
            browser="chrome",
            url=self.app.modal_page.url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.app.modal_page.visit()
        self.app.modal_page.modal_button.click()
        sleep(2)
        self.app.modal_page.search_button.click()
