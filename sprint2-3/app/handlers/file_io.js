document.addEventListener("DOMContentLoaded", function () {

    // get form from html
    const form = document.getElementById("uploadForm");

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            // create the form data based on $form
            const formData = new FormData(form);
            const errorParagraph = document.getElementById("upload-error");

            try {
                const response = await fetch("/file-io/upload", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                // get html tags from template
                const successParagraph = document.getElementById("upload-success");
                const fileLink = document.getElementById("file-link");

                if (response.ok && data.link) {
                    successParagraph.innerHTML = "File link: ";

                    // set the text and file link
                    fileLink.href = data.link;
                    fileLink.textContent = data.link;
                    fileLink.target = "_blank";

                    // add link into success paragraph
                    successParagraph.appendChild(fileLink);

                } else {
                    // show an error message if the request is not successful
                    errorParagraph.textContent = `Error:  ${data.error || 'Unknown error'}`;
                }
            } catch (error) {
                console.error("Error:", error);

                // show a generic error message if raise an error
                errorParagraph.textContent = "An error occurred when sending the file."
            }
        });
    } else {
        console.error("Form not found.");
    }
});
