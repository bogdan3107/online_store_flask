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
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
        console.log(data.message);
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

        if(updatedItemCount === undefined) {
            cartProductID.style.display = 'none'
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

        if(updatedItemCount === undefined) {
            cartProductID.style.display = 'none'
        } else {
            document.getElementById(`quantityDisplay_${productID}`).innerText = updatedItemCount;
            var itemInCartPrice = "Price: " + (productPrice * updatedItemCount).toFixed(2) + " USD";
            document.getElementById(`priceDisplay_${productID}`).innerText = itemInCartPrice;
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error.message);
    });
}




