const API_URL = 'http://localhost:8000/chat'; // Make sure your FastAPI endpoint matches
const sessionId = "user_" + Math.floor(Math.random() * 100000);

// Append messages to chat
function appendMessage(role, text) {
    const box = document.getElementById('chatBox');
    const msg = document.createElement('div');
    msg.classList.add('chat-message', role === 'User' ? 'user' : 'bot');

    const content = document.createElement('div');
    content.classList.add('message-content');
    content.textContent = text;

    msg.appendChild(content);
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

// Send message function
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('User', message);
    input.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: message })
        });

        const data = await response.json();
        appendMessage('Bot', data.response || 'Error: No response from server.');
    } catch (error) {
        appendMessage('Bot', 'Error: Unable to reach server.');
    }
}
