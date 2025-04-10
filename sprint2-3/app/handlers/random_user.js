document.getElementById("generateUser").addEventListener("click", () => {
    $.ajax({
        url: "https://randomuser.me/api/",
        dataType: "json",
        success: function(data) {
            const user = data.results[0];
            document.getElementById("name").textContent = `${user.name.first} ${user.name.last}`;
            document.getElementById("email").textContent = user.email;
            document.getElementById("phone").textContent = user.phone;
            document.getElementById("picture").src = user.picture.large;
            document.getElementById("naturalness").textContent = user.nat;
            document.getElementById("age").textContent = user.registered.age;
            document.getElementById("birthdate").textContent = user.registered.date;
        },
        error: function(error) {
            console.error("Error getting random user:", error);
        }
    });
});
