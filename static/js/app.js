const form = document.getElementById("scan-form");
const description = document.getElementById("description");
const charCount = document.getElementById("char-count");
const analyzeButton = document.getElementById("analyze-button");
const emptyState = document.getElementById("empty-state");
const resultsContent = document.getElementById("results-content");
const resultsPanel = document.getElementById("results-panel");

description.addEventListener("input", () => {
  charCount.textContent = `${description.value.length} / 12000`;
});

async function getSamples() {
  const response = await fetch("/api/samples");
  if (!response.ok) throw new Error("Could not load sample offers.");
  return response.json();
}

function fillForm(sample) {
  description.value = sample.description || "";
  document.getElementById("company_name").value = sample.company_name || "";
  document.getElementById("company_website").value = sample.company_website || "";
  document.getElementById("recruiter_email").value = sample.recruiter_email || "";
  document.getElementById("stipend").value = sample.stipend || "";
  document.getElementById("payment_requested").checked = Boolean(sample.payment_requested);
  charCount.textContent = `${description.value.length} / 12000`;
  description.focus();
}

document.getElementById("load-suspicious").addEventListener("click", async () => {
  try {
    const samples = await getSamples();
    fillForm(samples.find(item => item.id === "sample-high-risk"));
  } catch (error) {
    showError(error.message);
  }
});

document.getElementById("load-detailed").addEventListener("click", async () => {
  try {
    const samples = await getSamples();
    fillForm(samples.find(item => item.id === "sample-lower-risk"));
  } catch (error) {
    showError(error.message);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    description: description.value.trim(),
    company_name: document.getElementById("company_name").value.trim(),
    company_website: document.getElementById("company_website").value.trim(),
    recruiter_email: document.getElementById("recruiter_email").value.trim(),
    stipend: document.getElementById("stipend").value.trim(),
    payment_requested: document.getElementById("payment_requested").checked
  };

  if (payload.description.length < 30) {
    showError("Please enter at least 30 characters of internship description.");
    description.focus();
    return;
  }

  analyzeButton.disabled = true;
  analyzeButton.textContent = "Analyzing offer…";
  emptyState.hidden = true;
  resultsContent.hidden = false;
  resultsContent.innerHTML = '<p class="result-summary">Checking the submitted details…</p>';

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Analysis failed. Please try again.");
    renderResult(result);
  } catch (error) {
    showError(error.message || "Could not connect to the server. Is Flask running?");
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.innerHTML = 'Analyze offer <span aria-hidden="true">→</span>';
  }
});

function showError(message) {
  emptyState.hidden = true;
  resultsContent.hidden = false;
  resultsContent.innerHTML = "";
  const box = document.createElement("div");
  box.className = "error-message";
  box.textContent = message;
  resultsContent.appendChild(box);
}

function renderResult(result) {
  resultsContent.innerHTML = "";
  const categoryClass = result.category.toLowerCase().replaceAll(" ", "-");
  const score = Math.max(0, Math.min(100, Number(result.score) || 0));

  const header = document.createElement("div");
  header.className = "result-heading";
  const heading = document.createElement("div");
  heading.innerHTML = '<p class="eyebrow">SCAN COMPLETE</p><h3>Assessment results</h3>';
  const badge = document.createElement("span");
  badge.className = `category-pill category-${categoryClass}`;
  badge.textContent = result.category;
  header.append(heading, badge);
  resultsContent.appendChild(header);

  const scoreLine = document.createElement("div");
  scoreLine.className = "score-line";
  scoreLine.innerHTML = `<span class="score-number">${score}<small> / 100</small></span><span class="card-label">Risk indicator score</span>`;
  resultsContent.appendChild(scoreLine);

  const track = document.createElement("div");
  track.className = "score-track";
  const fill = document.createElement("div");
  fill.className = "score-fill" + (score <= 24 ? " low" : score >= 50 ? " high" : "");
  fill.style.width = `${score}%`;
  track.appendChild(fill);
  resultsContent.appendChild(track);

  const summary = document.createElement("p");
  summary.className = "result-summary";
  summary.textContent = result.summary || "";
  resultsContent.appendChild(summary);

  if (result.insufficient_information) {
    const note = document.createElement("p");
    note.className = "error-message";
    note.textContent = "Not enough information for a meaningful assessment. Add more details and verify the offer independently.";
    resultsContent.appendChild(note);
  }

  addSubhead(resultsContent, `Warning signals (${(result.findings || []).length})`);
  if (!result.findings || result.findings.length === 0) {
    const none = document.createElement("p");
    none.className = "result-summary";
    none.textContent = "No configured warning patterns were detected. This is not proof that the offer is genuine.";
    resultsContent.appendChild(none);
  } else {
    result.findings.forEach(item => {
      const card = document.createElement("article");
      card.className = "finding";
      const titleRow = document.createElement("div");
      titleRow.className = "finding-title";
      const title = document.createElement("span");
      title.textContent = item.title;
      const points = document.createElement("span");
      points.className = "finding-points";
      points.textContent = `+${item.points} pts`;
      titleRow.append(title, points);
      const explanation = document.createElement("p");
      explanation.textContent = item.explanation;
      card.append(titleRow, explanation);
      if (item.evidence) {
        const evidence = document.createElement("div");
        evidence.className = "evidence";
        evidence.textContent = `Evidence: ${item.evidence}`;
        card.appendChild(evidence);
      }
      resultsContent.appendChild(card);
    });
  }

  addSubhead(resultsContent, "Recommended next steps");
  const list = document.createElement("ul");
  list.className = "recommendations";
  (result.recommendations || []).forEach(text => {
    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });
  resultsContent.appendChild(list);

  const disclaimer = document.createElement("p");
  disclaimer.className = "result-disclaimer";
  disclaimer.textContent = result.disclaimer || "This is a rule-based assessment, not proof of fraud or legitimacy.";
  resultsContent.appendChild(disclaimer);
  resultsPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function addSubhead(parent, text) {
  const heading = document.createElement("h4");
  heading.className = "result-subhead";
  heading.textContent = text;
  parent.appendChild(heading);
}
