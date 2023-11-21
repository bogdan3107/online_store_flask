function updateCartCountInLocalStorage(count) {
    localStorage.setItem('cartCount', count);
}

function getCartCountFromLocalStorage() {
    return localStorage.getItem('cartCount');
}

document.addEventListener('DOMContentLoaded', function() {
    var savedCount = getCartCountFromLocalStorage();
    var isCartPage = document.getElementById('totalPay') !== null;
    if (savedCount > 0) {
        document.getElementById(`productCount`).innerText = savedCount;
    }
    if (isCartPage) {
        updateTotalPay();
    }
});

function updateCartCount(count) {
    document.getElementById('productCount').innerText = count;
}

function clearCart() {
    localStorage.setItem('cartCount', 0);
}

function updateTotalPay() {
    var totalPay = 0;

    document.querySelectorAll('.card').forEach(function(cardElement) {
        if (window.getComputedStyle(cardElement).getPropertyValue('display') !== 'none') {
            var priceElement = cardElement.querySelector('.card-title + span');

            if (priceElement) {
                totalPay += parseFloat(priceElement.textContent.replace('Price: ', '').replace(' USD', ''));
            }
        }
    });

    document.getElementById('totalPay').textContent = 'Total to pay: ' + totalPay.toFixed(2) + ' USD';
}

function addToCart(productId) {
    fetch('/add_to_cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'product_id': productId }),
    })
    .then(response => {
      if (!response.ok) {
        if (response.status === 401) {
            var responseHtmlContent = "<div class='alert alert-warning' role='alert'>Please log in!</div>";
            document.getElementById('loginRequired').innerHTML = responseHtmlContent;
        }
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
        console.log(data.message);
        var totalItemsInCart = data.cart_count;
        var productCountElement = document.getElementById('productCount');
        updateCartCount(totalItemsInCart);
        updateCartCountInLocalStorage(totalItemsInCart);
        
        if (totalItemsInCart > 0) {
            productCountElement.style.display = 'inline';
            document.getElementById(`productCount`).innerText = totalItemsInCart;
        } else {
            productCountElement.style.display = 'none';
        }
    })
    
    .catch(error => {
      console.error('Fetch Error:', error.message);
    });
  }

function removeFromCart(productID) {
    fetch('/remove_from_cart',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'product_id': productID }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok!');
      }
      return response.json();
    })
    .then(data => {
        console.log(data.message);
        var updatedItemCount = data.item_counts[productID];
        var cartProductID = document.getElementById(`cartProductID_${productID}`);
        var totalItemsInCart = data.cart_count;
        var productCountElement = document.getElementById('productCount');

        document.getElementById(`productCount`).innerText = totalItemsInCart;

        updateCartCountInLocalStorage(totalItemsInCart);

        if (totalItemsInCart > 0) {
            productCountElement.style.display = 'inline';
            document.getElementById(`productCount`).innerText = totalItemsInCart;
        } else {
            productCountElement.style.display = 'none';
        }

        if(updatedItemCount === undefined) {
            cartProductID.style.display = 'none';
            updateTotalPay();
            console.log('total pay after removing:', totalPay);
        } else {
            document.getElementById(`quantityDisplay_${productID}`).innerText = updatedItemCount;
        }
    })
    .catch(error => {
      console.error('Fetch error:', error.message);
    });
  }

function increaseQuantity(element) {
    var productID = element.getAttribute('data-product-id');
    var productPrice = element.getAttribute('data-product-price');
    fetch('/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'product_id': productID, 'action': 'increase' }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok!');
        }
        return response.json();
    })
    .then(data => {
        var updatedItemCount = data.item_counts[productID];
        document.getElementById(`quantityDisplay_${productID}`).innerText = updatedItemCount;
        var itemInCartPrice = "Price: " + (productPrice * updatedItemCount).toFixed(2) + " USD";
        document.getElementById(`priceDisplay_${productID}`).innerText = itemInCartPrice;
        var decreaseButton = document.getElementById(`decreaseButton_${productID}`);
        if (updatedItemCount > 1) {
            decreaseButton.disabled = false
        }

        updateTotalPay();
        
    })
    .catch(error => {
        console.error('Error updating quantity:', error.message);
    });
}

function decreaseQuantity(element) {
    var productID = element.getAttribute('data-product-id');
    var productPrice = element.getAttribute('data-product-price');

    fetch('/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'product_id': productID, 'action': 'decrease' }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok!');
        }
        return response.json();
    })
    .then(data => {
        var updatedItemCount = data.item_counts[productID];
        var cartProductID = document.getElementById(`cartProductID_${productID}`);
        var decreaseButton = document.getElementById(`decreaseButton_${productID}`);

        if(updatedItemCount === undefined) {
            cartProductID.style.display = 'none'
        } else {
            document.getElementById(`quantityDisplay_${productID}`).innerText = updatedItemCount;
            var itemInCartPrice = "Price: " + (productPrice * updatedItemCount).toFixed(2) + " USD";
            document.getElementById(`priceDisplay_${productID}`).innerText = itemInCartPrice;
            decreaseButton.disabled = (updatedItemCount === 1);
        }

        updateTotalPay();
    })
    .catch(error => {
        console.error('Error updating quantity:', error.message);
    });
}




