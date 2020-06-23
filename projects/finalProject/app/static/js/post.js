const addProduct = document.getElementById("new-Product");
const products = document.getElementById("products");
let countProductId = 0;

function newFormRow() {
    let formRow = document.createElement("div");
    formRow.classList.add("form-row");

    return formRow;
}

function newProduct(content, id, type) {
    let formGroup = document.createElement("div");
    formGroup.className = "form-group col-md-6";

    let formGroupLabel = document.createElement("label");
    formGroupLabel.setAttribute("for", content + "_" + id);
    formGroupLabel.textContent = content;

    formGroup.appendChild(formGroupLabel);

    let formGroupInput = document.createElement("input");
    formGroupInput.setAttribute("type", type);
    formGroupInput.classList = "form-control";
    formGroupInput.id = content + "_" + id;

    formGroup.appendChild(formGroupInput);

    return formGroup;
}

addProduct.addEventListener("click", function () {
    formRow = newFormRow();
    formRow.appendChild(newProduct("product", countProductId, "text"))
    formRow.appendChild(newProduct("price", countProductId, "number"))

    countProductId += 1;

    products.appendChild(formRow);
});

function validateForm() {
    if (countProductId == 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No Product has been given'
        });

        return false;
    }

    for (let index = 0; index < countProductId; index++) {
        let product = document.getElementById("product_" + index);
        let price = document.getElementById("price_" + index);

        if (product.value == "") {
            product.focus();

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Please enter product\'s name'
            });
            return false;
        }

        if (price.value == "") {
            price.focus();

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Please enter product\'s price'
            });
            return false;
        }
    }

    return true;
}

function createShoppingObject() {
    let shopping = {
        products: [],
        count: countProductId,
        author: document.getElementById("staticUser").value,
    }

    let totoalPrice = 0;
    for (let index = 0; index < countProductId; index++) {
        let product = document.getElementById("product_" + index);
        let price = document.getElementById("price_" + index);

        let newItem = {
            product: product.value,
            price: parseInt(price.value),
        }

        shopping.products.push(newItem)

        totoalPrice += parseInt(price.value);
    }

    shopping["total"] = totoalPrice;

    return shopping;
}

function restartShopping() {
    countProductId = 0;

    for (const child of Array.from(products.children)) {
        if (child.className === "form-row") {
            child.remove();
        }
    }
}

products.addEventListener("submit", e => {
    e.preventDefault();

    const endpoint = `${window.origin}/admin/postShopping`;

    if (!validateForm()) {
        return false;
    }

    fetch(endpoint, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(createShoppingObject()),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => {
        response.json().then((data) => {
            if (data["status"] == 400) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Sale wans\'t correctly registered'
                });

                return;
            }

            restartShopping();

            Swal.fire({
                icon: 'success',
                title: 'Successful Sale',
                text: 'Sale was correctly registered'
            });

        })
    });
})
