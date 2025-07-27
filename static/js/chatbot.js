
function sendMessage() {
  const input = document.getElementById("chat-input");
  const chatBody = document.getElementById("chat-body");
  const msg = input.value.trim();
  if (!msg) return;

  chatBody.innerHTML += `<div class="user-msg"><strong>You:</strong> ${msg}</div>`;
  input.value = "";
  chatBody.scrollTop = chatBody.scrollHeight;
  
// Prevent restoring chat history after clearing
document.addEventListener("DOMContentLoaded", function() {
  const chatBody = document.getElementById("chat-body");
  const chatOptions = document.getElementById("chat-options");
  // Only restore if localStorage exists and is not empty
  const saved = localStorage.getItem("hsbc_chat_history");
  if (saved && saved.trim().length > 0) {
    chatBody.innerHTML = saved;
  } else {
    chatBody.innerHTML = `<div class='bot-msg' style='margin-bottom:8px;'><strong>HyBe:</strong> Welcome to HSBC! How can I help you today?</div>`;
    if (chatOptions) {
      chatOptions.innerHTML = "";
      chatOptions.style.display = "flex";
      setTimeout(() => {
        chatOptions.innerHTML = `
          <button class='chat-option-btn' type='button' onclick='selectOption(1)'>Apply for a Loan</button>
          <button class='chat-option-btn' type='button' onclick='selectOption(2)'>Block a Card</button>
          <button class='chat-option-btn' type='button' onclick='selectOption(3)'>Account Statement</button>
        `;
      }, 50);
    }
  }
});
  // Save chat history for dashboard
  localStorage.setItem("hsbc_chat_history", chatBody.innerHTML);

  // Check for file upload
  var fileInput = document.getElementById('chat-file');
  var files = fileInput && fileInput.files.length > 0 ? fileInput.files : null;
  var formData = new FormData();
  formData.append('message', msg);
  if (files) {
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
  }
  fetch("/chat", {
    method: "POST",
    body: files ? formData : JSON.stringify({ message: msg }),
    headers: files ? {} : { "Content-Type": "application/json" },
  })
    .then((res) => res.json())
    .then((data) => {
      // Add message to chat
      if (data.reply) {
        chatBody.innerHTML += `<div class="bot-msg"><strong>HyBe:</strong> ${data.reply}</div>`;
      }
      chatBody.scrollTop = chatBody.scrollHeight;
      
      // Handle login requirement
      if (data.require_login) {
        if (window.showLoginModal) {
          window.showLoginModal();
        }
        return;
      }
      
      // Save chat history
      localStorage.setItem("hsbc_chat_history", chatBody.innerHTML);
      
      // Handle document upload
      if (data.reply && /upload.*document|aadhaar|pan/i.test(data.reply)) {
        fileInput.style.display = "inline-block";
      } else {
        fileInput.style.display = "none";
        fileInput.value = "";
      }
      
      // Handle PDF preview
      if (data.pdf_url) {
        chatBody.innerHTML += `<div class='bot-msg'><strong>HyBe:</strong> <a href='${data.pdf_url}' target='_blank'>View Loan Application PDF Preview</a></div>`;
      }
    });
}

function clearChat() {
  const chatBody = document.getElementById("chat-body");
  const chatOptions = document.getElementById("chat-options");
  // Remove all chat-related localStorage
  localStorage.removeItem("hsbc_chat_history");
  localStorage.removeItem("pending_chat_option");
  // Reset chat body and input
  chatBody.innerHTML = `<div class='bot-msg' style='margin-bottom:8px;'><strong>HyBe:</strong> Welcome to HSBC! How can I help you today?</div>`;
  const chatInput = document.getElementById("chat-input");
  if (chatInput) chatInput.value = "";
  // Hide file input if present
  var fileInput = document.getElementById('chat-file');
  if (fileInput) {
    fileInput.style.display = "none";
    fileInput.value = "";
  }
  if (chatOptions) {
    chatOptions.innerHTML = "";
    chatOptions.style.display = "flex";
    setTimeout(() => {
      chatOptions.innerHTML = `
        <button class='chat-option-btn' type='button' onclick='selectOption(1)'>Apply for a Loan</button>
        <button class='chat-option-btn' type='button' onclick='selectOption(2)'>Block a Card</button>
        <button class='chat-option-btn' type='button' onclick='selectOption(3)'>Account Statement</button>
      `;
    }, 50);
  }
}

function toggleChat() {
  const chatWidget = document.getElementById("chatbot-container");
  if (chatWidget.style.display === "none") {
    chatWidget.style.display = "block";
  } else {
    chatWidget.style.display = "none";
  }
}

function selectOption(option) {
  localStorage.setItem('pending_chat_option', option);
  let msg = "";
  if (option == 1) msg = "I want to apply for a loan.";
  if (option == 2) msg = "I want to block my card.";
  if (option == 3) msg = "I need my account statement.";
  if (msg) {
    document.getElementById("chat-input").value = msg;
    sendMessage();
    // Hide options after selection
    var chatOptions = document.getElementById("chat-options");
    if (chatOptions) {
      chatOptions.innerHTML = "";
      chatOptions.style.display = "none";
    }
  }
}
