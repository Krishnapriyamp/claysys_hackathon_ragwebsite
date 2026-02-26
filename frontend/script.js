document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url-input');
    const ingestBtn = document.getElementById('ingest-btn');
    const statusMsg = document.getElementById('ingest-status');

    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    let isIngested = false;

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerText = text;

        msgDiv.appendChild(contentDiv);
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return contentDiv;
    }

    function addLoadingMessage() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot-message';
        msgDiv.id = 'loading-message';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = '<span class="spinner"></span> Thinking<span class="loading-dots"></span>';

        msgDiv.appendChild(contentDiv);
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return msgDiv;
    }

    function removeLoadingMessage() {
        const loadingMsg = document.getElementById('loading-message');
        if (loadingMsg) {
            loadingMsg.remove();
        }
    }

    ingestBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;

        try {
            // UI state
            ingestBtn.disabled = true;
            ingestBtn.innerHTML = '<span class="spinner"></span> Ingesting';
            statusMsg.textContent = 'Processing URL... This might take a bit.';
            statusMsg.className = 'status-message';

            chatInput.disabled = true;
            sendBtn.disabled = true;

            const response = await fetch('/api/ingest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (response.ok) {
                statusMsg.textContent = data.message;
                statusMsg.className = 'status-message';
                isIngested = true;
                chatInput.disabled = false;
                sendBtn.disabled = false;
                addMessage('URL fully ingested! What would you like to know?', false);
            } else {
                statusMsg.textContent = data.error || 'Failed to ingest URL.';
                statusMsg.className = 'status-message status-error';
            }
        } catch (err) {
            statusMsg.textContent = 'Error: Could not reach the backend server.';
            statusMsg.className = 'status-message status-error';
        } finally {
            ingestBtn.disabled = false;
            ingestBtn.innerText = 'Ingest';
            if (isIngested) {
                chatInput.disabled = false;
                sendBtn.disabled = false;
            }
        }
    });

    async function handleSend() {
        const query = chatInput.value.trim();
        if (!query || !isIngested) return;

        addMessage(query, true);
        chatInput.value = '';

        chatInput.disabled = true;
        sendBtn.disabled = true;

        addLoadingMessage();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            removeLoadingMessage();

            if (response.ok) {
                addMessage(data.answer, false);

                if (data.exit === true) {
                    chatInput.disabled = true;
                    sendBtn.disabled = true;
                    chatInput.placeholder = "Session Closed";
                    isIngested = false; // Prevent further sending
                    return; // Stop further execution for this function
                }
            } else {
                addMessage('Error: ' + (data.error || 'Failed to generate answer.'), false);
            }
        } catch (err) {
            removeLoadingMessage();
            addMessage('Error: Could not reach the backend server.', false);
        } finally {
            if (isIngested) {
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
        }
    }

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });
});
