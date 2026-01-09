async function sendMessage() {
  const input = document.getElementById("userInput").value.trim();
  const messagesDiv = document.getElementById("messages");
  if (!input) return;

  const userMsg = document.createElement("div");
  userMsg.className = "user-msg align-self-end";
  userMsg.textContent = input;
  messagesDiv.appendChild(userMsg);
  document.getElementById("userInput").value = "";
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  const assistantMsg = document.createElement("div");
  assistantMsg.className = "assistant-msg align-self-start";
  assistantMsg.innerHTML = "⏳ Loading...";
  messagesDiv.appendChild(assistantMsg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  try {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": window.location.origin,
        "X-Title": document.title
      },
      body: JSON.stringify({
        model: "deepseek/deepseek-r1:free",
        messages: [{ role: "user", content: input }],
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    const message = data.choices?.[0]?.message?.content || "No response received.";
    assistantMsg.innerHTML = marked.parse(message);
  } catch (error) {
    assistantMsg.innerHTML = "❌ Error: " + error.message;
  }
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}