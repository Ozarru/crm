console.log("hello cart");

function update_cart(obj_id, action) {
  // alert('mod')
  const csrfToken = document.getElementById("csrf_token").value;

  $.ajax({
    type: "POST",
    url: `${action}/`,
    data: {
      product_id: obj_id,
      csrfmiddlewaretoken: csrfToken,
      action: "post",
    },
    success: function (json) {
      let counter_span = document.getElementById("cart_counter");
      counter_span.textContent = json.cart_count;

      // Convert cart_count to an integer and check the condition
      if (parseInt(json.cart_count) > 0) {
        counter_span.classList.remove("bg-gray-200");
        counter_span.classList.add("bg-yellow-400");
      } else {
        counter_span.classList.remove("bg-yellow-400");
        counter_span.classList.add("bg-gray-200");
      }

      // Reload the cart content
      $("#cart").load(location.href + " #cart");
    },
    error: function (xhr, errmsg, err) {
      console.error(errmsg);
    },
  });
}

// add to cart button ----------------------------------------------------------------------------------------------------
// function add_to_cart(obj_id) {
//   // alert('added')
//   // Retrieve the CSRF token from the hidden input
//   const csrfToken = document.getElementById("csrf_token").value;
//   $.ajax({
//     type: "POST",
//     url: "{% url 'add_to_cart' %}",
//     data: {
//       product_id: obj_id,
//       csrfmiddlewaretoken: csrfToken,
//       action: "post",
//     },
//     success: function (json) {
//       let counter_span = document.getElementById("cart_counter");
//       counter_span.textContent = json.cart_count;

//       // Convert cart_count to an integer and check the condition
//       if (parseInt(json.cart_count) > 0) {
//         counter_span.classList.remove("bg-gray-200");
//         counter_span.classList.add("bg-yellow-400");
//       } else {
//         counter_span.classList.remove("bg-yellow-400");
//         counter_span.classList.add("bg-gray-200");
//       }
//     },
//     error: function (xhr, errmsg, err) {
//       console.error(errmsg); // Log error message to console
//     },
//   });
// }

//   checkout button ----------------------------------------------------------------------------------------------------
    document.getElementById("checkout_btn").addEventListener("click", function (event) {
        const clientSelect = document.querySelector("select[name='client_id']");
        const selectedClient = clientSelect.value;

        if (!selectedClient) {
            alert('Please select a client before proceeding with the checkout.');
            event.preventDefault(); // Prevent form submission
        } else {
            document.getElementById("client_selector").submit(); // Submit the form if a client is selected
        }
    });
