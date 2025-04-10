// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to generate a new session_id when the page loads
function generateSessionId() {
    const sessionId = crypto.randomUUID();
    sessionIdInput.value = sessionId;
}

// Get the CSRF token
const csrftoken = getCookie('csrftoken');

// DOM elements
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const sessionIdInput = document.getElementById("session_id");
const chatBox = document.getElementById("chat-box");
const clearChatButton = document.getElementById("clear-chat");
const imageInput = document.getElementById("image");

// Function to display SoliBot's response
function displayBotResponse(data) {
    if (data.error) {
        chatBox.innerHTML += `
            <div class="d-flex justify-content-start mb-2">
                <div class="bg-danger text-white p-2 rounded" style="max-width: 70%;">
                    <strong>Error:</strong> ${data.error}
                </div>
            </div>`;
    } else {
        data.lex.forEach((msg) => {
            chatBox.innerHTML += `
                <div class="d-flex justify-content-start mb-2">
                    <div class="bg-secondary-subtle text-dark p-2 rounded" style="max-width: 70%;">
                        <strong>SoliBot:</strong> ${msg['content']}
                    </div>
                </div>`;
        });
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Form submission to send a message or image to the backend
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    const sessionId = sessionIdInput.value;
    const imageFile = imageInput.files[0];

    if (message) {
        chatBox.innerHTML += `
            <div class="d-flex justify-content-end mb-2">
                <div class="bg-success-subtle text-dark p-2 rounded" style="max-width: 70%;">
                    <strong>You:</strong> ${message}
                </div>
            </div>`;
    }

    messageInput.value = '';
    imageInput.value = '';

    const formData = new FormData();
    formData.append("session_id", sessionId);

    if (message) {
        formData.append("message", message);
    }

    if (imageFile) {
        formData.append("image", imageFile);
    }

    try {
        const response = await fetch("/chatbot/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });

        const data = await response.json();
        displayBotResponse(data);
    } catch (error) {
        console.error("Request error:", error);
    }
});

// Clear the chat
clearChatButton.addEventListener("click", () => {
    chatBox.innerHTML = '';
});

// Generate a new session_id when the page loads
document.addEventListener("DOMContentLoaded", generateSessionId);
