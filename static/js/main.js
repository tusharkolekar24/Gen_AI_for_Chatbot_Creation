function toggleSidebar() {
    const sidebar = document.querySelector('.sidenav');
    sidebar.classList.toggle('toggled');
    document.querySelector('.content').classList.toggle('toggled');
}       
const config = {
            displaylogo: false,
            modeBarButtonsToRemove: [
                'resetAxes', 'spikelines', 'zoomIn2d', 'zoomOut2d',
                'zoom2d', 'pan2d', 'select2d'
            ]
        };

document.querySelector('.dropdown-button').addEventListener('click', function() {
    var formContainer = this.nextElementSibling;
        if (formContainer.style.display === 'block') {
            formContainer.style.display = 'none';
        } else {
            formContainer.style.display = 'block';
        }
});

function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (message === "") return;

    let chatBox = document.getElementById("chat-box");
    let userMessage = document.createElement("div");
    userMessage.classList.add("user");
    // userMessage.innerHTML = `${message} <span class='emoji'>😊</span>`;
    // userMessage.innerHTML = `<span class='text'>${message}</span> <span class='emoji'>😊</span>`;

    userMessage.innerHTML = `
    <div class="message-row user-row">
        <span class="emoji">🧑</span>
        <pre class="text">${message}</pre>
    </div>
    `;
    chatBox.appendChild(userMessage);
    input.value = "";

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = document.createElement("div");
        botMessage.classList.add("bot");
        // botMessage.innerHTML = `<span class='emoji1'>🤖</span> ${data.reply}`;
        // botMessage.innerHTML = `<span class='emoji1'>🤖</span> <span class='text'>${data.reply}</span>`;

        botMessage.innerHTML = `
        <div class="message-row bot-row">
            <pre class="text">${data.reply}</pre>
            <span class="emoji1">🤖</span>
        </div>
        `;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}