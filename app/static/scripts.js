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
        console.log(data.message); // Выведите сообщение в консоль для отладки
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
      console.log(data.message); // for error logging
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
function increaseQuantity(productID) {
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
    })
    .catch(error => {
        console.error('Error updating quantity:', error.message);
    });
}
function decreaseQuantity(productID) {
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
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error.message);
    });
}




