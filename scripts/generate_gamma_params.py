#!/usr/bin/env python3
"""
generate_gamma_params.py — Generate Gamma submission materials from gamma-ready markdown.

Usage:
    python3 scripts/generate_gamma_params.py <file.md> [--instructions <file.json>]

Produces TWO outputs:
  1. *-gamma-api.json   — Gamma MCP API parameters (2000-char additionalInstructions)
  2. *-gamma-web.md     — Comprehensive web submission guide for Gamma browser paste
                          (unlimited length, per-slide design + AI image instructions)

The web submission guide is the primary output for manual Gamma.app browser submissions.
The API JSON is for programmatic Gamma MCP tool calls.
"""

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

from card_utils import classify_card, get_title, split_cards


DEFAULT_PRESENTER = "Evan DeCan, MD"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CORE_SCRIPTS_DIR = SKILL_DIR.parent / "gamma-presentation-core" / "scripts"
CORE_BUILD_SCRIPT = CORE_SCRIPTS_DIR / "build_gamma_payload.py"
CORE_VALIDATE_SCRIPT = CORE_SCRIPTS_DIR / "validate_gamma_payload.py"
MEDICAL_PROFILE_PATH = SKILL_DIR / "config" / "gamma-medical-profile.json"

IMAGE_STYLE = (
    "ultra-detailed photorealistic medical photography, surgical suite and trauma bay realism, "
    "50mm lens depth, high dynamic range, anatomical accuracy, no illustrations or cartoons"
)


def _load_module(path: Path, name: str):
    resolved = path.resolve()
    expected_parent = CORE_SCRIPTS_DIR.resolve()
    if not str(resolved).startswith(str(expected_parent)):
        raise RuntimeError(
            f"Module path '{resolved}' is outside the expected directory '{expected_parent}'"
        )
    if not resolved.exists():
        raise RuntimeError(
            f"Required dependency not found: gamma-presentation-core. "
            f"Install as a sibling skill."
        )
    spec = importlib.util.spec_from_file_location(name, resolved)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to load module from {resolved}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_CORE_BUILD = None
_CORE_VALIDATE = None


def _get_core_build():
    global _CORE_BUILD
    if _CORE_BUILD is None:
        _CORE_BUILD = _load_module(CORE_BUILD_SCRIPT, "gamma_core_build")
    return _CORE_BUILD


def _get_core_validate():
    global _CORE_VALIDATE
    if _CORE_VALIDATE is None:
        _CORE_VALIDATE = _load_module(CORE_VALIDATE_SCRIPT, "gamma_core_validate")
    return _CORE_VALIDATE


def extract_topic(cards: list[str]) -> str:
    """Extract presentation topic from first substantive card heading.

    Skips common non-descriptive titles like 'Disclosures' or 'Learning Objectives'.
    """
    skip_titles = {"disclosures", "learning objectives", "financial disclosures"}
    if not cards:
        return "Medical Presentation"
    for card in cards[:5]:
        for line in card.strip().split('\n'):
            stripped = line.strip()
            if stripped.startswith('## '):
                title = stripped.lstrip('# ').strip()
                if title.lower() not in skip_titles:
                    return title
    return "Medical Presentation"




def group_consecutive(indices: list[int]) -> str:
    """Group consecutive indices into ranges: [1,2,3,5,7,8] -> '1-3,5,7-8'."""
    if not indices:
        return ""
    groups = []
    start = indices[0]
    prev = indices[0]
    for idx in indices[1:]:
        if idx == prev + 1:
            prev = idx
        else:
            if start == prev:
                groups.append(str(start))
            else:
                groups.append(f"{start}-{prev}")
            start = idx
            prev = idx
    if start == prev:
        groups.append(str(start))
    else:
        groups.append(f"{start}-{prev}")
    return ",".join(groups)


# --- API Output (2000-char compressed) ---

