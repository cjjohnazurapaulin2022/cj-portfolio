"use client";

export default function Services() {
  const services = [
    {
      title: "Executive Report",
      description: "A concise, decision-ready summary of your data — key findings, visualizations, and recommendations formatted for stakeholders and leadership.",
      turnaround: "2–4 days",
      bestFor: "Business owners and managers who need clear answers fast without the technical deep-dive.",
    },
    {
      title: "Full Project & Analysis Report",
      description: "End-to-end analysis covering Descriptive, Diagnostic, Prescriptive, and Predictive layers. Includes Python code, visualizations, and a written report.",
      turnaround: "7–14 days",
      bestFor: "Businesses with complex data questions needing rigorous, documented analysis.",
    },
    {
      title: "Data Cleaning & Preprocessing",
      description: "Messy or incomplete data transformed into a clean, analysis-ready dataset with full documentation of all changes made.",
      turnaround: "1–3 days",
      bestFor: "Anyone with raw data that needs preparing before analysis or visualization.",
    },
    {
      title: "Statistical Report",
      description: "Hypothesis testing, correlation analysis, regression, and significance testing with plain-language interpretation of results.",
      turnaround: "3–6 days",
      bestFor: "Researchers, students, and businesses needing statistically valid answers.",
    },
    {
      title: "Machine Learning Report",
      description: "Supervised or unsupervised ML models with performance evaluation, feature importance analysis, and business interpretation.",
      turnaround: "7–14 days",
      bestFor: "Businesses exploring predictive analytics or customer segmentation.",
    },
  ];

  const deliverables = [
    { icon: "📊", label: "Clean, documented dataset" },
    { icon: "📓", label: "Python notebook with full code" },
    { icon: "📄", label: "Written report or executive summary" },
    { icon: "📈", label: "Charts and visualizations" },
    { icon: "💡", label: "Actionable recommendations" },
    { icon: "🔁", label: "One round of revisions included" },
  ];

  const clients = [
    { icon: "🏢", label: "Small to medium businesses needing data-driven clarity" },
    { icon: "📣", label: "Marketing teams wanting to understand campaign performance" },
    { icon: "🛒", label: "E-commerce owners tracking customer behavior and revenue" },
    { icon: "🎓", label: "Students and researchers needing statistical analysis" },
    { icon: "🚀", label: "Startups without a dedicated in-house analyst" },
    { icon: "🌏", label: "Remote and local clients — Philippines and worldwide" },
  ];

  const faqs = [
    {
      q: "What data formats do you accept?",
      a: "CSV, Excel (.xlsx), JSON, SQL databases, and Google Sheets. If you have something else, just ask.",
    },
    {
      q: "Do you work with my existing tools?",
      a: "Yes. I primarily use Python and can deliver outputs compatible with Excel, Power BI, or Tableau.",
    },
    {
      q: "What if I do not know exactly what I need?",
      a: "That is what the briefing call is for. You describe your problem and I will recommend the right service.",
    },
    {
      q: "Do you offer revisions?",
      a: "Yes — one round of revisions is included in every service. Additional revisions can be arranged.",
    },
    {
      q: "Can you work with sensitive or confidential data?",
      a: "Yes. I treat all client data as strictly confidential. We can sign an NDA before starting if needed.",
    },
  ];

  const cardStyle = {
    border: "1px solid rgba(128,128,128,0.2)",
    borderRadius: "12px",
    padding: "24px",
  };

  const labelStyle = {
    fontSize: "0.75rem",
    fontWeight: 600,
    opacity: 0.5,
    textTransform: "uppercase" as const,
    letterSpacing: "0.05em",
  };

  return (
    <main style={{ maxWidth: "860px", margin: "0 auto", padding: "60px 24px", fontFamily: "inherit" }}>

      <section style={{ marginBottom: "64px" }}>
        <h1 style={{ fontSize: "2.5rem", fontWeight: 700, marginBottom: "16px" }}>
          Data Analytics Services
        </h1>
        <p style={{ fontSize: "1.15rem", lineHeight: 1.7, opacity: 0.8, maxWidth: "640px" }}>
          I help businesses and individuals turn raw data into clear, actionable insights.
          Available for both remote and local clients.
        </p>
      </section>

      <section style={{ marginBottom: "64px" }}>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "32px" }}>
          What I Offer
        </h2>
        <div style={{ display: "grid", gap: "24px" }}>
          {services.map((service, i) => (
            <div key={i} style={cardStyle}>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "10px" }}>
                {service.title}
              </h3>
              <p style={{ opacity: 0.8, lineHeight: 1.7, marginBottom: "16px" }}>
                {service.description}
              </p>
              <div style={{ display: "flex", gap: "32px", flexWrap: "wrap" as const }}>
                <div>
                  <span style={labelStyle}>Turnaround</span>
                  <p style={{ marginTop: "4px", fontWeight: 600 }}>{service.turnaround}</p>
                </div>
                <div style={{ flex: 1, minWidth: "200px" }}>
                  <span style={labelStyle}>Best For</span>
                  <p style={{ marginTop: "4px", opacity: 0.8 }}>{service.bestFor}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section style={{ marginBottom: "64px" }}>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "24px" }}>
          What You Get
        </h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "16px" }}>
          {deliverables.map((item, i) => (
            <div key={i} style={{ ...cardStyle, display: "flex", alignItems: "center", gap: "12px" }}>
              <span style={{ fontSize: "1.5rem" }}>{item.icon}</span>
              <span style={{ fontWeight: 500 }}>{item.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section style={{ marginBottom: "64px" }}>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "24px" }}>
          Who This Is For
        </h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "16px" }}>
          {clients.map((item, i) => (
            <div key={i} style={{ ...cardStyle, display: "flex", alignItems: "flex-start", gap: "12px" }}>
              <span style={{ fontSize: "1.5rem" }}>{item.icon}</span>
              <span style={{ opacity: 0.85, lineHeight: 1.6 }}>{item.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section style={{ marginBottom: "64px" }}>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "12px" }}>
          Pricing
        </h2>
        <p style={{ opacity: 0.7, lineHeight: 1.7 }}>
          Pricing depends on the scope, complexity, and timeline of your project.
          Book a free 30-minute briefing call and I will give you a clear quote after
          understanding your specific needs.
        </p>
      </section>

      <section style={{ marginBottom: "64px" }}>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "24px" }}>
          Frequently Asked Questions
        </h2>
        <div style={{ display: "grid", gap: "16px" }}>
          {faqs.map((item, i) => (
            <div key={i} style={cardStyle}>
              <p style={{ fontWeight: 700, marginBottom: "8px" }}>{item.q}</p>
              <p style={{ opacity: 0.8, lineHeight: 1.7 }}>{item.a}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{
        ...cardStyle,
        borderRadius: "16px",
        padding: "48px 32px",
        textAlign: "center" as const,
        marginBottom: "32px",
      }}>
        <h2 style={{ fontSize: "1.75rem", fontWeight: 700, marginBottom: "16px" }}>
          Let us Talk About Your Project
        </h2>
        <p style={{ opacity: 0.8, lineHeight: 1.7, maxWidth: "520px", margin: "0 auto 32px" }}>
          Book a free 30-minute briefing call. Tell me what problem you are trying to solve,
          what data you have, and what decisions you need to make.
        </p>
        <div>
          <button
            onClick={() => window.open("https://calendly.com/cjjohnazurapaulin2022/30min", "_blank")}
            style={{
              backgroundColor: "#06b6d4",
              color: "#000",
              fontWeight: 700,
              padding: "14px 32px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontSize: "1rem",
            }}>
            Book a Free Briefing Call
          </button>
        </div>
        <p style={{ marginTop: "16px", opacity: 0.5, fontSize: "0.85rem" }}>
          Or email directly: cjjohnazurapaulin2022@gmail.com
        </p>
      </section>

    </main>
  );
}
