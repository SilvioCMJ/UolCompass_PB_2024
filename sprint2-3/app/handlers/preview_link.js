document.getElementById("fetch-data").addEventListener("click", async () => {
    const inputData = document.getElementById("url-input").value.trim();

    // validate the url
    const isValidUrl = (url) => {
        const urlRegex = /^(https?:\/\/)?(www\.)?([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6}([\/\w .-]*)*\/?$/;
        return urlRegex.test(url);
    };

    // verify if url is valid
    if (!isValidUrl(inputData)) {
        document.getElementById("result").textContent = "Invalid URL";
        return
    }

    let urlToPreview = inputData
    
    try {
        const response = await fetch("/preview-link/api/extract", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            // sends the url as part of the request body
            body: JSON.stringify({ urlToPreview })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        document.getElementById("result").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("result").textContent = "Error fetching data";
    }
});
