gsap.from("header, aside, table", { opacity: 0, y: 12, duration: 0.45, stagger: 0.08 });

function cell(text, className = "px-5 py-4") {
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
    tr.className = "hover:bg-slate-50";

    const jurisdiction = document.createElement("span");
    jurisdiction.className = "rounded-full bg-slate-100 px-3 py-1 text-xs";
    jurisdiction.textContent = r.jurisdiction ?? "";

    const jurisdictionCell = cell("");
    jurisdictionCell.append(jurisdiction);

    tr.append(
      cell(r.category, "px-5 py-4 font-medium"),
      cell(r.topic),
      cell(r.regulation),
      cell(r.section, "px-5 py-4 font-mono text-xs"),
      cell(r.description, "px-5 py-4 text-slate-600"),
      cell(r.frequency_summary, "px-5 py-4 text-sky-700 font-medium"),
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
    paragraph("font-semibold text-slate-900", data.answer ?? ""),
    paragraph("mt-3", ...labeledText("Frequency", data.required_frequency || "Not confirmed")),
    paragraph("", ...labeledText("Action", data.action || "Not confirmed")),
    paragraph("", ...labeledText("Citation", data.citation || "No citation found")),
    paragraph("", ...labeledText("Confidence", data.confidence ?? "")),
    paragraph("mt-3 text-slate-500", data.interpretation ?? "")
  ];

  if (data.missing_information?.length) {
    content.push(paragraph(
      "mt-2 text-amber-700",
      ...labeledText("Missing", data.missing_information.join(", "))
    ));
  }

  answerBox.replaceChildren(...content);
}

document.getElementById("askBtn").addEventListener("click", askHydro);
