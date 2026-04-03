const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Config
const INPUT = path.join(__dirname, "presentation-unified-final.md");
const OUTPUT = "/Users/fee4jk/Library/CloudStorage/OneDrive-UniversityofVirginia/LECTURES/Trauma-Shelf-Review-2026.pptx";
const IMAGES_DIR = path.join(__dirname, "images");

// Marine theme colors
const NAVY = "001F3F";
const WHITE = "FFFFFF";
const ACCENT = "4FC3F7"; // light blue accent
const RED_ACCENT = "FF6B6B";
const GREEN_ACCENT = "66BB6A";
const GRAY = "B0BEC5";

// Parse markdown into slides
function parseMarkdown(md) {
  const slides = [];
  const rawSlides = md.split("\n---\n");

  for (const raw of rawSlides) {
    const trimmed = raw.trim();
    if (!trimmed) continue;

    // Extract title
    const titleMatch = trimmed.match(/^## (.+)$/m);
    if (!titleMatch) continue;
    const title = titleMatch[1];

    // Extract speaker notes
    let notes = "";
    const notesMatch = trimmed.match(/<!-- Speaker Notes:\n([\s\S]*?)-->/);
    if (notesMatch) {
      notes = notesMatch[1].trim();
      // Strip shelf tip formatting
      notes = notes.replace(/> \*\*Shelf Tip:\*\* /g, "\nShelf Tip: ");
    }

    // Extract body (between title and Bottom Line/Sources/Speaker Notes)
    let body = trimmed;
    // Remove everything before and including the title
    body = body.replace(/[\s\S]*?^## .+$/m, "");
    // Remove speaker notes
    body = body.replace(/<!-- Speaker Notes:[\s\S]*?-->/, "");
    // Remove type tags
    body = body.replace(/<!-- type:.*?-->/g, "");
    // Remove Gamma instructions
    body = body.replace(/\*\*Gamma instruction:.*?\*\*/g, "");
    // Remove Sources blocks
    body = body.replace(/\*\*Sources:\*\*[\s\S]*?(?=\n\n|$)/g, "");
    body = body.replace(/- \[\d+\].*$/gm, "");

    // Extract Bottom Line
    let bottomLine = "";
    const blMatch = body.match(/> \*\*Bottom Line:\*\* (.+)/);
    if (blMatch) {
      bottomLine = blMatch[1];
      body = body.replace(/> \*\*Bottom Line:\*\* .+/, "");
    }

    // Extract images
    const images = [];
    const imgRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
    let imgMatch;
    while ((imgMatch = imgRegex.exec(body)) !== null) {
      images.push({ alt: imgMatch[1], url: imgMatch[2] });
    }
    body = body.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, "");

    // Extract tables
    const tables = [];
    const tableRegex = /(\|.+\|[\s\S]*?(?:\n\n|\n(?!\|)|$))/g;
    let tableMatch;
    while ((tableMatch = tableRegex.exec(body)) !== null) {
      const tableText = tableMatch[1].trim();
      const rows = tableText.split("\n").filter(r => r.includes("|") && !r.match(/^\|[\s-|]+\|$/));
      const parsed = rows.map(r =>
        r.split("|").filter(c => c.trim()).map(c => c.trim().replace(/\*\*/g, ""))
      );
      if (parsed.length > 0) tables.push(parsed);
    }
    body = body.replace(/(\|.+\|[\s\S]*?(?:\n\n|\n(?!\|)|$))/g, "");

    // Extract key stat
    let keyStat = "";
    const ksMatch = body.match(/\*\*(.+?)\*\*\s*$/m);
    if (ksMatch && !ksMatch[1].startsWith("Sources") && !ksMatch[1].startsWith("Gamma")) {
      keyStat = ksMatch[1];
    }

    // Clean body to bullet points
    const bullets = body
      .split("\n")
      .map(l => l.trim())
      .filter(l => l.startsWith("- ") || l.startsWith("* ") || /^\d+\./.test(l))
      .map(l => l.replace(/^[-*]\s+/, "").replace(/^\d+\.\s+/, "").replace(/\*\*/g, ""));

    // Detect slide type
    let type = "content";
    if (title.includes("Clinical Decision Point")) type = "mcq";
    else if (title.startsWith("Answer:")) type = "mcq_answer";
    else if (title === "Trauma for the Shelf: Every Topic in 45 Minutes" && !slides.length) type = "title";
    else if (title.includes("Objectives") || title.includes("objectives")) type = "objectives";
    else if (title === "References") type = "references";
    else if (title.includes("Ten Topics, Ten Discriminators")) type = "takehome";
    else if (tables.length > 0) type = "data_table";

    slides.push({ title, body: bullets, notes, bottomLine, images, tables, keyStat, type, raw: trimmed });
  }

  return slides;
}

// Resolve image path (local or URL)
function resolveImage(url) {
  if (url.startsWith("http")) return url;
  const local = path.join(IMAGES_DIR, path.basename(url));
  if (fs.existsSync(local)) return local;
  return url;
}

// Build PPTX
async function buildPptx(slides) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "Evan DeCan, MD";
  pres.title = "Trauma for the Shelf: Every Topic in 45 Minutes";

  // Define slide master
  pres.defineSlideMaster({
    title: "MARINE",
    background: { color: NAVY },
    objects: [
      { text: { text: "Evan DeCan, MD", options: { x: 0.3, y: 5.2, w: 3, h: 0.3, fontSize: 8, color: GRAY, fontFace: "Calibri" } } },
    ],
  });

  let slideNum = 0;

  for (const s of slides) {
    slideNum++;
    const slide = pres.addSlide({ masterName: "MARINE" });

    // Add speaker notes
    if (s.notes) {
      slide.addNotes(s.notes);
    }

    // Slide number (except title)
    if (s.type !== "title") {
      slide.addText(String(slideNum), { x: 9.3, y: 5.2, w: 0.5, h: 0.3, fontSize: 8, color: GRAY, fontFace: "Calibri", align: "right" });
    }

    switch (s.type) {
      case "title":
        slide.addText(s.title, { x: 0.8, y: 1.5, w: 8.4, h: 1.5, fontSize: 36, fontFace: "Georgia", color: WHITE, bold: true, align: "center" });
        slide.addText("Evan DeCan, MD\nDivision of Acute Care Surgery | University of Virginia\n2026", {
          x: 1.5, y: 3.2, w: 7, h: 1.2, fontSize: 16, fontFace: "Calibri", color: GRAY, align: "center"
        });
        break;

      case "objectives":
        slide.addText(s.title, { x: 0.5, y: 0.2, w: 9, h: 0.7, fontSize: 24, fontFace: "Georgia", color: ACCENT, bold: true });
        const objItems = s.body.map((b, i) => ({
          text: `${i + 1}. ${b}`,
          options: { breakLine: true, fontSize: 14, color: WHITE, fontFace: "Calibri", lineSpacingMultiple: 1.5 }
        }));
        slide.addText(objItems, { x: 0.7, y: 1.0, w: 8.5, h: 4.2 });
        break;

      case "mcq":
        slide.addText(s.title, { x: 0.5, y: 0.1, w: 9, h: 0.5, fontSize: 22, fontFace: "Georgia", color: ACCENT, bold: true });
        // Extract question and options from raw
        const qLines = s.raw.split("\n").filter(l => !l.startsWith("##") && !l.startsWith("<!--") && !l.startsWith("**Gamma") && l.trim());
        const questionLines = [];
        const optionLines = [];
        let inOptions = false;
        for (const l of qLines) {
          if (l.trim().startsWith("- A.") || l.trim().startsWith("- A)")) inOptions = true;
          if (inOptions) optionLines.push(l.trim().replace(/^- /, ""));
          else if (!l.includes("-->") && !l.includes("Speaker Notes")) questionLines.push(l.trim());
        }
        const questionText = questionLines.filter(l => l && !l.startsWith("|") && !l.startsWith("---")).join("\n").replace(/\*\*/g, "");
        slide.addText(questionText, { x: 0.5, y: 0.7, w: 9, h: 1.8, fontSize: 14, fontFace: "Calibri", color: WHITE, valign: "top" });

        const optItems = optionLines.map((o, i) => ({
          text: o.replace(/\*\*/g, ""),
          options: { breakLine: true, fontSize: 15, color: i === 1 ? WHITE : GRAY, fontFace: "Calibri", lineSpacingMultiple: 1.8, bold: false }
        }));
        if (optItems.length) {
          slide.addText(optItems, { x: 0.7, y: 2.8, w: 8.5, h: 2.5 });
        }
        break;

      case "mcq_answer":
        slide.addText(s.title.replace(/\*\*/g, ""), { x: 0.5, y: 0.1, w: 9, h: 0.6, fontSize: 20, fontFace: "Georgia", color: GREEN_ACCENT, bold: true });
        const ansItems = s.body.map(b => ({
          text: b,
          options: { breakLine: true, fontSize: 13, color: WHITE, fontFace: "Calibri", lineSpacingMultiple: 1.6 }
        }));
        slide.addText(ansItems, { x: 0.7, y: 0.9, w: 8.5, h: 2.5 });

        if (s.keyStat) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.6, w: 9, h: 0.6, fill: { color: "0D2137" } });
          slide.addText(s.keyStat, { x: 0.7, y: 3.6, w: 8.5, h: 0.6, fontSize: 14, fontFace: "Calibri", color: ACCENT, bold: true, valign: "middle" });
        }
        if (s.bottomLine) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.4, w: 9, h: 0.6, fill: { color: "1A3A5C" } });
          slide.addText(s.bottomLine, { x: 0.7, y: 4.4, w: 8.5, h: 0.6, fontSize: 13, fontFace: "Calibri", color: WHITE, italic: true, valign: "middle" });
        }
        break;

      case "data_table":
        slide.addText(s.title, { x: 0.5, y: 0.1, w: 9, h: 0.6, fontSize: 20, fontFace: "Georgia", color: ACCENT, bold: true });

        // Add image if present (smaller, to the right or above)
        let tableY = 0.8;
        if (s.images.length > 0) {
          try {
            const imgPath = resolveImage(s.images[0].url);
            slide.addImage({ path: imgPath, x: 7, y: 0.8, w: 2.5, h: 2, sizing: { type: "contain", w: 2.5, h: 2 } });
          } catch (e) { /* skip if image fails */ }
        }

        // Add table
        if (s.tables.length > 0) {
          const tbl = s.tables[0];
          const tableRows = tbl.map((row, ri) =>
            row.map(cell => ({
              text: cell,
              options: {
                fontSize: 11,
                fontFace: "Calibri",
                color: ri === 0 ? NAVY : WHITE,
                bold: ri === 0,
                fill: { color: ri === 0 ? ACCENT : (ri % 2 === 0 ? "0D2137" : NAVY) },
                border: { pt: 0.5, color: "1A3A5C" },
                valign: "middle",
                margin: [2, 4, 2, 4],
              }
            }))
          );
          const colCount = tbl[0] ? tbl[0].length : 2;
          const colW = Array(colCount).fill(8.5 / colCount);
          slide.addTable(tableRows, { x: 0.5, y: tableY, w: 8.5, colW, autoPage: false });
        }

        // Bullets below table
        if (s.body.length > 0) {
          const bY = tableY + 2.5;
          const bItems = s.body.map(b => ({
            text: b, options: { breakLine: true, fontSize: 12, color: WHITE, fontFace: "Calibri" }
          }));
          slide.addText(bItems, { x: 0.5, y: bY, w: 8.5, h: 1.2 });
        }

        if (s.keyStat) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.0, w: 9, h: 0.5, fill: { color: "0D2137" } });
          slide.addText(s.keyStat, { x: 0.7, y: 4.0, w: 8.5, h: 0.5, fontSize: 13, fontFace: "Calibri", color: ACCENT, bold: true, valign: "middle" });
        }
        if (s.bottomLine) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.6, w: 9, h: 0.5, fill: { color: "1A3A5C" } });
          slide.addText(s.bottomLine, { x: 0.7, y: 4.6, w: 8.5, h: 0.5, fontSize: 12, fontFace: "Calibri", color: WHITE, italic: true, valign: "middle" });
        }
        break;

      case "takehome":
        slide.addText(s.title, { x: 0.5, y: 0.1, w: 9, h: 0.6, fontSize: 22, fontFace: "Georgia", color: ACCENT, bold: true });
        const thItems = s.body.map(b => ({
          text: b,
          options: { breakLine: true, fontSize: 14, color: WHITE, fontFace: "Calibri", lineSpacingMultiple: 1.5, bullet: { type: "number" } }
        }));
        slide.addText(thItems, { x: 0.5, y: 0.8, w: 9, h: 4.5 });
        break;

      case "references":
        slide.addText("References", { x: 0.5, y: 0.1, w: 9, h: 0.5, fontSize: 20, fontFace: "Georgia", color: ACCENT, bold: true });
        const refText = s.raw.split("\n").filter(l => /^\d+\./.test(l.trim())).map(l => l.trim()).join("\n");
        slide.addText(refText, { x: 0.3, y: 0.6, w: 9.4, h: 4.8, fontSize: 8, fontFace: "Calibri", color: GRAY, valign: "top" });
        break;

      default: // content
        slide.addText(s.title, { x: 0.5, y: 0.1, w: 9, h: 0.7, fontSize: 22, fontFace: "Georgia", color: ACCENT, bold: true });

        // Add image if present
        let contentY = 0.9;
        if (s.images.length > 0) {
          try {
            const imgPath = resolveImage(s.images[0].url);
            slide.addImage({ path: imgPath, x: 6.5, y: 0.9, w: 3, h: 2.2, sizing: { type: "contain", w: 3, h: 2.2 } });
          } catch (e) { /* skip */ }
        }

        // Bullets
        if (s.body.length > 0) {
          const bulletW = s.images.length > 0 ? 5.8 : 8.5;
          const bItems = s.body.map(b => ({
            text: b,
            options: { breakLine: true, bullet: true, fontSize: 14, color: WHITE, fontFace: "Calibri", lineSpacingMultiple: 1.5 }
          }));
          slide.addText(bItems, { x: 0.5, y: contentY, w: bulletW, h: 2.8 });
        }

        // Key stat
        if (s.keyStat) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.9, w: 9, h: 0.55, fill: { color: "0D2137" } });
          slide.addText(s.keyStat, { x: 0.7, y: 3.9, w: 8.5, h: 0.55, fontSize: 14, fontFace: "Calibri", color: ACCENT, bold: true, valign: "middle" });
        }

        // Bottom line
        if (s.bottomLine) {
          slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.55, w: 9, h: 0.55, fill: { color: "1A3A5C" } });
          slide.addText(s.bottomLine, { x: 0.7, y: 4.55, w: 8.5, h: 0.55, fontSize: 13, fontFace: "Calibri", color: WHITE, italic: true, valign: "middle" });
        }
        break;
    }
  }

  // Ensure output directory exists
  const outDir = path.dirname(OUTPUT);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  await pres.writeFile({ fileName: OUTPUT });
  console.log(`PPTX saved to: ${OUTPUT}`);
  console.log(`Total slides: ${slideNum}`);
}

// Main
const md = fs.readFileSync(INPUT, "utf-8");
const slides = parseMarkdown(md);
console.log(`Parsed ${slides.length} slides`);
buildPptx(slides).catch(e => console.error("Error:", e));
