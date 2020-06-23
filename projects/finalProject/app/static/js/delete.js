const sellersList = document.getElementById("sellers");

function requestDeletUser(email, parent) {
    const endpoint = `${window.origin}/deleteAuser`;

    fetch(endpoint, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
            "email" : email
        }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => {
        if (response.status == 200) {
            Swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: 'User has been deleted from Blockchain'
            });
            parent.remove();
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'User couldn\t be deleted'
            });
        }
    });
}

function deleteUser() {
    const email = this.getAttribute("email");
    console.log(email);
    Swal.fire({
        title: 'Are you sure to delete this user?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.value) {
            requestDeletUser(email, this.parentNode)
        }
    })
}

function createNewCardLiElement(userName, email) {
    let liElement = document.createElement("li");
    liElement.classList.add("list-group-item");
    let p = document.createElement("p");
    p.textContent = userName;
    p.classList.add("userName");
    liElement.appendChild(p);
    p = document.createElement("p");
    p.textContent = email;
    liElement.appendChild(p);

    let deleteButtton = document.createElement("button");
    deleteButtton.className = "btn btn-danger float-right"
    deleteButtton.textContent = "Delete User"
    deleteButtton.setAttribute("email", email);
    deleteButtton.addEventListener("click", deleteUser);


    liElement.appendChild(deleteButtton);

    sellersList.appendChild(liElement);
}


document.addEventListener("DOMContentLoaded", function() {
    const endpoint = `${window.origin}/getSellers`;

    fetch(endpoint, {
        method: "GET",
        credentials: "include"
    }).then((response) => {
        response.json().then((data) => {
            for(const user of data.users){
                createNewCardLiElement(user.name, user.email)
            }
        })
    });
})
