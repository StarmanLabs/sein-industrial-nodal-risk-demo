from __future__ import annotations

import streamlit as st


def inject_global_style() -> None:
    st.markdown(
        """
<style>
:root {
  --sein-bg: #f5f8fb;
  --sein-panel: #ffffff;
  --sein-panel-soft: #f8fafc;
  --sein-ink: #102033;
  --sein-muted: #64748b;
  --sein-line: #d8e3ea;
  --sein-navy: #164a63;
  --sein-deep: #0e2f43;
  --sein-teal: #168c8c;
  --sein-blue: #2f6f9f;
  --sein-amber: #c47a16;
  --sein-red: #b23a2e;
  --sein-green: #1f8a5b;
}

.stApp {
  background:
    linear-gradient(180deg, #f9fbfd 0%, #eef3f7 100%);
  color: var(--sein-ink);
}

[data-testid="stAppViewContainer"] > .main {
  background: transparent;
}

[data-testid="stHeader"] {
  background: transparent;
  height: 0;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
}

[data-testid="stSidebar"] {
  width: 260px !important;
  min-width: 260px !important;
  max-width: 260px !important;
  background:
    radial-gradient(circle at 18% 10%, rgba(35, 211, 211, 0.20), transparent 22%),
    linear-gradient(180deg, #021a2a 0%, #052439 48%, #031826 100%);
  border-right: 1px solid rgba(117, 242, 255, 0.20);
  box-shadow: 12px 0 32px rgba(0, 23, 38, 0.18);
}

[data-testid="stSidebar"] h1 {
  font-size: 1.35rem;
  letter-spacing: 0;
  color: #ffffff;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
  color: #d6edf4;
}

[data-testid="stSidebar"] a {
  border-radius: 8px;
  padding: 0.48rem 0.55rem;
}

[data-testid="stSidebar"] a:hover {
  background: rgba(35, 211, 211, 0.14);
}

.sein-sidebar-brand {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 0.75rem;
  align-items: center;
  margin: 1rem 0 2.3rem 0;
}

.sein-sidebar-mark {
  width: 56px;
  height: 56px;
}

.sein-sidebar-mark svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 16px rgba(35, 211, 211, 0.28));
}

.sein-sidebar-title {
  color: #ffffff;
  font-size: 1.85rem;
  line-height: 0.95;
  font-weight: 860;
  letter-spacing: 0;
}

.sein-sidebar-subtitle {
  color: #e8f9ff;
  font-size: 0.82rem;
  line-height: 1.08;
  font-weight: 780;
  text-transform: uppercase;
  letter-spacing: 0.045em;
  margin-top: 0.24rem;
}

.sein-sidebar-section {
  color: #23d3d3;
  font-size: 0.78rem;
  text-transform: uppercase;
  font-weight: 820;
  letter-spacing: 0.07em;
  margin: 0.9rem 0 0.75rem 0;
}

.sein-sidebar-note {
  width: 100%;
  border: 1px solid rgba(35, 211, 211, 0.65);
  background: rgba(2, 26, 42, 0.72);
  border-radius: 8px;
  color: #e9fbff;
  padding: 0.95rem 0.85rem;
  text-align: center;
  box-shadow: 0 18px 38px rgba(0, 0, 0, 0.20);
  margin-top: 2rem;
}

.sein-sidebar-note-icon {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(35, 211, 211, 0.75);
  border-radius: 50%;
  display: grid;
  place-items: center;
  margin: 0 auto 0.6rem auto;
  color: #23d3d3;
  font-weight: 900;
}

.sein-sidebar-note strong {
  display: block;
  color: #ffffff;
  font-size: 0.78rem;
  line-height: 1.2;
  margin-bottom: 0.3rem;
}

.sein-sidebar-note span {
  display: block;
  color: #d6edf4 !important;
  font-size: 0.75rem;
  line-height: 1.28;
}

[data-testid="stSidebar"] hr {
  border-color: rgba(117, 242, 255, 0.18);
}

[data-testid="stSidebar"] [role="radiogroup"] label {
  border-radius: 7px;
  padding: 0.55rem 0.55rem;
  margin: 0.1rem 0;
  color: #f4fbff;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  background: rgba(35, 211, 211, 0.12);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: linear-gradient(90deg, rgba(35, 211, 211, 0.55), rgba(22, 140, 140, 0.24));
  box-shadow: inset 3px 0 0 #23d3d3;
}

.sein-custom-nav {
  display: flex;
  flex-direction: column;
  gap: 0.28rem;
  margin: 0.75rem 0 0.9rem 0;
}

.sein-nav-link {
  display: block;
  text-decoration: none !important;
  color: #3c4858 !important;
  font-weight: 650;
  border-radius: 8px;
  padding: 0.62rem 0.65rem;
}

.sein-nav-link:hover {
  background: #e1e9f0;
  color: var(--sein-navy) !important;
}

.block-container {
  max-width: 1320px;
  padding-top: 0;
  padding-bottom: 3rem;
}

h1 {
  color: var(--sein-ink);
  font-weight: 760;
  letter-spacing: 0;
}

h2, h3 {
  color: var(--sein-ink);
  letter-spacing: 0;
}

.sein-hero {
  position: relative;
  overflow: hidden;
  min-height: 410px;
  border: 1px solid rgba(117, 242, 255, 0.18);
  border-radius: 0;
  background:
    linear-gradient(90deg, rgba(1, 22, 36, 0.98) 0%, rgba(3, 36, 58, 0.92) 52%, rgba(2, 22, 35, 0.62) 100%),
    radial-gradient(circle at 80% 18%, rgba(35, 211, 211, 0.26), transparent 28%),
    linear-gradient(180deg, #032238 0%, #021523 100%);
  color: #ffffff;
  padding: 3rem 3.4rem 2.7rem 3.4rem;
  margin: 0 -1rem 0 -1rem;
  box-shadow: 0 18px 42px rgba(3, 27, 42, 0.20);
}

.sein-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: linear-gradient(90deg, transparent 0%, black 22%, black 100%);
  pointer-events: none;
}

.sein-hero::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 120px;
  background:
    linear-gradient(180deg, transparent 0%, rgba(1, 14, 23, 0.86) 100%);
  pointer-events: none;
}

.sein-hero-content {
  position: relative;
  z-index: 2;
  max-width: 690px;
}

.sein-hero-visual {
  position: absolute;
  z-index: 1;
  top: 2.1rem;
  right: 2.3rem;
  width: min(40vw, 440px);
  opacity: 0.96;
}

.sein-hero-visual svg {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 0 20px rgba(35, 211, 211, 0.25));
}

.peru-outline {
  fill: rgba(35, 211, 211, 0.035);
  stroke: rgba(117, 242, 255, 0.72);
  stroke-width: 2;
  stroke-dasharray: 3 5;
}

.peru-lines path {
  fill: none;
  stroke: rgba(117, 242, 255, 0.35);
  stroke-width: 1.5;
}

.sein-hero-visual circle {
  fill: #23d3d3;
}

.sein-exec-kpi-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0;
  margin: 0 -1rem 1.5rem -1rem;
  padding: 1.7rem 3rem;
  background: #ffffff;
  border-bottom: 1px solid var(--sein-line);
  box-shadow: 0 12px 30px rgba(16, 32, 51, 0.06);
}

.sein-exec-kpi {
  background: transparent;
  border: 0;
  border-right: 1px solid var(--sein-line);
  border-radius: 0;
  padding: 0.25rem 1.4rem;
  min-height: 130px;
  box-shadow: none;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.sein-exec-kpi:last-child { border-right: 0; }

.sein-exec-kpi::before {
  display: none;
}

.sein-exec-kpi.signal::before { background: var(--sein-teal); }
.sein-exec-kpi.action::before { background: var(--sein-green); }
.sein-exec-kpi.watch::before { background: var(--sein-amber); }
.sein-exec-kpi.scope::before { background: var(--sein-navy); }

.sein-exec-kpi-label {
  color: var(--sein-muted);
  font-size: 0.72rem;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: 0.065em;
  margin-bottom: 0.36rem;
}

.sein-exec-kpi-icon {
  width: 34px;
  height: 34px;
  margin: 0 auto 0.55rem auto;
  color: var(--sein-teal);
}

.sein-exec-kpi-icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sein-exec-kpi-value {
  color: var(--sein-ink);
  font-size: 2.45rem;
  line-height: 1.05;
  font-weight: 820;
}

.sein-exec-kpi-note {
  color: #475569;
  font-size: 0.78rem;
  line-height: 1.32;
  margin-top: 0.42rem;
}

.sein-flow-panel {
  border-top: 1px solid var(--sein-line);
  border-bottom: 1px solid var(--sein-line);
  background: transparent;
  box-shadow: none;
  margin: 1.4rem 0 1.2rem 0;
  padding: 2rem 0;
}

.sein-flow-copy {
  background: linear-gradient(180deg, #eef6f8 0%, #f8fafc 100%);
  border-left: 4px solid var(--sein-teal);
  border-radius: 8px;
  padding: 1rem 1rem;
}

.sein-flow-kicker,
.sein-taxonomy-kicker {
  color: var(--sein-muted);
  font-size: 0.7rem;
  font-weight: 780;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  margin-bottom: 0.34rem;
}

.sein-flow-headline,
.sein-taxonomy-headline {
  color: var(--sein-ink);
  font-size: 1.55rem;
  line-height: 1.18;
  font-weight: 820;
  margin-bottom: 1.35rem;
}

.sein-flow-headline::after,
.sein-use-title::after,
.sein-taxonomy-headline::after {
  content: "";
  display: block;
  width: 32px;
  height: 3px;
  background: var(--sein-teal);
  margin-top: 0.65rem;
}

.sein-flow-text {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.45;
}

.sein-flow-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.6rem;
  border: 0;
  overflow: visible;
  background: transparent;
}

.sein-flow-step {
  display: block;
  align-items: start;
  background: transparent;
  border-right: 1px solid var(--sein-line);
  padding: 0 1rem 0 0.25rem;
  min-height: 220px;
  position: relative;
}

.sein-flow-step:last-child { border-right: 0; }

.sein-flow-step:not(:last-child)::after {
  content: "→";
  position: absolute;
  top: 58px;
  right: -1.15rem;
  color: #9aa8b6;
  font-size: 2.6rem;
  font-weight: 300;
}

.sein-flow-icon {
  width: 82px;
  height: 82px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: radial-gradient(circle, #168c8c 0%, #0b6d7f 72%);
  border: 14px solid rgba(22, 140, 140, 0.14);
  color: #ffffff;
  margin: 0 0 1.05rem 0.25rem;
  box-shadow: 0 10px 24px rgba(22, 140, 140, 0.16);
}

.sein-flow-icon.rank {
  background: radial-gradient(circle, #32a852 0%, #168328 72%);
  border-color: rgba(50, 168, 82, 0.16);
}

.sein-flow-icon.proof {
  background: radial-gradient(circle, #f08c00 0%, #c46f00 72%);
  border-color: rgba(240, 140, 0, 0.18);
}

.sein-flow-icon svg {
  width: 38px;
  height: 38px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sein-flow-title {
  color: var(--sein-ink);
  font-size: 1.08rem;
  font-weight: 800;
  margin-bottom: 0.28rem;
}

.sein-flow-step:nth-child(1) .sein-flow-title { color: #0b6d7f; }
.sein-flow-step:nth-child(2) .sein-flow-title { color: #168328; }
.sein-flow-step:nth-child(3) .sein-flow-title { color: #c46f00; }

.sein-flow-body {
  color: #26384d;
  font-size: 0.95rem;
  line-height: 1.5;
}

.sein-use-panel {
  border-radius: 0;
  border: 0;
  border-bottom: 1px solid var(--sein-line);
  background: transparent;
  padding: 1rem 0 1.55rem 0;
  box-shadow: none;
  margin: 0.9rem 0 1rem 0;
}

.sein-use-title {
  color: var(--sein-ink);
  font-size: 1.32rem;
  font-weight: 820;
  margin-bottom: 0.7rem;
}

.sein-use-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 2.2rem;
}

.sein-use-step {
  display: grid;
  grid-template-columns: 70px minmax(0, 1fr);
  column-gap: 1rem;
  align-items: start;
  border: 1px solid var(--sein-line);
  background: #ffffff;
  border-radius: 8px;
  padding: 1.1rem 1.05rem;
  box-shadow: 0 10px 26px rgba(16, 32, 51, 0.055);
  position: relative;
}

.sein-use-step:not(:last-child)::after {
  content: "→";
  position: absolute;
  right: -1.9rem;
  top: 45%;
  color: #a4afba;
  font-size: 2rem;
}

.sein-use-step span {
  display: block;
  color: var(--sein-ink);
  font-weight: 800;
  font-size: 0.86rem;
  margin-bottom: 0.26rem;
}

.sein-use-step p {
  color: #475569;
  font-size: 0.83rem;
  line-height: 1.42;
  margin: 0 0 0.55rem 0;
}

.sein-use-step a {
  display: inline-block;
  color: var(--sein-teal) !important;
  font-size: 0.84rem;
  font-weight: 820;
  text-decoration: none !important;
}

.sein-use-icon {
  grid-row: span 3;
  width: 54px;
  height: 54px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  color: #ffffff;
  background: linear-gradient(135deg, #0b6d7f, #168c8c);
}

.sein-use-icon.ranking {
  background: linear-gradient(135deg, #168328, #42b946);
}

.sein-use-icon.case {
  background: linear-gradient(135deg, #c93b31, #e66d38);
}

.sein-use-icon svg {
  width: 29px;
  height: 29px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sein-taxonomy-panel {
  border: 0;
  border-radius: 8px;
  background: transparent;
  padding: 0.95rem 0;
  box-shadow: none;
  margin: 1rem 0 1rem 0;
}

.sein-taxonomy-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: end;
  margin-bottom: 0.85rem;
}

.sein-taxonomy-caption {
  max-width: 460px;
  color: #475569;
  font-size: 0.86rem;
  line-height: 1.4;
}

.sein-taxonomy-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0;
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  overflow: hidden;
  background: #ffffff;
}

.sein-taxonomy-item {
  border: 0;
  border-right: 1px solid var(--sein-line);
  border-radius: 0;
  padding: 1rem 1rem;
  min-height: 152px;
  background: #ffffff;
}

.sein-taxonomy-item:last-child { border-right: 0; }

.sein-taxonomy-item.urgent { border-top: 4px solid var(--sein-red); color: var(--sein-red); }
.sein-taxonomy-item.selective { border-top: 4px solid var(--sein-amber); color: #f08c00; }
.sein-taxonomy-item.watch { border-top: 4px solid var(--sein-green); color: var(--sein-green); }
.sein-taxonomy-item.base { border-top: 4px solid var(--sein-blue); color: var(--sein-blue); }
.sein-taxonomy-item.limited { border-top: 4px solid #5546a6; color: #5546a6; }

.sein-taxonomy-icon {
  width: 34px;
  height: 34px;
  margin-bottom: 0.62rem;
}

.sein-taxonomy-icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sein-taxonomy-title {
  color: currentColor;
  font-size: 0.9rem;
  font-weight: 820;
  margin-bottom: 0.34rem;
}

.sein-taxonomy-body {
  color: #475569;
  font-size: 0.82rem;
  line-height: 1.42;
}

.sein-compact-note {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 0.85rem;
  align-items: center;
  border-radius: 8px;
  border: 1px solid #bcdce5;
  background: linear-gradient(90deg, #eef9fb, #f8fcfe);
  color: #475569;
  padding: 0.95rem 1rem;
  font-size: 0.86rem;
  line-height: 1.44;
  margin: 0.9rem 0;
}

.sein-compact-note strong {
  color: var(--sein-ink);
}

.sein-compact-note-icon {
  width: 38px;
  height: 38px;
  color: var(--sein-teal);
}

.sein-compact-note-icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sein-hero-kicker {
  font-size: 0.84rem;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #23d3d3;
  opacity: 1;
  margin-bottom: 0.9rem;
}

.sein-hero-title {
  font-size: clamp(2rem, 4.2vw, 3.75rem);
  line-height: 1.08;
  font-weight: 880;
  margin-bottom: 1rem;
  max-width: 720px;
}

.sein-hero-title span {
  color: #23d3d3;
}

.sein-hero-body {
  max-width: 640px;
  font-size: 1.12rem;
  line-height: 1.45;
  opacity: 0.94;
}

.sein-hero-proof {
  border-left: 4px solid #23d3d3;
  margin-top: 1.5rem;
  padding-left: 1rem;
  max-width: 560px;
  color: #ffffff;
  font-size: 1.02rem;
  line-height: 1.45;
}

.sein-hero-actions {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  max-width: 650px;
  margin-top: 2rem;
}

.sein-hero-action {
  border: 1px solid rgba(255, 255, 255, 0.58);
  color: #ffffff;
  border-radius: 6px;
  padding: 0.82rem 1rem;
  font-size: 0.88rem;
  font-weight: 820;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(2, 24, 38, 0.42);
}

.sein-hero-action.primary {
  border-color: transparent;
  background: linear-gradient(90deg, #18b7b7, #22d3d3);
  color: #052132;
}

.sein-section-title {
  color: var(--sein-ink);
  font-size: 1.15rem;
  font-weight: 800;
  margin: 1.25rem 0 0.45rem 0;
}

.sein-section-caption {
  color: var(--sein-muted);
  font-size: 0.9rem;
  line-height: 1.45;
  margin: -0.1rem 0 0.65rem 0;
}

.sein-insight-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.7rem;
  margin: 0.8rem 0 1rem 0;
}

.sein-insight-card {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.9rem 0.95rem;
  min-height: 118px;
  box-shadow: 0 8px 22px rgba(24, 34, 53, 0.04);
}

.sein-insight-card.decision {
  border-top: 4px solid var(--sein-teal);
}

.sein-insight-card.evidence {
  border-top: 4px solid var(--sein-blue);
}

.sein-insight-card.action {
  border-top: 4px solid var(--sein-green);
}

.sein-insight-card.caveat {
  border-top: 4px solid var(--sein-amber);
}

.sein-insight-title {
  color: var(--sein-ink);
  font-size: 0.82rem;
  font-weight: 800;
  margin-bottom: 0.34rem;
}

.sein-insight-body {
  color: #435063;
  font-size: 0.84rem;
  line-height: 1.43;
}

.sein-badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0.55rem 0 0.85rem 0;
}

.sein-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.34rem;
  border-radius: 999px;
  border: 1px solid #d4dee8;
  background: #ffffff;
  color: #3c4858;
  padding: 0.32rem 0.58rem;
  font-size: 0.78rem;
  font-weight: 720;
  white-space: nowrap;
}

.sein-badge.priority-a {
  border-color: #efb2ac;
  background: #fff2f1;
  color: #8e2f2a;
}

.sein-badge.priority-b {
  border-color: #edc987;
  background: #fff8e8;
  color: #8a5a14;
}

.sein-badge.watchlist {
  border-color: #a8cfe0;
  background: #eaf5f9;
  color: #245a73;
}

.sein-badge.monitor {
  border-color: #ccd3dc;
  background: #f1f4f7;
  color: #4f5d6f;
}

.sein-badge.evidence-a {
  border-color: #9fd4c2;
  background: #eefaf5;
  color: #287c67;
}

.sein-badge.evidence-b {
  border-color: #edc987;
  background: #fff8e8;
  color: #8a5a14;
}

.sein-action-panel {
  border-radius: 8px;
  border: 1px solid #cfdbe7;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  padding: 1rem 1.1rem;
  box-shadow: 0 10px 26px rgba(24, 34, 53, 0.055);
  margin: 0.85rem 0;
}

.sein-action-title {
  color: var(--sein-ink);
  font-weight: 820;
  font-size: 1rem;
  margin-bottom: 0.35rem;
}

.sein-action-body {
  color: #3c4858;
  line-height: 1.5;
  font-size: 0.92rem;
}

[data-testid="stCaptionContainer"] {
  color: var(--sein-muted);
}

.sein-page-kicker {
  color: var(--sein-teal);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 0.4rem;
  margin-bottom: 0.25rem;
}

.sein-kpi {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.9rem 1rem;
  box-shadow: 0 8px 22px rgba(24, 34, 53, 0.045);
  min-height: 102px;
}

.sein-kpi.priority-a,
.sein-kpi.danger {
  border-left: 4px solid var(--sein-red);
  background: #fff7f6;
}

.sein-kpi.priority-b,
.sein-kpi.warning {
  border-left: 4px solid var(--sein-amber);
  background: #fffaf1;
}

.sein-kpi.good {
  border-left: 4px solid var(--sein-green);
  background: #f5fbf8;
}

.sein-kpi.info {
  border-left: 4px solid var(--sein-teal);
  background: #f7fcfc;
}

.sein-kpi.neutral {
  border-left: 4px solid #9aa4b2;
}

.sein-kpi-label {
  color: var(--sein-muted);
  font-size: 0.76rem;
  font-weight: 650;
  text-transform: uppercase;
  letter-spacing: 0.055em;
  margin-bottom: 0.42rem;
}

.sein-kpi-value {
  color: var(--sein-ink);
  font-size: 2rem;
  line-height: 1.05;
  font-weight: 760;
}

.sein-kpi-note {
  color: var(--sein-muted);
  font-size: 0.78rem;
  margin-top: 0.48rem;
}

.sein-card {
  border-radius: 8px;
  border: 1px solid var(--sein-line);
  background: var(--sein-panel);
  padding: 1rem 1.1rem;
  box-shadow: 0 8px 24px rgba(24, 34, 53, 0.05);
  margin: 0.8rem 0;
}

.sein-card-title {
  color: var(--sein-ink);
  font-weight: 740;
  margin-bottom: 0.35rem;
}

.sein-card-body {
  color: #3c4858;
  line-height: 1.56;
  font-size: 0.94rem;
}

.sein-card.info {
  border-left: 4px solid var(--sein-teal);
}

.sein-card.warning {
  border-left: 4px solid var(--sein-amber);
  background: #fffaf1;
}

.sein-card.success {
  border-left: 4px solid var(--sein-green);
}

.sein-card.danger {
  border-left: 4px solid var(--sein-red);
  background: #fff7f6;
}

.sein-card.neutral {
  border-left: 4px solid #9aa4b2;
}

.sein-decision-card {
  display: grid;
  grid-template-columns: minmax(180px, 0.72fr) minmax(0, 1.28fr);
  gap: 1rem;
  border-radius: 8px;
  border: 1px solid var(--sein-line);
  background: var(--sein-panel);
  box-shadow: 0 10px 28px rgba(24, 34, 53, 0.055);
  margin: 1rem 0;
  overflow: hidden;
}

.sein-decision-band {
  padding: 1rem;
  color: #ffffff;
  background: var(--sein-navy);
}

.sein-decision-band.priority-a {
  background: var(--sein-red);
}

.sein-decision-band.priority-b {
  background: var(--sein-amber);
}

.sein-decision-band.watchlist {
  background: var(--sein-blue);
}

.sein-decision-band.monitor {
  background: #667085;
}

.sein-decision-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 760;
  opacity: 0.88;
}

.sein-decision-value {
  font-size: 1.7rem;
  font-weight: 800;
  line-height: 1.05;
  margin-top: 0.45rem;
}

.sein-decision-score {
  margin-top: 0.85rem;
  font-size: 0.88rem;
  line-height: 1.35;
}

.sein-decision-body {
  padding: 1rem 1.05rem;
}

.sein-decision-body h4 {
  margin: 0 0 0.35rem 0;
  color: var(--sein-ink);
}

.sein-decision-body p {
  margin: 0.25rem 0 0.7rem 0;
  color: #3c4858;
  line-height: 1.48;
  font-size: 0.93rem;
}

.sein-scope-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.7rem;
  margin: 0.8rem 0;
}

.sein-scope-card {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.9rem 0.95rem;
  min-height: 148px;
  box-shadow: 0 8px 22px rgba(24, 34, 53, 0.04);
}

.sein-scope-card.use {
  border-top: 4px solid var(--sein-green);
}

.sein-scope-card.limit {
  border-top: 4px solid var(--sein-amber);
}

.sein-scope-card.next {
  border-top: 4px solid var(--sein-teal);
}

.sein-scope-title {
  color: var(--sein-ink);
  font-size: 0.86rem;
  font-weight: 760;
  margin-bottom: 0.35rem;
}

.sein-scope-body {
  color: #435063;
  font-size: 0.84rem;
  line-height: 1.45;
}

.sein-definition-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.7rem;
  margin: 0.8rem 0 1rem 0;
}

.sein-definition-card {
  background: #f8fafc;
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.85rem 0.9rem;
}

.sein-definition-title {
  color: var(--sein-navy);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin-bottom: 0.32rem;
}

.sein-definition-body {
  color: #435063;
  font-size: 0.84rem;
  line-height: 1.45;
}

.sein-meta-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.6rem;
  margin: 0.8rem 0 1rem 0;
}

.sein-meta-item {
  background: #edf3f7;
  border: 1px solid #d4dee8;
  border-left: 4px solid var(--sein-blue);
  border-radius: 8px;
  padding: 0.68rem 0.78rem;
  min-height: 74px;
}

.sein-meta-label {
  color: var(--sein-muted);
  font-size: 0.7rem;
  font-weight: 720;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 0.28rem;
}

.sein-meta-value {
  color: var(--sein-ink);
  font-size: 0.92rem;
  line-height: 1.22;
  font-weight: 720;
}

.sein-context-panel {
  display: grid;
  grid-template-columns: minmax(300px, 0.95fr) minmax(520px, 1.65fr);
  gap: 0.9rem;
  align-items: stretch;
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(24, 34, 53, 0.045);
  margin: 0.85rem 0 1rem 0;
  padding: 0.85rem;
}

.sein-context-copy {
  border-left: 4px solid var(--sein-blue);
  background: #edf3f7;
  border-radius: 8px;
  padding: 0.85rem 0.95rem;
}

.sein-context-eyebrow {
  color: var(--sein-muted);
  font-size: 0.7rem;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: 0.065em;
  margin-bottom: 0.35rem;
}

.sein-context-title {
  color: var(--sein-ink);
  font-size: 1.05rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 0.35rem;
}

.sein-context-body {
  color: #435063;
  font-size: 0.86rem;
  line-height: 1.45;
}

.sein-context-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.55rem;
}

.sein-context-stat {
  background: #fbfcfe;
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.78rem 0.82rem;
  min-height: 88px;
}

.sein-context-stat strong {
  display: block;
  color: var(--sein-ink);
  font-size: 1.55rem;
  line-height: 1.05;
  margin-bottom: 0.38rem;
}

.sein-compact-context {
  display: grid;
  grid-template-columns: minmax(300px, 0.9fr) minmax(0, 2.1fr);
  gap: 0.75rem;
  margin: 0.8rem 0 1rem 0;
}

.sein-context-stat span {
  display: block;
  color: var(--sein-muted);
  font-size: 0.7rem;
  font-weight: 720;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1.25;
}

.sein-context-stat em {
  display: block;
  color: #526173;
  font-size: 0.75rem;
  font-style: normal;
  margin-top: 0.3rem;
}

.sein-matrix-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.7rem;
  margin: 0.8rem 0 1rem 0;
}

.sein-matrix-card {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.85rem 0.9rem;
  min-height: 138px;
  box-shadow: 0 8px 22px rgba(24, 34, 53, 0.04);
}

.sein-matrix-card.high {
  border-top: 4px solid var(--sein-red);
}

.sein-matrix-card.local {
  border-top: 4px solid var(--sein-amber);
}

.sein-matrix-card.system {
  border-top: 4px solid var(--sein-blue);
}

.sein-matrix-card.monitor {
  border-top: 4px solid #9aa4b2;
}

.sein-matrix-title {
  color: var(--sein-ink);
  font-size: 0.88rem;
  font-weight: 760;
  line-height: 1.25;
  margin-bottom: 0.35rem;
}

.sein-matrix-body {
  color: #435063;
  font-size: 0.82rem;
  line-height: 1.42;
}

[data-testid="stPlotlyChart"] {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.65rem 0.7rem 0.2rem 0.7rem;
  box-shadow: 0 8px 24px rgba(24, 34, 53, 0.045);
}

[data-testid="stDataFrame"] {
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(24, 34, 53, 0.04);
}

.stMultiSelect [data-baseweb="select"] > div,
.stSelectbox [data-baseweb="select"] > div {
  border-radius: 8px;
  border-color: #cbd6e2;
  background: #fbfcfe;
}

.stMultiSelect [data-baseweb="tag"] {
  background: #e5f2f7;
  border: 1px solid #b7d7e1;
}

.stMultiSelect [data-baseweb="tag"] span {
  color: #173b57;
  font-weight: 650;
}

.stDownloadButton button,
.stButton button {
  border-radius: 8px;
  border: 1px solid var(--sein-navy);
  background: var(--sein-navy);
  color: white;
  font-weight: 650;
}

.stDownloadButton button:hover,
.stButton button:hover {
  border-color: var(--sein-teal);
  background: var(--sein-teal);
  color: white;
}

div[data-testid="stMetric"] {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.8rem 0.9rem;
  box-shadow: 0 8px 22px rgba(24, 34, 53, 0.045);
}

@media (max-width: 900px) {
  .sein-meta-strip,
  .sein-context-panel,
  .sein-compact-context,
  .sein-matrix-grid,
  .sein-scope-grid,
  .sein-definition-grid,
  .sein-insight-grid,
  .sein-exec-kpi-strip,
  .sein-flow-panel,
  .sein-flow-steps,
  .sein-use-grid,
  .sein-taxonomy-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sein-context-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sein-decision-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  .sein-meta-strip,
  .sein-context-panel,
  .sein-compact-context,
  .sein-matrix-grid,
  .sein-scope-grid,
  .sein-definition-grid,
  .sein-insight-grid,
  .sein-exec-kpi-strip,
  .sein-flow-panel,
  .sein-flow-steps,
  .sein-use-grid,
  .sein-taxonomy-grid {
    grid-template-columns: 1fr;
  }

  .sein-context-stats {
    grid-template-columns: 1fr;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )
