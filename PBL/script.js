function addToCart(name, price) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  const existingItem = cart.find(item => item.name === name);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({ name, price, quantity: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  showBannerAlert(`${name} added to cart!`);
}

function placeOrder() {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];

  if (cart.length === 0) {
    showBannerAlert("Your cart is empty!", "error");
    return;
  }

  showBannerAlert("Order placed successfully!");
  localStorage.removeItem("cart");
}

function showBannerAlert(message, type = "success") {
  const alertBox = document.getElementById("custom-alert");
  alertBox.textContent = message;
  alertBox.style.display = "block";
  alertBox.style.opacity = "1";

  if (type === "error") {
    alertBox.style.backgroundColor = "#e53935";
    alertBox.style.color = "#fff";
  } else {
    alertBox.style.backgroundColor = "#fbc02d";
    alertBox.style.color = "#000";
  }

  setTimeout(() => {
    alertBox.style.opacity = "0";
  }, 2000);

  setTimeout(() => {
    alertBox.style.display = "none";
    alertBox.style.opacity = "1";
  }, 2500);
}
  
