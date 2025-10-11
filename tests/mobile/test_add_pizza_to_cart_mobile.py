from appium import webdriver

def test_add_pizza_to_cart_mobile():
    caps = {
        "platformName": "Android",
        "app": "path/to/papajohns.apk",
        "deviceName": "Android Emulator"
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    driver.find_element_by_accessibility_id("menu_button").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='Пицца']").click()
    driver.find_element_by_accessibility_id("add_to_cart").click()

    cart_item = driver.find_element_by_accessibility_id("cart_item")
    assert cart_item.is_displayed()

    driver.quit()
