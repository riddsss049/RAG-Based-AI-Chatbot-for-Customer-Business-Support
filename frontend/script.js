const input = document.getElementById("msg");
const chatBox = document.getElementById("chat");

async function send() {
    const msg = input.value.trim();
    if (!msg) return;

    appendMessage("You", msg);
    input.value = "";

    const res = await fetch("/chat/send", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            user_id: "web-user-1",
            message: msg
        })
    });

    const data = await res.json();
    appendMessage("Bot", data.reply);
}

function appendMessage(sender, text) {
    chatBox.innerHTML += `<p><b>${sender}:</b> ${text}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}