def _load_profile_directives() -> tuple[dict[str, str], dict[str, str]]:
    """Load slideTypeDirectives and typeImageStyles from the medical profile config."""
    try:
        with open(MEDICAL_PROFILE_PATH, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        slide_directives = profile_data.get("slideTypeDirectives", {})
        type_image_styles = profile_data.get("typeImageStyles", {})
        return slide_directives, type_image_styles
    except Exception as e:
        import sys
        print(f"WARNING: Failed to load medical profile directives: {e}", file=sys.stderr)
        return {}, {}


def build_api_instructions(card_types: list[tuple[int, str]]) -> str:
    """Build compact per-slide design instructions, max 2000 chars for API."""
    type_groups: dict[str, list[int]] = {}
    for slide_num, card_type in card_types:
        type_groups.setdefault(card_type, []).append(slide_num)

    # Load directives from profile config; fall back to hardcoded defaults
    profile_directives, _ = _load_profile_directives()
    directives = {
        "Title": "Full-bleed hero image, centered white text",
        "Disclosures": "Clean minimal, dark blue bg, no images",
        "Learning Objectives": "Clean minimal, dark blue bg",
        "Case": "Split layout, clinical scene left, case text right",
        "Data/Table": "Bold stats, dark bg, tables preserved exactly",
        "MCQ": "Quiz card layout, green highlight for answer",
        "Content": "Clean layout, key message prominent",
        "References": "Small text, 2-column, no images",
        "Q&A": "Centered text, professional bg image",
        "Take-Home": "Large numbered list, bold key phrases",
        "Future Directions": "Forward-looking imagery, clean layout",
        "Guideline": "Side-by-side comparison table, preserve structure",
        "Trial": "PICO or trial results table, key findings highlighted",
    }
    # Override with profile directives where available
    for k, v in profile_directives.items():
        directives[k] = v

    parts = ["SLIDE DESIGN BY TYPE:"]

    for card_type in ["Title", "Disclosures", "Learning Objectives", "Case",
                       "Data/Table", "MCQ", "Content", "Take-Home",
                       "Future Directions", "Guideline", "Trial", "References", "Q&A"]:
        if card_type not in type_groups:
            continue
        slides = type_groups[card_type]
        range_str = group_consecutive(slides)
        directive = directives.get(card_type, "Clean layout")
        label = f"Slide {range_str}" if len(slides) == 1 else f"Slides {range_str}"
        parts.append(f"{label} ({card_type}): {directive}.")

    parts.append(
        "GLOBAL: Preserve ALL tables exactly. High contrast. "
        "Academic medicine. Sources at bottom of each slide."
    )

    result = " ".join(parts)
    if len(result) > 2000:
        result = result[:1997] + "..."
    return result


def generate_api_params(content: str, presenter: str, card_types: list[tuple[int, str]], num_cards: int, topic: str) -> dict:
    """Generate Gamma MCP API parameters using gamma-presentation-core contracts."""
    additional_instructions = build_api_instructions(card_types)

    # Append header/footer instructions to additionalInstructions since
    # the public API does not accept cardOptions.headerFooter (400 error).
    footer_instruction = (
        f" FOOTER: Add slide numbers (bottom-right) and \"{presenter}\" "
        f"(bottom-left) on all slides except the title slide."
    )
    additional_instructions += footer_instruction

    core_build = _get_core_build()
    profile = core_build.load_profile(MEDICAL_PROFILE_PATH)

    payload = core_build.build_gamma_payload(
        content,
        profile=profile,
        text_mode="preserve",
        output_format="presentation",
        num_cards=num_cards,
        card_split="auto",
        additional_instructions=additional_instructions,
        image_options={
            "source": "aiGenerated",
            "model": "imagen-4-pro",
            "style": IMAGE_STYLE,
        },
        text_options={
            "amount": "detailed",
        },
        card_options={
            "dimensions": "16x9",
        },
    )
    # Always include themeId from medical profile
    try:
        with open(MEDICAL_PROFILE_PATH, 'r', encoding='utf-8') as f:
            _prof = json.load(f)
        theme_id = _prof.get("themeId")
        if theme_id:
            payload["themeId"] = theme_id
    except Exception:
        payload["themeId"] = "marine"
    return payload


# --- Web Output (comprehensive, unlimited length) ---

DEFAULT_TYPE_INSTRUCTIONS = {
    "Title": "Full-bleed hero image relevant to the presentation topic. Centered white text overlay with presenter name and credentials. Dramatic, cinematic lighting. High-impact visual.",
    "Disclosures": "Clean minimal layout with solid dark blue background. No imagery. White text only. Professional and understated.",
    "Learning Objectives": "Clean minimal layout with solid dark blue background. Numbered list format. No imagery. White text, clear hierarchy.",
    "Case": "Split layout: clinical scene or patient care imagery on the left (emergency department, trauma bay, ambulance). Patient details and clinical data as structured text on the right. Urgent, realistic tone.",
    "Data/Table": "Data-first layout. Large bold statistics as focal points. Full-width tables dominate the slide. Subtle dark background. High-contrast text. Preserve ALL table formatting exactly as written.",
    "MCQ": "Quiz card layout with clean sans-serif font. Four answer options clearly labeled A-D. Highlight correct answer with green accent. Clean, minimal background. Interactive feel.",
    "Content": "Clean professional layout with key message prominent. Relevant medical imagery. Bullet hierarchy preserved. Sources displayed at bottom in small text.",
    "References": "Small text in 2-column layout. No images. Clean numbered list. Dense but readable. Professional academic formatting.",
    "Q&A": "Professional closing slide. Centered large text. Subtle medical/clinical background image. Include contact information or metrics if present.",
    "Take-Home": "Large numbered list with bold key phrases. Each point is a standalone take-away message. Clean background. High-impact typography.",
    "Future Directions": "Forward-looking imagery (research, innovation, technology). Clean layout. Bullet points with emerging concepts. Optimistic but professional tone.",
    "Guideline": "Side-by-side comparison layout. Full-width table with society guidelines. Professional academic formatting. Preserve table structure exactly.",
    "Trial": "Clinical trial summary layout. PICO framework or trial results table. Clean data presentation. Key findings highlighted.",
}

NON_PHOTOREAL_TOKENS = (
    "illustration",
    "diagram",
    "flowchart",
    "schematic",
    "cartoon",
    "icon",
)

LO_TAG_RE = re.compile(r"\s*\[LO:\s*[\d,\s]+\]")

NO_IMAGE_CARD_TYPES = {
    "Disclosures",
    "Learning Objectives",
    "References",
}


def strip_lo_tags(text: str) -> str:
    return LO_TAG_RE.sub("", text).strip()


def normalize_instruction_title(text: str) -> str:
    """Compact slide titles for instruction artifacts."""
    title = strip_lo_tags(text)
    title = title.replace("```", "").strip()
    for marker in (" | ", " **"):
        if marker in title:
            title = title.split(marker, 1)[0].strip()
    return title[:140].strip()


def style_points_for_card_type(card_type: str) -> list[str]:
    presets: dict[str, list[str]] = {
        "Title": [
            "Full-bleed visual with centered title hierarchy.",
            "High-contrast text over controlled dark overlay.",
            "Use premium conference-grade typography spacing.",
        ],
        "Case": [
            "Split layout with clear visual/text separation.",
            "Prioritize clinical realism and urgency.",
            "Keep vitals and key findings scan-friendly.",
        ],
        "Data/Table": [
            "Use full-width table and preserve source formatting exactly.",
            "Maximize contrast for numeric readability.",
            "Keep decorative elements minimal to avoid data interference.",
        ],
        "MCQ": [
            "Use quiz layout with clear A-D option separation.",
            "Highlight correct answer in green only on answer slide.",
            "Maintain strict visual consistency across all knowledge checks.",
        ],
        "Content": [
            "Lead with one dominant assertion in headline zone.",
            "Keep bullets concise with clear visual hierarchy.",
            "Reserve lower band for citations and sources.",
        ],
        "Guideline": [
            "Use side-by-side or full-width matrix structure.",
            "Preserve guideline language and row alignment.",
            "Prioritize legibility over decorative visuals.",
        ],
        "Q&A": [
            "Centered closing composition with clean negative space.",
            "Subtle background only; do not overpower text.",
            "Retain professional conference tone.",
        ],
        "Take-Home": [
            "Large numbered points with bold keywords.",
            "One concept per line; avoid visual clutter.",
            "Strong end-of-talk emphasis and contrast.",
        ],
    }
    return presets.get(
        card_type,
        [
            "Maintain high-contrast readability.",
            "Use a clean professional medical conference aesthetic.",
            "Preserve citation and source fidelity.",
        ],
    )


def build_image_prompt(title: str, card_type: str) -> str:
    clean_title = strip_lo_tags(title)
    lowered = clean_title.lower()

    if card_type in NO_IMAGE_CARD_TYPES:
        return "NO_IMAGE"

    if card_type in {"Data/Table", "Guideline", "Trial", "MCQ"}:
        return (
            "NO_IMAGE (data-first slide). Optional background only: subtle, defocused clinical environment "
            "with low contrast and no recognizable text."
        )

    if "case presentation" in lowered or "mr. j.m." in lowered or card_type == "Case":
        subject = "Level 1 trauma bay initial assessment of blunt chest trauma patient with multidisciplinary team"
    elif "vats" in lowered or "orif" in lowered or "rib fixation" in lowered or "rib plating" in lowered:
        subject = "thoracic trauma surgery in modern operating room with rib fixation instruments and thoracoscopic setup"
    elif "questions" in lowered or card_type == "Q&A":
        subject = "professional medical conference closing scene with podium and subtle hospital context"
    elif "take-home" in lowered:
        subject = "clean clinical conference visual motif suggesting synthesis and decision support"
    else:
        subject = f"clinical scene representing: {clean_title}"

    return (
        f"{subject}; ultra-detailed photoreal medical photography, 16:9 composition, "
        "realistic skin and material textures, HDR lighting, shallow depth of field, "
        "anatomically accurate, non-graphic, no illustrations, no diagrams, no icons, "
        "no overlaid text, no watermark."
    )


def normalize_instruction_set(
    cards: list[str],
    card_types: list[tuple[int, str]],
    raw_instructions: dict | None,
) -> dict[str, dict]:
    normalized: dict[str, dict] = {}

    for slide_num, card_type in card_types:
        key = str(slide_num)
        if raw_instructions and key in raw_instructions and raw_instructions[key].get("title"):
            title = normalize_instruction_title(str(raw_instructions[key]["title"]))
        else:
            title = normalize_instruction_title(get_title(cards[slide_num - 1]))

        if raw_instructions and key in raw_instructions:
            base_instruction = str(raw_instructions[key].get("instruction", "")).strip()
        else:
            base_instruction = DEFAULT_TYPE_INSTRUCTIONS.get(card_type, DEFAULT_TYPE_INSTRUCTIONS["Content"])

        instruction = enforce_photoreal_instruction(card_type, base_instruction)
        image_prompt = build_image_prompt(title, card_type)

        is_no_image = image_prompt.startswith("NO_IMAGE")
        normalized[key] = {
            "title": title,
            "instruction": instruction,
            "stylePoints": style_points_for_card_type(card_type),
            "imageRequired": not is_no_image,
            "imagePrompt": image_prompt,
        }

    return normalized


def enforce_photoreal_instruction(card_type: str, instruction: str) -> str:
    """Normalize visual instructions to photoreal medical imagery where applicable."""
    if card_type in {"Disclosures", "Learning Objectives", "References"}:
        return instruction

    lower = instruction.lower()
    if not any(token in lower for token in NON_PHOTOREAL_TOKENS):
        return instruction

    if card_type == "Case":
        return (
            "Split layout with a photoreal trauma bay or emergency department scene on the left "
            "and case details on the right. Real clinical environment only; no diagrams or illustrations."
        )
    if card_type == "Content":
        return (
            "Use photoreal clinical imagery matched to the claim, with realistic OR/ICU/trauma settings. "
            "No diagrams, flowcharts, icons, or illustrations."
        )

    return (
        "Use high-detail photoreal medical imagery with anatomical accuracy and real clinical context. "
        "No diagrams, flowcharts, icons, cartoons, or illustrations."
    )


_ELEMENT_BUDGETS: dict[str, str] = {
    "Title": "title(1) + subtitle(1) + presenter-byline(1) = 3 elements",
    "Disclosures": "title(1) + text-block(1) = 2 elements; no images",
    "Learning Objectives": "title(1) + numbered-list(1) = 2 elements; no images",
    "Case": "title(1) + clinical-image(1) + vitals-block(1) + narrative-text(1) = 4 elements max",
    "Content": "title(1) + image(1) + bullets(1) + sources(1) = 4 elements max",
    "Data/Table": "title(1) + table(1) + stat-callout(opt 1) = 3 elements max; no decorative images",
    "Trial": "title(1) + table(1) + key-finding-callout(opt 1) = 3 elements max; no decorative images",
    "Guideline": "title(1) + comparison-table(1) = 2 elements; no decorative images",
    "MCQ": "title(1) + question-text(1) + answer-list(1) = 3 elements",
    "Take-Home": "title(1) + numbered-list(1) + closing-image(opt 1) = 3 elements max",
    "References": "title(1) + 2-column-list(1) = 2 elements; no images",
    "Q&A": "title(1) + background-image(1) + contact-info(opt 1) = 3 elements max",
}


def build_web_guide(
    source_path: str,
    content_len: int,
    cards: list[str],
    card_types: list[tuple[int, str]],
    num_cards: int,
    topic: str,
    presenter: str,
    instructions: dict | None = None,
) -> str:
    """Build comprehensive web submission guide for Gamma browser paste."""
    _, type_image_styles = _load_profile_directives()
    lines = []

    lines.append(f"# Gamma Web Submission Guide: {topic}")
    lines.append(f"")
    lines.append(f"**Presenter:** {presenter}")
    lines.append(f"**Slides:** {num_cards}")
    lines.append(f"**Generated:** Use this guide when submitting to gamma.app via web browser.")
    lines.append(f"")

    # --- Section 1: Settings ---
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 1. Gamma Settings (Configure in UI)")
    lines.append(f"")
    lines.append(f"| Setting | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| **Format** | Presentation |")
    lines.append(f"| **Text Mode** | Preserve (keep exact text) |")
    lines.append(f"| **Number of Cards** | {num_cards} |")
    lines.append(f"| **Dimensions** | 16:9 (widescreen) |")
    lines.append(f"| **Image Source** | AI Generated |")
    lines.append(f"| **Image Model** | Imagen 4 Pro (highest quality) |")
    lines.append(f"| **Text Amount** | Detailed |")
    lines.append(f"")

    # --- Section 2: Additional Instructions (paste into Gamma) ---
    lines.append(f"## 2. Additional Instructions")
    lines.append(f"")
    lines.append(f"Copy everything below the line into Gamma's \"Additional Instructions\" field:")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Global rules first
    lines.append(f"### GLOBAL RULES")
    lines.append(f"")
    lines.append(f"- This is a **medical grand rounds presentation** for an academic physician audience.")
    lines.append(f"- **Preserve ALL tables exactly as formatted.** Do not simplify, summarize, or rearrange table contents. Maintain column alignment.")
    lines.append(f"- **Preserve all superscript citation formatting** (`<sup>[N]</sup>`). Display Sources at the bottom of each slide exactly as written.")
    lines.append(f"- Each section between `---` markers is **one slide**. Maintain exactly **{num_cards} cards**.")
    lines.append(f"- Use **consistent header hierarchy** across all cards. Slide titles are `##` (H2).")
    lines.append(f"- **High contrast text** throughout. Professional academic medicine aesthetic.")
    lines.append(f"- Add **slide numbers** (bottom-right) and **\"{presenter}\"** (bottom-left) on all slides except the title.")
    lines.append(f"- **Image style for all AI-generated images:** {IMAGE_STYLE}")
    lines.append(f"")

    # Per-slide instructions
    lines.append(f"### PER-SLIDE DESIGN INSTRUCTIONS")
    lines.append(f"")

    for slide_num, card_type in card_types:
        card = cards[slide_num - 1]
        title = get_title(card)

        # Use extracted instruction from source if available, otherwise use type default
        slide_key = str(slide_num)
        if instructions and slide_key in instructions:
            entry = instructions[slide_key]
            instruction = entry.get("instruction", DEFAULT_TYPE_INSTRUCTIONS.get(card_type, DEFAULT_TYPE_INSTRUCTIONS["Content"]))
            image_prompt = entry.get("imagePrompt", build_image_prompt(title, card_type))
            style_points = entry.get("stylePoints", style_points_for_card_type(card_type))
        else:
            instruction = DEFAULT_TYPE_INSTRUCTIONS.get(card_type, DEFAULT_TYPE_INSTRUCTIONS["Content"])
            instruction = enforce_photoreal_instruction(card_type, instruction)
            image_prompt = build_image_prompt(title, card_type)
            style_points = style_points_for_card_type(card_type)

        # Type-specific image style from profile config (fallback to computed image_prompt)
        type_img_style = type_image_styles.get(card_type, image_prompt)
        element_budget = _ELEMENT_BUDGETS.get(card_type, "title(1) + content(1) + image(opt 1) = 3 elements max")

        lines.append(f"**Slide {slide_num}: {title}** ({card_type})")
        lines.append(f"> {instruction}")
        lines.append(f"- Style points: {' | '.join(style_points)}")
        lines.append(f"- Image prompt: {image_prompt}")
        lines.append(f"- Type image style: {type_img_style}")
        lines.append(f"- Element budget: {element_budget}")
        lines.append(f"")

    lines.append(f"---")
    lines.append(f"")

    # --- Section 3: Card Summary ---
    lines.append(f"## 3. Card Classification Summary")
    lines.append(f"")
    lines.append(f"| Slide | Type | Title |")
    lines.append(f"|---|---|---|")
    for slide_num, card_type in card_types:
        title = get_title(cards[slide_num - 1])
        lines.append(f"| {slide_num} | {card_type} | {title} |")
    lines.append(f"")

    # Type distribution
    type_counts: dict[str, int] = {}
    for _, ct in card_types:
        type_counts[ct] = type_counts.get(ct, 0) + 1
    lines.append(f"**Distribution:** " + ", ".join(f"{k}: {v}" for k, v in sorted(type_counts.items(), key=lambda x: -x[1])))
    lines.append(f"")

    # --- Section 4: Content ---
    lines.append(f"## 4. Slide Content (Paste into Gamma Content Area)")
    lines.append(f"")
    lines.append(f"The gamma-ready markdown file should be pasted into Gamma's main content area.")
    lines.append(f"File: `{os.path.basename(source_path)}` ({content_len:,} chars)")
    lines.append(f"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Gamma submission materials from gamma-ready markdown.'
    )
    parser.add_argument('input', help='Gamma-ready markdown file')
    parser.add_argument(
        '--instructions', '-i',
        help='Extracted Gamma instructions JSON (from preprocessor Pass 6)'
    )
    parser.add_argument(
        '--presenter', default=DEFAULT_PRESENTER,
        help=f'Presenter name (default: {DEFAULT_PRESENTER})'
    )
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Load extracted instructions if available
    instructions = None
    instr_path = args.instructions
    if not instr_path:
        # Auto-detect companion instructions JSON
        auto_path = os.path.splitext(filepath)[0] + '-instructions.json'
        if os.path.exists(auto_path):
            instr_path = auto_path

    if instr_path and os.path.exists(instr_path):
        with open(instr_path, 'r', encoding='utf-8') as f:
            instructions = json.load(f)
        print(f"Loaded {len(instructions)} slide instructions from {instr_path}", file=sys.stderr)
    else:
        print("No instructions JSON found — using type-based defaults", file=sys.stderr)

    # Parse cards
    cards = split_cards(content)
    num_cards = len(cards)
    topic = extract_topic(cards)

    # Classify each card
    card_types = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, num_cards, args.presenter)
        card_types.append((i + 1, card_type))

    # Print classification summary
    print(f"Analyzed: {filepath} ({len(content):,} chars, {num_cards} cards)", file=sys.stderr)
    for slide_num, card_type in card_types:
        title = get_title(cards[slide_num - 1])
        instr_marker = "*" if instructions and str(slide_num) in instructions else " "
        print(f"  {instr_marker} Card {slide_num:2d}: {card_type:20s} | {title[:50]}", file=sys.stderr)
    print(file=sys.stderr)

    instructions = normalize_instruction_set(cards, card_types, instructions)

    # Output paths — strip trailing '-gamma' to avoid double suffix
    base = os.path.splitext(filepath)[0]
    if base.endswith('-gamma'):
        base = base[:-6]
    api_path = base + '-gamma-api.json'
    web_path = base + '-gamma-web.md'
    normalized_instructions_path = base + '-gamma-instructions.json'
    image_prompts_path = base + '-gamma-image-prompts.json'

    # 1. Generate API params JSON
    api_params = generate_api_params(content, args.presenter, card_types, num_cards, topic)
    validation = _get_core_validate().validate_payload(api_params)
    validation_errors = [x for x in validation.get("issues", []) if x.get("level") == "error"]
    validation_warnings = [x for x in validation.get("issues", []) if x.get("level") == "warning"]
    if validation_errors:
        print("Generated payload failed core validation:", file=sys.stderr)
        for issue in validation_errors:
            print(f"  ERROR {issue.get('path')}: {issue.get('message')}", file=sys.stderr)
        sys.exit(2)
    if validation_warnings:
        print("Generated payload has core warnings:", file=sys.stderr)
        for issue in validation_warnings:
            print(f"  WARN  {issue.get('path')}: {issue.get('message')}", file=sys.stderr)

    with open(api_path, 'w', encoding='utf-8') as f:
        json.dump(api_params, f, indent=2)
    print(f"Wrote API params: {api_path} ({len(json.dumps(api_params)):,} chars)", file=sys.stderr)

    # 2. Generate web submission guide
    web_guide = build_web_guide(
        filepath, len(content), cards, card_types, num_cards, topic,
        args.presenter, instructions,
    )
    with open(web_path, 'w', encoding='utf-8') as f:
        f.write(web_guide)
    print(f"Wrote web guide:  {web_path} ({len(web_guide):,} chars)", file=sys.stderr)

    with open(normalized_instructions_path, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, indent=2)
    print(f"Wrote normalized instructions: {normalized_instructions_path}", file=sys.stderr)

    image_prompts = {
        key: {
            "title": value["title"],
            "imageRequired": value["imageRequired"],
            "imagePrompt": value["imagePrompt"],
        }
        for key, value in instructions.items()
    }
    with open(image_prompts_path, 'w', encoding='utf-8') as f:
        json.dump(image_prompts, f, indent=2)
    print(f"Wrote image prompts: {image_prompts_path}", file=sys.stderr)

    # Also print API JSON to stdout for convenience
    print(json.dumps(api_params, indent=2))


if __name__ == '__main__':
    main()
