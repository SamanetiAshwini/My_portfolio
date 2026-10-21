/**
 * Explore Ashwini — Interactive Floating Portfolio Chatbot
 * Answers visitor questions about education, skills, projects, and contact
 * using the verified portfolio knowledge engine.
 */

document.addEventListener('DOMContentLoaded', () => {
  initChatbot();
});

function initChatbot() {
  const triggerBtn = document.getElementById('chatbotTriggerBtn');
  const panel = document.getElementById('chatbotPanel');
  const closeBtn = document.getElementById('chatbotCloseBtn');
  const minimizeBtn = document.getElementById('chatbotMinimizeBtn');
  const messagesBody = document.getElementById('chatbotMessagesBody');
  const inputField = document.getElementById('chatInputField');
  const sendBtn = document.getElementById('chatSendBtn');
  const suggestionsWrap = document.getElementById('chatbotSuggestionsWrap');
  const notificationBadge = document.getElementById('chatbotNotificationBadge');

  if (!triggerBtn || !panel) return;

  // Toggle open / close
  triggerBtn.addEventListener('click', () => {
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) {
      if (notificationBadge) notificationBadge.style.display = 'none';
      inputField.focus();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      panel.classList.remove('open');
    });
  }

  if (minimizeBtn) {
    minimizeBtn.addEventListener('click', () => {
      panel.classList.remove('open');
    });
  }

  // Handle Send
  const handleSend = async (messageText) => {
    const text = (messageText || inputField.value).trim();
    if (!text) return;

    // Append user message
    appendMessage(text, 'user');
    if (!messageText) inputField.value = '';

    // Show typing indicator
    const typingIndicator = showTypingIndicator();
    messagesBody.scrollTop = messagesBody.scrollHeight;

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      removeTypingIndicator(typingIndicator);

      if (!response.ok) {
        throw new Error('API communication error');
      }

      const data = await response.json();
      appendMessage(data.reply, 'bot');

      // Update follow-up prompt chips if provided
      if (data.suggested_prompts && data.suggested_prompts.length > 0) {
        renderSuggestions(data.suggested_prompts);
      }
    } catch (err) {
      removeTypingIndicator(typingIndicator);
      // Fallback local deterministic responder
      const fallbackReply = getLocalFallback(text);
      appendMessage(fallbackReply.reply, 'bot');
      renderSuggestions(fallbackReply.prompts);
    }

    messagesBody.scrollTop = messagesBody.scrollHeight;
  };

  sendBtn.addEventListener('click', () => handleSend());
  inputField.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  });

  // Suggestion chips handler
  function renderSuggestions(prompts) {
    if (!suggestionsWrap) return;
    suggestionsWrap.innerHTML = '';
    prompts.forEach(p => {
      const chip = document.createElement('button');
      chip.className = 'prompt-chip';
      chip.textContent = p;
      chip.addEventListener('click', () => {
        handleSend(p);
      });
      suggestionsWrap.appendChild(chip);
    });
  }

  // Initial chips
  renderSuggestions([
    "Tell me about CodeFoundry",
    "What are your core skills?",
    "Tell me about your education",
    "How can I contact Ashwini?"
  ]);

  function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${sender}`;

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';

    // Simple markdown-style formatting (bold, newlines, links)
    let formatted = escapeHTML(text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/•\s/g, '• ')
      .replace(/\n/g, '<br/>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color:#22d3ee;text-decoration:underline;">$1</a>');

    bubble.innerHTML = formatted;
    msgDiv.appendChild(bubble);
    messagesBody.appendChild(msgDiv);
    messagesBody.scrollTop = messagesBody.scrollHeight;
  }

  function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot typing-message';
    typingDiv.innerHTML = `
      <div class="chat-bubble">
        <div class="typing-dots">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    `;
    messagesBody.appendChild(typingDiv);
    return typingDiv;
  }

  function removeTypingIndicator(element) {
    if (element && element.parentNode) {
      element.parentNode.removeChild(element);
    }
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  function getLocalFallback(msg) {
    const m = msg.toLowerCase();
    if (m.includes('codefoundry')) {
      return {
        reply: "CodeFoundry is a Software Engineering Readiness Platform built with Django 5.2, DRF, PostgreSQL, Redis, React, and isolated Docker sandboxes for automated code evaluation.",
        prompts: ["Tell me about SkillTrack", "Tell me about SMRITI", "What are your skills?"]
      };
    }
    if (m.includes('education') || m.includes('college')) {
      return {
        reply: "Ashwini is pursuing B.Tech in Artificial Intelligence at Vidya Jyothi Institute of Technology (VJIT), Hyderabad (2022-2026) with an 8.34/10 CGPA.",
        prompts: ["What certifications do you have?", "What projects have you built?", "Contact Ashwini"]
      };
    }
    return {
      reply: "Ashwini Samaneti is a Python Full Stack Developer & AI enthusiast with projects in Django, FastAPI, PostgreSQL, Docker, and OpenCV. How can I help you explore her work?",
      prompts: ["Tell me about CodeFoundry", "What are your core skills?", "Download resume"]
    };
  }
}
