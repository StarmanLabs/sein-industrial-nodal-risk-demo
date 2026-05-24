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
    linear-gradient(180deg, #f7f9fc 0%, #eef3f7 100%);
  color: var(--sein-ink);
}

[data-testid="stAppViewContainer"] > .main {
  background: transparent;
}

[data-testid="stHeader"] {
  background: rgba(245, 247, 250, 0.82);
  backdrop-filter: blur(8px);
}

[data-testid="stSidebar"] {
  background: #eef3f7;
  border-right: 1px solid var(--sein-line);
}

[data-testid="stSidebar"] h1 {
  font-size: 1.35rem;
  letter-spacing: 0;
  color: var(--sein-navy);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
  color: #4e5d70;
}

[data-testid="stSidebar"] a {
  border-radius: 8px;
  padding: 0.48rem 0.55rem;
}

[data-testid="stSidebar"] a:hover {
  background: #e1e9f0;
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
  max-width: 1400px;
  padding-top: 2.4rem;
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
  border: 1px solid #cfdbe7;
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(14, 47, 67, 0.98), rgba(22, 140, 140, 0.9)),
    radial-gradient(circle at 84% 18%, rgba(255,255,255,0.20), transparent 30%);
  color: #ffffff;
  padding: 1.35rem 1.45rem;
  margin: 0.35rem 0 1rem 0;
  box-shadow: 0 12px 32px rgba(24, 34, 53, 0.11);
}

.sein-exec-kpi-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.65rem;
  margin: 0.9rem 0 1rem 0;
}

.sein-exec-kpi {
  background: var(--sein-panel);
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.9rem 0.95rem;
  min-height: 104px;
  box-shadow: 0 8px 22px rgba(16, 32, 51, 0.045);
  position: relative;
  overflow: hidden;
}

.sein-exec-kpi::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 4px;
  width: 100%;
  background: var(--sein-blue);
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
  letter-spacing: 0.06em;
  margin-bottom: 0.36rem;
}

.sein-exec-kpi-value {
  color: var(--sein-ink);
  font-size: 2.05rem;
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
  display: grid;
  grid-template-columns: minmax(300px, 0.92fr) minmax(0, 1.8fr);
  gap: 0.85rem;
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 10px 26px rgba(16, 32, 51, 0.05);
  margin: 0.95rem 0 1.1rem 0;
  padding: 0.9rem;
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
  font-size: 1.18rem;
  line-height: 1.18;
  font-weight: 820;
  margin-bottom: 0.4rem;
}

.sein-flow-text {
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.45;
}

.sein-flow-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  overflow: hidden;
  background: #fbfcfe;
}

.sein-flow-step {
  display: grid;
  grid-template-columns: 38px minmax(0, 1fr);
  gap: 0.65rem;
  align-items: start;
  background: transparent;
  border-right: 1px solid var(--sein-line);
  padding: 0.95rem;
  min-height: 112px;
}

.sein-flow-step:last-child { border-right: 0; }

.sein-flow-number {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--sein-navy);
  color: #ffffff;
  font-weight: 800;
  font-size: 0.78rem;
}

.sein-flow-title {
  color: var(--sein-ink);
  font-size: 0.9rem;
  font-weight: 800;
  margin-bottom: 0.28rem;
}

.sein-flow-body {
  color: #475569;
  font-size: 0.82rem;
  line-height: 1.42;
}

.sein-use-panel {
  border-radius: 8px;
  border: 1px solid var(--sein-line);
  background: #ffffff;
  padding: 0.9rem 1rem;
  box-shadow: 0 8px 22px rgba(16, 32, 51, 0.04);
  margin: 0.9rem 0 1rem 0;
}

.sein-use-title {
  color: var(--sein-ink);
  font-size: 1rem;
  font-weight: 820;
  margin-bottom: 0.7rem;
}

.sein-use-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.7rem;
}

.sein-use-step {
  border-left: 4px solid var(--sein-blue);
  background: #f8fafc;
  border-radius: 8px;
  padding: 0.75rem 0.82rem;
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
  margin: 0;
}

.sein-taxonomy-panel {
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  background: #ffffff;
  padding: 0.95rem;
  box-shadow: 0 10px 26px rgba(16, 32, 51, 0.05);
  margin: 0.9rem 0 1rem 0;
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
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.65rem;
}

.sein-taxonomy-item {
  border: 1px solid var(--sein-line);
  border-radius: 8px;
  padding: 0.82rem 0.88rem;
  min-height: 122px;
  background: #fbfcfe;
}

.sein-taxonomy-item.urgent { border-top: 4px solid var(--sein-red); }
.sein-taxonomy-item.selective { border-top: 4px solid var(--sein-amber); }
.sein-taxonomy-item.watch { border-top: 4px solid var(--sein-teal); }
.sein-taxonomy-item.base { border-top: 4px solid var(--sein-muted); }

.sein-taxonomy-title {
  color: var(--sein-ink);
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
  border-radius: 8px;
  border: 1px solid #ead7b7;
  background: #fffaf1;
  color: #475569;
  padding: 0.78rem 0.9rem;
  font-size: 0.86rem;
  line-height: 1.44;
  margin: 0.9rem 0;
}

.sein-compact-note strong {
  color: #7a4d12;
}

.sein-hero-kicker {
  font-size: 0.74rem;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.86;
  margin-bottom: 0.34rem;
}

.sein-hero-title {
  font-size: clamp(1.65rem, 3.2vw, 2.55rem);
  line-height: 1.08;
  font-weight: 820;
  margin-bottom: 0.48rem;
}

.sein-hero-body {
  max-width: 980px;
  font-size: 1rem;
  line-height: 1.45;
  opacity: 0.94;
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
