"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  Button,
  Card,
  Chip,
  Label,
  ListBox,
  Modal,
  Select,
  Table,
  TextArea,
} from "@heroui/react";
import sample from "../../examples/dashboard/workspace.json";
import { THEMES, resolveTheme, type ThemeId } from "../lib/themes";
import {
  COSTS,
  LABELS,
  STAGES,
  metrics,
  validateWorkspace,
  parseWorkspace,
  type Cohort,
  type Workspace,
} from "../lib/workspace";

type View =
  "overview" | "funnel" | "economics" | "experiments" | "delivery" | "sources";
const NAV: { id: View; label: string; icon: string }[] = [
  { id: "overview", label: "Overview", icon: "grid" },
  { id: "funnel", label: "Growth funnel", icon: "funnel" },
  { id: "economics", label: "Unit economics", icon: "chart" },
  { id: "experiments", label: "Experiments", icon: "flask" },
  { id: "delivery", label: "Delivery plan", icon: "layers" },
  { id: "sources", label: "Data sources", icon: "database" },
];
const COST_LABELS = {
  acquisition_cost: "Acquisition",
  credit_loss: "Credit loss",
  funding_cost: "Funding",
  servicing_cost: "Servicing",
  incentives: "Incentives",
};
function Icon({ name, className = "" }: { name: string; className?: string }) {
  const paths: Record<string, React.ReactNode> = {
    grid: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="1.3" />
        <rect x="14" y="3" width="7" height="7" rx="1.3" />
        <rect x="3" y="14" width="7" height="7" rx="1.3" />
        <rect x="14" y="14" width="7" height="7" rx="1.3" />
      </>
    ),
    funnel: (
      <>
        <path d="M3 4h18l-7 8v7l-4 2v-9z" />
      </>
    ),
    chart: (
      <>
        <path d="M4 3v17h17M8 15l4-5 4 2 5-7" />
      </>
    ),
    flask: (
      <>
        <path d="M9 3h6M10 3v7l-6 9a1.5 1.5 0 0 0 1.3 2h13.4a1.5 1.5 0 0 0 1.3-2l-6-9V3M8 15h8" />
      </>
    ),
    layers: (
      <>
        <path d="m12 3 10 5-10 5L2 8zm-10 9 10 5 10-5M2 16l10 5 10-5" />
      </>
    ),
    database: (
      <>
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0" />
      </>
    ),
    upload: (
      <>
        <path d="M12 16V3m-5 5 5-5 5 5M4 15v6h16v-6" />
      </>
    ),
    arrow: (
      <>
        <path d="M4 12h15m-6-6 6 6-6 6" />
      </>
    ),
    check: <path d="m5 12 4 4L19 6" />,
    download: (
      <>
        <path d="M12 3v13m-5-5 5 5 5-5M4 16v5h16v-5" />
      </>
    ),
  };
  return (
    <svg
      className={`icon ${className}`}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.65"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[name] || paths.grid}
    </svg>
  );
}
const num = (v: number) => new Intl.NumberFormat("en-US").format(v);
const pct = (v: number | null) =>
  v === null ? "Unknown" : `${(v * 100).toFixed(1)}%`;
const money = (v: number | null, currency: string) =>
  v === null
    ? "Unknown"
    : `${currency} ${new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v)}`;
