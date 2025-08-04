const form = document.getElementById("friend-form");
const messageDiv = document.getElementById("message");
const quoteBtn = document.getElementById("quoteBtn");
const quoteDisplay = document.getElementById("quoteDisplay");

const quotes = [
  "A real friend is one who walks in when the rest of the world walks out.",
  "Friendship doubles your joy and divides your sorrow.",
  "Good friends are like stars. You don't always see them, but you know they're always there.",
  "True friendship comes when the silence between two people is comfortable.",
  "Friends are the family we choose for ourselves."
];

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.getElementById("nameInput").value.trim();
  const note = document.getElementById("noteInput").value.trim();

  if (name && note) {
    messageDiv.textContent = `💌 Your note to ${name} has been sent!`;
    form.reset();
  } else {
    messageDiv.textContent = "Please fill out both fields.";
  }
});

quoteBtn.addEventListener("click", () => {
  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
  quoteDisplay.textContent = `"${randomQuote}"`;
});
