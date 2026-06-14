function cell(text, className = "table-cell") {
  const td = document.createElement("td");
  td.className = className;
  td.textContent = text ?? "";
  return td;
}

function paragraph(className, ...children) {
  const p = document.createElement("p");
  if (className) p.className = className;
  p.append(...children);
  return p;
}

function labeledText(label, value) {
  const strong = document.createElement("strong");
  strong.textContent = `${label}:`;
  return [strong, ` ${value}`];
}

async function searchRegs() {
  const search = document.getElementById("searchInput").value;
  const res = await fetch(`/api/regulations?search=${encodeURIComponent(search)}`);
  const data = await res.json();
  document.getElementById("resultCount").textContent = data.items.length;
  const rows = data.items.map(r => {
    const tr = document.createElement("tr");
    tr.className = "table-row";

    const jurisdiction = document.createElement("span");
    jurisdiction.className = "badge";
    jurisdiction.textContent = r.jurisdiction ?? "";

    const jurisdictionCell = cell("");
    jurisdictionCell.append(jurisdiction);

    tr.append(
      cell(r.category, "table-cell table-cell--strong"),
      cell(r.topic),
      cell(r.regulation),
      cell(r.section, "table-cell table-cell--mono"),
      cell(r.description, "table-cell table-cell--muted"),
      cell(r.frequency_summary, "table-cell table-cell--accent"),
      jurisdictionCell
    );

    return tr;
  });
  document.getElementById("regTable").replaceChildren(...rows);
}

document.getElementById("searchBtn").addEventListener("click", searchRegs);

async function askHydro() {
  const payload = {
    parameter: document.getElementById("parameter").value,
    system_type: document.getElementById("systemType").value,
    source_type: document.getElementById("sourceType").value,
    population_served: document.getElementById("population").value ? Number(document.getElementById("population").value) : null,
    result: document.getElementById("result").value,
    jurisdiction: null
  };
  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  const answerBox = document.getElementById("answerBox");
  const content = [
    paragraph("answer-line answer-line--lead", data.answer ?? ""),
    paragraph("answer-line", ...labeledText("Frequency", data.required_frequency || "Not confirmed")),
    paragraph("answer-line", ...labeledText("Action", data.action || "Not confirmed")),
    paragraph("answer-line", ...labeledText("Citation", data.citation || "No citation found")),
    paragraph("answer-line", ...labeledText("Confidence", data.confidence ?? "")),
    paragraph("answer-line answer-line--muted", data.interpretation ?? "")
  ];

  if (data.missing_information?.length) {
    content.push(paragraph(
      "answer-warning",
      ...labeledText("Missing", data.missing_information.join(", "))
    ));
  }

  answerBox.replaceChildren(...content);
}

document.getElementById("askBtn").addEventListener("click", askHydro);
