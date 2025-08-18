async function sendMessage() {
    let input = document.getElementById("user-input").value;
    let response = await fetch(`/chatbot/get_response/?message=${encodeURIComponent(input)}`);
    let data = await response.json();
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
}
