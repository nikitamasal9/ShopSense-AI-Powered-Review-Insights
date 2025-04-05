document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    
    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-product");

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: new URLSearchParams({ "product_id": productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    document.getElementById("cart-count").innerText = data.cart_count;
                    updateCart();  // Refresh cart items dynamically
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });


    
    const checkoutBtn = document.getElementById("checkoutBtn");
    const successMessage = document.getElementById("successMessage");

    if (checkoutBtn) {
        checkoutBtn.addEventListener("click", function () {
            if (confirm("Are you sure you want to proceed with payment?")) {
                fetch("/checkout/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successMessage.style.display = "block";
                    }
                })
                .catch(error => console.error("Checkout error:", error));
            }
        });
    }


    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