function download(value: unknown, filename: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(value, null, 2)], { type: "application/json" }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function Pill({
  children,
  tone = "neutral",
}: {
  children: React.ReactNode;
  tone?: string;
}) {
  return (
    <Chip size="sm" className={`pill ${tone}`} variant="soft">
      {children}
    </Chip>
  );
}
function Panel({
  title,
  detail,
  children,
  action,
}: {
  title: string;
  detail?: string;
  children: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <Card className="panel">
      <Card.Header className="panel-header">
        <div>
          <Card.Title>{title}</Card.Title>
          {detail && <Card.Description>{detail}</Card.Description>}
        </div>
        {action}
      </Card.Header>
      <Card.Content>{children}</Card.Content>
    </Card>
  );
}
function DataTable({
  headers,
  rows,
  label,
}: {
  headers: string[];
  rows: React.ReactNode[][];
  label: string;
}) {
  const columns = headers.map((title, i) => ({
    id: "column-" + i,
    title,
    index: i,
  }));
  const items = rows.map((cells, i) => ({ id: "row-" + i, cells }));
  return (
    <Table className="data-table">
      <Table.ScrollContainer>
        <Table.Content aria-label={label}>
          <Table.Header columns={columns}>
            {(column) => (
              <Table.Column id={column.id} isRowHeader={column.index === 0}>
                {column.title}
              </Table.Column>
            )}
          </Table.Header>
          <Table.Body items={items}>
            {(row) => (
              <Table.Row id={row.id} columns={columns}>
                {(column) => <Table.Cell>{row.cells[column.index]}</Table.Cell>}
              </Table.Row>
            )}
          </Table.Body>
        </Table.Content>
      </Table.ScrollContainer>
    </Table>
  );
}
function FunnelChart({
  cohort,
  compact = false,
}: {
  cohort: Cohort;
  compact?: boolean;
}) {
  return (
    <div className={`funnel-chart ${compact ? "compact" : ""}`}>
      {STAGES.slice(0, 7).map((stage, index) => {
        const previous = index ? cohort.counts[STAGES[index - 1]] : null;
        return (
          <div className="funnel-row" key={stage}>
            <div className="funnel-caption">
              <span>{LABELS[stage]}</span>
              <strong>{num(cohort.counts[stage])}</strong>
            </div>
            <div className="bar-track">
              <div
                className={`bar-fill bar-${index}`}
                style={{
                  width: `${cohort.counts.acquired ? (cohort.counts[stage] / cohort.counts.acquired) * 100 : 0}%`,
                }}
              />
            </div>
            <span className="bar-rate">
              {previous === null
                ? "Entry"
                : pct(previous ? cohort.counts[stage] / previous : null)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
function LeaderCard({
  kind,
  cohort,
}: {
  kind: "count" | "rate";
  cohort: Cohort;
}) {
  const m = metrics(cohort);
  const leaders = kind === "count" ? m.countLeaders : m.rateLeaders;
  return (
    <div className="leader-card">
      <span className="eyebrow">
        {kind === "count" ? "LARGEST COUNT GAP" : "LOWEST CONVERSION"}
      </span>
      <h3>
        {leaders.length
          ? leaders
              .map((s) => `${LABELS[s.from]} → ${LABELS[s.to]}`)
              .join(" · ")
          : "No observed leader"}
      </h3>
      <strong>
        {leaders.length
          ? kind === "count"
            ? `${num(leaders[0].not_progressed)} people`
            : pct(leaders[0].conversion)
          : "Unknown"}
      </strong>
      <p>
        {kind === "count"
          ? "People not yet in the next stage; reasons still need evidence."
          : "Approval includes policy decisions. A lower rate is not proof of friction."}
      </p>
    </div>
  );
}
export default function Dashboard() {
  const [theme, setTheme] = useState<ThemeId>("default");
  const [themeReady, setThemeReady] = useState(false);
  useEffect(() => {
    try {
      setTheme(resolveTheme(localStorage.getItem("fingrowth-theme")));
    } catch {
      /* Browser storage may be unavailable. */
    }
    setThemeReady(true);
  }, []);
  useEffect(() => {
    document.documentElement.dataset.brand = theme;
    if (themeReady) {
      try {
        localStorage.setItem("fingrowth-theme", theme);
      } catch {
        /* Theme remains usable without persistence. */
      }
    }
  }, [theme, themeReady]);

  const [workspace, setWorkspace] = useState<Workspace>(() =>
    validateWorkspace(sample),
  );
  const [selected, setSelected] = useState("0");
  const [view, setView] = useState<View>("overview");
  const [importOpen, setImportOpen] = useState(false),
    [draft, setDraft] = useState(""),
    [error, setError] = useState(""),
    [notice, setNotice] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  const cohort = workspace.cohorts[Number(selected)] ?? workspace.cohorts[0];
  const m = useMemo(() => metrics(cohort), [cohort]);
  const active = NAV.find((v) => v.id === view)!;
  function importText(text: string) {
    try {
      const next = parseWorkspace(text);
      setWorkspace(next);
      setSelected("0");
      setImportOpen(false);
      setError("");
      setDraft("");
      setNotice(`Loaded ${next.name}. Data stays in this browser tab.`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to read workspace.");
    }
  }
  async function importFile(file: File | undefined) {
    if (!file) return;
    if (file.size > 2_000_000) {
      setError("File exceeds the 2 MB workspace limit.");
      return;
    }
    try {
      importText(await file.text());
    } catch {
      setError("Unable to read file. Choose a JSON workspace.");
    }
    if (fileRef.current) fileRef.current.value = "";
  }
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/" aria-label="FinGrowth home">
          <span className="brand-mark">
            <span />
            <span />
            <span />
          </span>
          <span>
            FinGrowth<span className="brand-dot">.</span>
          </span>
        </a>
        <div className="workspace-label">
          <span className="workspace-avatar">FG</span>
          <div>
            <strong>Growth workspace</strong>
            <span>Consumer fintech</span>
          </div>
          <span className="tiny-chevron">⌄</span>
        </div>
        <div className="nav-title">WORKSPACE</div>
        <nav aria-label="Workspace sections">
          {NAV.map((item) => (
            <Button
              key={item.id}
              variant="ghost"
              className={`nav-button ${view === item.id ? "active" : ""}`}
              aria-current={view === item.id ? "page" : undefined}
              onPress={() => setView(item.id)}
            >
              <Icon name={item.icon} />
              {item.label}
              {item.id === "experiments" && (
                <span className="nav-count">
                  {workspace.experiments.length}
                </span>
              )}
            </Button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="skill-connection">
            <span className="status-dot" />
            <strong>Powered by Skills</strong>
            <p>
              One data contract.
              <br />
              Your growth engineering workflow.
            </p>
            <Button
              variant="ghost"
              size="sm"
              onPress={() => setView("sources")}
            >
              Explore data sources <Icon name="arrow" />
            </Button>
          </div>
          <div className="version">
            <span>FG / OPEN SOURCE</span>
            <span>v0.1.0</span>
          </div>
        </div>
      </aside>
      <div className="main-shell">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> <strong>{active.label}</strong>
          </div>
          <div className="topbar-right">
            <Select
              aria-label="UI theme"
              className="theme-select"
              value={theme}
              onChange={(value) => setTheme(resolveTheme(value))}
            >
              <Select.Trigger>
                <Select.Value />
                <Select.Indicator />
              </Select.Trigger>
              <Select.Popover>
                <ListBox aria-label="Technology company themes">
                  {THEMES.map((item) => (
                    <ListBox.Item
                      key={item.id}
                      id={item.id}
                      textValue={item.label}
                    >
                      <span
                        className="theme-swatch"
                        aria-hidden="true"
                        style={{ backgroundColor: item.accent }}
                      />
                      {item.label}
                      <ListBox.ItemIndicator />
                    </ListBox.Item>
                  ))}
                </ListBox>
              </Select.Popover>
            </Select>

            <span className="local-status">
              <span className="status-dot" /> Browser-local workspace
            </span>
            <span className="user-avatar">S</span>
          </div>
        </header>
        <main id="main-content">
          <div className="page-heading">
            <div>
              <div className="heading-eyebrow">GROWTH ENGINEERING</div>
              <h1>{active.label}</h1>
              <p>
                {view === "overview"
                  ? "Connect acquisition, customer journeys and risk-adjusted value."
                  : view === "sources"
                    ? "Bring your own data. Keep its origin and definitions visible."
                    : view === "funnel"
                      ? "Find investigation priorities before choosing a fix."
                      : view === "economics"
                        ? "Measure growth after acquisition cost and credit loss."
                        : view === "experiments"
                          ? "Turn a hypothesis into a reviewable decision."
                          : "Connect every initiative to an owner and acceptance check."}
              </p>
            </div>
            <Button
              className="import-button"
              onPress={() => {
                setError("");
                setImportOpen(true);
              }}
            >
              <Icon name="upload" /> Import workspace
            </Button>
          </div>
          {notice && (
            <div className="notice" role="status">
              {notice}
              <Button
                variant="ghost"
                size="sm"
                onPress={() => setNotice("")}
                aria-label="Dismiss notification"
              >
                ×
              </Button>
            </div>
          )}
          <div className="context-bar">
            <div className="context-meta">
              <Pill
                tone={workspace.data_mode === "synthetic" ? "sage" : "amber"}
              >
                {workspace.data_mode === "synthetic"
                  ? "Synthetic demo"
                  : "Declared approved aggregate"}
              </Pill>
              <span>{workspace.name}</span>
              <span className="context-divider" />
              <span>{cohort.window.replace("/", " → ")}</span>
            </div>
            <Select
              aria-label="Select cohort"
              className="cohort-select"
              value={selected}
              onChange={(value) => setSelected(String(value ?? "0"))}
            >
              <Select.Trigger>
                <Select.Value />
                <Select.Indicator />
              </Select.Trigger>
              <Select.Popover>
                <ListBox aria-label="Cohorts">
                  {workspace.cohorts.map((item, i) => (
                    <ListBox.Item
                      id={String(i)}
                      key={i}
                      textValue={item.cohort}
                    >
                      {item.cohort}
                      <ListBox.ItemIndicator />
                    </ListBox.Item>
                  ))}
                </ListBox>
              </Select.Popover>
            </Select>
          </div>
          {view === "overview" && (
            <>
              <div className="kpi-grid">
                {[
                  {
                    label: "First-funded people",
                    value: num(cohort.counts.disbursed),
                    detail: "Unique people · selected cohort",
                    icon: "funnel",
                  },
                  {
                    label: "Funded CAC",
                    value: money(m.funded_cac, cohort.currency),
                    detail: "Acquisition spend / first funded",
                    icon: "chart",
                  },
                  {
                    label: "Contribution",
                    value: money(m.contribution, cohort.currency),
                    detail: cohort.mature
                      ? "Conditional on declared maturity"
                      : "Awaiting mature outcomes",
                    icon: "layers",
                  },
                  {
                    label: "Acquired → funded",
                    value: pct(
                      cohort.counts.acquired
                        ? cohort.counts.disbursed / cohort.counts.acquired
                        : null,
                    ),
                    detail: "Full journey conversion",
                    icon: "check",
                  },
                ].map((item, i) => (
                  <Card
                    key={item.label}
                    className={`kpi-card ${i === 2 ? "featured" : ""}`}
                  >
                    <Card.Content>
                      <div className="kpi-label">
                        {item.label}
                        <Icon name={item.icon} />
                      </div>
                      <div
                        className={`kpi-value ${i === 2 && m.contribution !== null && m.contribution < 0 ? "negative" : ""}`}
                      >
                        {item.value}
                      </div>
                      <p>{item.detail}</p>
                    </Card.Content>
                  </Card>
                ))}
              </div>
              <div className="overview-grid">
                <Panel
                  title="From acquisition to funding"
                  detail="Nested people · step conversion at right"
                  action={
                    <Button
                      variant="ghost"
                      size="sm"
                      onPress={() => setView("funnel")}
                    >
                      View funnel <Icon name="arrow" />
                    </Button>
                  }
                >
                  <FunnelChart cohort={cohort} compact />
                </Panel>
                <Panel
                  title="Investigate before you optimize"
                  detail="Two rankings. Two different questions."
                >
                  <div className="leaders">
                    <LeaderCard kind="count" cohort={cohort} />
                    <LeaderCard kind="rate" cohort={cohort} />
                  </div>
                  <div className="insight-note">
                    <span className="mini-spark">✦</span>
                    <p>
                      Conversion shows where people stop progressing. Evidence
                      explains why.
                    </p>
                  </div>
                </Panel>
              </div>
              <div className="lower-grid">
                <Panel
                  title="Channel economics"
                  detail="Separate cohort snapshots · descriptive comparisons only"
                >
                  <DataTable
                    label="Channel economics"
                    headers={[
                      "Cohort",
                      "First funded",
                      "Funded CAC",
                      "Contribution",
                    ]}
                    rows={workspace.cohorts.map((c) => {
                      const values = metrics(c);
                      return [
                        <strong key="name">{c.cohort}</strong>,
                        num(c.counts.disbursed),
                        money(values.funded_cac, c.currency),
                        <span
                          key="value"
                          className={
                            values.contribution !== null &&
                            values.contribution < 0
                              ? "negative"
                              : "positive"
                          }
                        >
                          {money(values.contribution, c.currency)}
                        </span>,
                      ];
                    })}
                  />
                  <p className="footnote">
                    Compare only after aligning populations, currency,
                    attribution, risk mix and maturity. Lower CAC alone does not
                    establish a winner.
                  </p>
                </Panel>
                <Panel
                  title="Next decisions"
                  detail="Planning entries supplied with this workspace"
                  action={
                    <Button
                      variant="ghost"
                      size="sm"
                      onPress={() => setView("experiments")}
                    >
                      All <Icon name="arrow" />
                    </Button>
                  }
                >
                  <div className="decision-list">
                    {workspace.experiments.slice(0, 2).map((item) => (
                      <div key={item.id}>
                        <Pill tone="amber">{item.status}</Pill>
                        <h3>{item.title}</h3>
                        <p>{item.next_action}</p>
                      </div>
                    ))}
                    {!workspace.experiments.length && (
                      <p className="empty">
                        No experiment plans supplied. Use the experiment-design
                        Skill to add a reviewable card.
                      </p>
                    )}
                  </div>
                </Panel>
              </div>
            </>
          )}
          {view === "funnel" && (
            <>
              <div className="overview-grid">
                <Panel
                  title="Acquisition → first funding"
                  detail="Counts describe observed progression, not recoverable uplift"
                >
                  <FunnelChart cohort={cohort} />
                </Panel>
                <Panel title="Investigation priorities">
                  <div className="leaders">
                    <LeaderCard kind="count" cohort={cohort} />
                    <LeaderCard kind="rate" cohort={cohort} />
                  </div>
                </Panel>
              </div>
              <Panel
                title="Journey measurement"
                detail="Policy decisions, pending work and technical errors need separate reason codes"
              >
                <DataTable
                  label="Funnel transitions"
                  headers={[
                    "Transition",
                    "Population",
                    "Progressed",
                    "Not progressed",
                    "Conversion",
                  ]}
                  rows={m.steps.map((step) => [
                    `${LABELS[step.from]} → ${LABELS[step.to]}`,
                    num(step.population),
                    num(step.converted),
                    num(step.not_progressed),
                    pct(step.conversion),
                  ])}
                />
                <div className="callout">
                  Repayment and repeat are delayed outcomes. Their complements
                  do not establish default or churn, and they are excluded from
                  onboarding priorities.
                </div>
              </Panel>
            </>
          )}
          {view === "economics" && (
            <>
              <div className="overview-grid">
                <Panel
                  title="Contribution bridge"
                  detail={`${cohort.currency} · same cohort and observation horizon`}
                >
                  <div className="economics-bars">
                    {[
                      {
                        label: "Recognized revenue",
                        value: cohort.revenue,
                        positive: true,
                      },
                      ...m.costs.map((item) => ({
                        label: COST_LABELS[item.key],
                        value: item.amount,
                        positive: false,
                      })),
                    ].map((item) => (
                      <div key={item.label}>
                        <div>
                          <span>{item.label}</span>
                          <strong>
                            {item.positive ? "" : "− "}
                            {money(item.value, cohort.currency)}
                          </strong>
                        </div>
                        <div className="bar-track">
                          <div
                            className={`bar-fill ${item.positive ? "" : "cost-fill"}`}
                            style={{
                              width: `${Math.max(cohort.revenue, ...m.costs.map((c) => c.amount)) ? (item.value / Math.max(cohort.revenue, ...m.costs.map((c) => c.amount))) * 100 : 0}%`,
                            }}
                          />
                        </div>
                      </div>
                    ))}
                    <div className="contribution-total">
                      <span>Contribution</span>
                      <strong
                        className={
                          m.contribution !== null && m.contribution < 0
                            ? "negative"
                            : "positive"
                        }
                      >
                        {money(m.contribution, cohort.currency)}
                      </strong>
                    </div>
                  </div>
                </Panel>
                <Panel title="The metric contract">
                  <div className="definition-list">
                    <div>
                      <span>Population</span>
                      <strong>Nested first-loan people</strong>
                    </div>
                    <div>
                      <span>Window</span>
                      <strong>{cohort.window}</strong>
                    </div>
                    <div>
                      <span>Observed through</span>
                      <strong>{cohort.outcome_as_of}</strong>
                    </div>
                    <div>
                      <span>Maturity</span>
                      <Pill tone="amber">
                        {cohort.mature
                          ? "Declared · not independently verified"
                          : "Immature · contribution unknown"}
                      </Pill>
                    </div>
                  </div>
                  <div className="callout">
                    Principal is not revenue. Subtract one loss measure per
                    exposure; do not add expected and realized loss on the same
                    exposure.
                  </div>
                  <p className="footnote">
                    The dashboard uses bounded amounts and integer cents. It is
                    a planning view, not a financial ledger.
                  </p>
                </Panel>
              </div>
            </>
          )}
          {view === "experiments" && (
            <div className="plan-grid">
              {workspace.experiments.map((item, index) => (
                <Card key={item.id} className="panel experiment-card">
                  <Card.Header>
                    <div className="card-topline">
                      <span className="item-index">
                        EXP / {String(index + 1).padStart(2, "0")}
                      </span>
                      <Pill tone="amber">{item.status}</Pill>
                    </div>
                    <Card.Title>{item.title}</Card.Title>
                    <Card.Description>{item.hypothesis}</Card.Description>
                  </Card.Header>
                  <Card.Content>
                    <div className="experiment-field">
                      <span>PRIMARY METRIC</span>
                      <p>{item.primary_metric}</p>
                    </div>
                    <div className="experiment-field">
                      <span>GUARDRAILS & GATES</span>
                      <ul>
                        {item.guardrails.map((guard, i) => (
                          <li key={i}>{guard}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="next-action">
                      <span>NEXT ACTION</span>
                      <p>{item.next_action}</p>
                    </div>
                  </Card.Content>
                  <Card.Footer>
                    <span className="owner-badge">{item.owner}</span>
                    <span className="footnote">
                      Planning status · no launch action
                    </span>
                  </Card.Footer>
                </Card>
              ))}
              {!workspace.experiments.length && (
                <Panel title="No experiment plans yet">
                  <p>
                    Have the growth-experiment-design Skill produce a
                    hypothesis, ITT metric, guardrails and unresolved decision
                    gates, then include them in your workspace.
                  </p>
                </Panel>
              )}
            </div>
          )}
          {view === "delivery" && (
            <Panel
              title="From evidence to delivery"
              detail="Owner roles and statuses are supplied plans, not completed deployments"
            >
              <DataTable
                label="Delivery initiatives"
                headers={[
                  "Initiative",
                  "Owner",
                  "Status",
                  "Dependency",
                  "Acceptance check",
                ]}
                rows={workspace.initiatives.map((item, index) => [
                  <div key="title">
                    <span className="item-index">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <strong>{item.title}</strong>
                  </div>,
                  item.owner,
                  <Pill key="status" tone="sage">
                    {item.status}
                  </Pill>,
                  item.dependency,
                  item.acceptance,
                ])}
              />
              {!workspace.initiatives.length && (
                <p className="empty">
                  No initiatives supplied. Use the architecture Skill to define
                  source ownership and acceptance checks.
                </p>
              )}
            </Panel>
          )}
          {view === "sources" && (
            <>
              <div className="adapter-flow">
                <div>
                  <span>01</span>
                  <Icon name="database" />
                  <h3>Your data source</h3>
                  <p>
                    Approved aggregate export
                    <br />
                    CSV, SQL result or API output
                  </p>
                </div>
                <Icon name="arrow" />
                <div>
                  <span>02</span>
                  <Icon name="layers" />
                  <h3>Data adapter Skill</h3>
                  <p>
                    Map fields, validate populations
                    <br />
                    Preserve provenance and gaps
                  </p>
                </div>
                <Icon name="arrow" />
                <div>
                  <span>03</span>
                  <Icon name="grid" />
                  <h3>One growth workspace</h3>
                  <p>
                    Funnel, economics, experiments
                    <br />
                    and delivery in one view
                  </p>
                </div>
              </div>
              <Panel
                title="Source & measurement contract"
                action={
                  <Button
                    variant="outline"
                    size="sm"
                    onPress={() =>
                      download(workspace, "fingrowth-workspace.json")
                    }
                  >
                    <Icon name="download" /> Export workspace
                  </Button>
                }
              >
                <div className="definition-list source-definitions">
                  <div>
                    <span>Source</span>
                    <strong>{workspace.provenance.source}</strong>
                  </div>
                  <div>
                    <span>Extracted at</span>
                    <strong>{workspace.provenance.extracted_at}</strong>
                  </div>
                  <div>
                    <span>Timezone</span>
                    <strong>{workspace.provenance.timezone}</strong>
                  </div>
                  <div>
                    <span>Approval reference</span>
                    <strong>
                      {workspace.provenance.approval_reference ??
                        "Not applicable · synthetic fixture"}
                    </strong>
                  </div>
                </div>
                <div className="source-description">
                  <span>COHORT DEFINITION</span>
                  <p>{workspace.provenance.cohort_definition}</p>
                </div>
                <DataTable
                  label="Source field mapping"
                  headers={[
                    "Workspace field",
                    "Source field",
                    "Transformation",
                  ]}
                  rows={workspace.provenance.mappings.map((item) => [
                    item.target,
                    item.source,
                    item.transform,
                  ])}
                />
                <div className="callout">
                  Import validates shape and arithmetic assumptions. It cannot
                  establish privacy approval, source completeness or loan
                  maturity. Files stay in this tab; reload returns to the
                  synthetic demo.
                </div>
              </Panel>
              <div className="source-actions">
                <Button
                  variant="secondary"
                  onPress={() =>
                    download(sample, "fingrowth-demo-workspace.json")
                  }
                >
                  Download demo template <Icon name="download" />
                </Button>
                <Button
                  variant="ghost"
                  onPress={() => {
                    setWorkspace(validateWorkspace(sample));
                    setSelected("0");
                    setNotice("Synthetic demo restored.");
                  }}
                >
                  Restore synthetic demo
                </Button>
              </div>
            </>
          )}
          <footer className="page-footer">
            <span>
              <span className="status-dot" />{" "}
              {workspace.data_mode === "synthetic"
                ? "All demo data is invented."
                : "Aggregate approval is declared by the source owner."}{" "}
              No live actions.
            </span>
            <span>
              Observed through {cohort.outcome_as_of} · {cohort.currency}
            </span>
          </footer>
        </main>
      </div>
      <Modal isOpen={importOpen} onOpenChange={setImportOpen}>
        <Modal.Backdrop>
          <Modal.Container>
            <Modal.Dialog className="import-dialog">
              <Modal.CloseTrigger />
              <Modal.Header>
                <Modal.Heading>Bring your growth workspace</Modal.Heading>
                <p>
                  Use the data-adapter Skill to map an authorized aggregate
                  source into the workspace format.
                </p>
              </Modal.Header>
              <Modal.Body>
                <Button
                  variant="secondary"
                  onPress={() => fileRef.current?.click()}
                >
                  <Icon name="upload" /> Choose JSON file
                </Button>
                <input
                  ref={fileRef}
                  type="file"
                  accept="application/json,.json"
                  className="hidden"
                  aria-label="Workspace JSON file"
                  onChange={(e) => void importFile(e.target.files?.[0])}
                />
                <Label htmlFor="workspace-json">Or paste workspace JSON</Label>
                <TextArea
                  id="workspace-json"
                  className="json-input"
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  placeholder={'{ "schema_version": "1.0", ... }'}
                  aria-label="Workspace JSON"
                />
                <p className="footnote">
                  Up to 2 MB. No credentials or customer-level records. Import
                  does not transmit data or retain it after reload.
                </p>
                {error && (
                  <div className="error-message" role="alert">
                    {error}
                  </div>
                )}
              </Modal.Body>
              <Modal.Footer>
                <Button
                  variant="ghost"
                  onPress={() =>
                    download(sample, "fingrowth-demo-workspace.json")
                  }
                >
                  Get template
                </Button>
                <Button
                  isDisabled={!draft.trim()}
                  onPress={() => importText(draft)}
                >
                  Load workspace
                </Button>
              </Modal.Footer>
            </Modal.Dialog>
          </Modal.Container>
        </Modal.Backdrop>
      </Modal>
    </div>
  );
}
