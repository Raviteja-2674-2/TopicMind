const API = "http://127.0.0.1:8000";

let questions = [];
let current = 0;
let correct = 0;
let wrong = 0;
let currentTopic = "";
let answered = false;

function setTopic(t) {
  document.getElementById("topic-input").value = t;
}

function show(id) {
  ["home-screen","loading-screen","quiz-screen","results-screen"].forEach(s => {
    document.getElementById(s).style.display = "none";
  });
  document.getElementById(id).style.display = "block";
}

function activateStep(n) {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById("step" + i);
    if (i < n) el.className = "step done";
    else if (i === n) el.className = "step active";
    else el.className = "step";
  }
}

async function startQuiz() {
  const topic = document.getElementById("topic-input").value.trim();
  if (!topic) { document.getElementById("topic-input").focus(); return; }

  currentTopic = topic;
  questions = []; current = 0; correct = 0; wrong = 0;
  document.getElementById("start-btn").disabled = true;
  show("loading-screen");

  activateStep(1);
  await sleep(600);
  activateStep(2);
  await sleep(500);
  activateStep(3);

  try {
    const res = await fetch(`${API}/api/generate-quiz`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic })
    });

    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    questions = data.questions;

    activateStep(4);
    await sleep(400);

    document.getElementById("quiz-topic-label").textContent = "Topic: " + topic;
    const ctx = data.context_used || "";
    document.getElementById("rag-text-display").textContent = ctx;

    show("quiz-screen");
    renderQuestion();
  } catch (e) {
    alert("Could not connect to backend. Make sure the server is running on port 8000.");
    show("home-screen");
    document.getElementById("start-btn").disabled = false;
  }
}

function renderQuestion() {
  answered = false;
  const q = questions[current];
  const pct = (current / 5) * 100;

  document.getElementById("progress-fill").style.width = pct + "%";
  document.getElementById("q-counter").textContent = `Question ${current + 1} of 5`;
  document.getElementById("correct-count").textContent = correct + " correct";
  document.getElementById("wrong-count").textContent = wrong + " wrong";
  document.getElementById("q-number").textContent = "Question " + (current + 1);
  document.getElementById("q-text").textContent = q.question;
  document.getElementById("feedback-box").style.display = "none";
  document.getElementById("quiz-actions").style.display = "none";

  const opts = document.getElementById("options-list");
  opts.innerHTML = "";
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = opt;
    btn.onclick = () => selectAnswer(opt.charAt(0), i);
    opts.appendChild(btn);
  });
}

async function selectAnswer(chosen, idx) {
  if (answered) return;
  answered = true;

  const q = questions[current];
  const isCorrect = chosen === q.correct;

  document.querySelectorAll(".option-btn").forEach((btn, i) => {
    btn.disabled = true;
    const letter = q.options[i].charAt(0);
    if (letter === q.correct) btn.classList.add("correct");
    else if (i === idx && !isCorrect) btn.classList.add("wrong");
  });

  const fb = document.getElementById("feedback-box");
  fb.style.display = "block";
  fb.className = "feedback-box " + (isCorrect ? "correct" : "wrong");
  fb.innerHTML = "<div>Loading feedback...</div>";

  try {
    const res = await fetch(`${API}/api/check-answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: q.question,
        user_answer: chosen,
        correct_answer: q.correct,
        topic: currentTopic
      })
    });
    const data = await res.json();
    if (data.is_correct) correct++; else wrong++;

    fb.innerHTML = `<div>${data.feedback}</div><div class="feedback-tip">Tip: ${data.tip}</div>`;
  } catch {
    if (isCorrect) { correct++; fb.innerHTML = `<div>Correct! ${q.explanation}</div>`; }
    else { wrong++; fb.innerHTML = `<div>Wrong. ${q.explanation}</div>`; }
  }

  document.getElementById("correct-count").textContent = correct + " correct";
  document.getElementById("wrong-count").textContent = wrong + " wrong";

  const nextBtn = document.getElementById("next-btn");
  nextBtn.textContent = current < 4 ? "Next question →" : "See results";
  document.getElementById("quiz-actions").style.display = "flex";
}

function nextQuestion() {
  current++;
  if (current >= 5) { showResults(); return; }
  renderQuestion();
}

function showResults() {
  document.getElementById("progress-fill").style.width = "100%";
  const pct = Math.round((correct / 5) * 100);
  const icons = ["😔","😕","🙂","😊","🎉"];
  const labels = ["Keep trying!","Getting there!","Good job!","Great work!","Perfect!"];
  const msgs = [
    "Don't give up — review the topic and try again.",
    "You're making progress. A few more rounds and you'll nail it.",
    "Solid attempt! You have a good foundation on this topic.",
    "Impressive! You clearly know your stuff.",
    "Outstanding! You aced every single question."
  ];

  document.getElementById("results-icon").textContent = icons[correct] || "🎉";
  document.getElementById("results-score").textContent = correct + "/5";
  document.getElementById("results-label").textContent = labels[correct] || "Well done!";
  document.getElementById("results-topic").textContent = "Topic: " + currentTopic;
  document.getElementById("res-correct").textContent = correct;
  document.getElementById("res-wrong").textContent = wrong;
  document.getElementById("results-msg").textContent = msgs[correct] || "";
  show("results-screen");
}

function resetQuiz() {
  document.getElementById("topic-input").value = "";
  document.getElementById("start-btn").disabled = false;
  show("home-screen");
}

function retryTopic() {
  document.getElementById("topic-input").value = currentTopic;
  document.getElementById("start-btn").disabled = false;
  show("home-screen");
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
