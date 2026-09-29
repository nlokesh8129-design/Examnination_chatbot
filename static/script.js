const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (sender === "user") {
        messageDiv.classList.add("user-message");
        messageDiv.innerHTML = `<strong>You:</strong> ${message}`;
    } else {
        messageDiv.classList.add("bot-message");
        messageDiv.innerHTML = `<strong>Chatbot:</strong> ${message}`;
    }

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    try {

        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        addMessage(data.response, "bot");

    } catch (error) {

        addMessage(
            "Unable to connect to the chatbot server.",
            "bot"
        );

        console.error(error);
    }
}


input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});