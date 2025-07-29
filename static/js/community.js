// Get the chat input field and button
const chatInput = document.querySelector('.chat-input input');
const chatButton = document.querySelector('.chat-input button');

// Add an event listener to the chat button
chatButton.addEventListener('click', () => {
    // Get the chat input value
    const chatValue = chatInput.value;

    // Create a new chat message element
    const chatMessage = document.createElement('li');
    chatMessage.classList.add('sent');
    chatMessage.innerHTML = `
        <p>${chatValue}</p>
        <span>8:40 AM, Today</span>
    `;

    // Add the chat message to the chat history
    const chatHistory = document.querySelector('.chat-history ul');
    chatHistory.appendChild(chatMessage);

    // Clear the chat input field
    chatInput.value = '';
});