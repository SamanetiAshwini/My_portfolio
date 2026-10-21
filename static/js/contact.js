/**
 * Ashwini Samaneti — Contact Form Submission & Validation Handler
 * Enforces client & server validation, anti-spam honeypot,
 * real status reporting, and safe error handling without fake successes.
 */

document.addEventListener('DOMContentLoaded', () => {
  initContactForm();
});

function initContactForm() {
  const form = document.getElementById('portfolioContactForm');
  const submitBtn = document.getElementById('contactSubmitBtn');
  const statusDiv = document.getElementById('contactFormStatus');

  if (!form || !submitBtn || !statusDiv) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset status box
    statusDiv.className = 'form-status';
    statusDiv.style.display = 'none';
    statusDiv.textContent = '';

    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const subject = form.subject.value.trim();
    const message = form.message.value.trim();
    const website = form.website ? form.website.value : ''; // Honeypot trap

    // Client-side validations
    if (name.length < 2) {
      showStatus('Please enter your full name (at least 2 characters).', 'error');
      form.name.focus();
      return;
    }

    const emailRegex = /^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$/;
    if (!emailRegex.test(email)) {
      showStatus('Please provide a valid email address so Ashwini can reply to you.', 'error');
      form.email.focus();
      return;
    }

    if (message.length < 10) {
      showStatus('Please enter a descriptive message (at least 10 characters).', 'error');
      form.message.focus();
      return;
    }

    // Set Loading State
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
        <path d="M12 2a10 10 0 0 1 10 10"></path>
      </svg>
      <span>Submitting to Database...</span>
    `;

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          subject: subject,
          message: message,
          website: website
        })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showStatus(
          `✔ ${result.message || 'Thank you! Your message has been saved to the MongoDB database.'}`,
          'success'
        );
        form.reset();
      } else {
        // Clear reporting of backend failure (e.g. 503 DB unverified, or 400 validation)
        const errMsg = result.detail || 'An unexpected response occurred while contacting the server.';
        showStatus(`⚠ ${errMsg}`, 'error');
      }
    } catch (networkError) {
      showStatus(
        '⚠ Network connection error. Could not reach the FastAPI server. Please check your network or reach Ashwini directly at ashwinisamaneti@gmail.com.',
        'error'
      );
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });

  function showStatus(msg, type) {
    statusDiv.textContent = msg;
    statusDiv.className = `form-status ${type}`;
    statusDiv.style.display = 'block';
  }
}
