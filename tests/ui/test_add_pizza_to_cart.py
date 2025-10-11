from selene import browser, be, have

def test_add_pizza_to_cart():
    browser.open('https://papajohns.ru')
    browser.element('[data-testid="menu-link"]').click()
    browser.element('[data-testid="product-card"]').click()
    browser.element('[data-testid="add-to-cart-button"]').click()
    browser.element('[data-testid="cart-link"]').click()
    browser.element('[data-testid="cart-item"]').should(be.visible)
    browser.element('[data-testid="cart-total"]').should(have.text('₽'))
