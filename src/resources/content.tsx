import { About, Blog, Gallery, Home, Newsletter, Person, Social, Work } from "@/types";
import { Line, Row, Text } from "@once-ui-system/core";

const person: Person = {
  firstName: "CJ",
  lastName: "Paulin",
  name: `CJ Paulin`,
  role: "Data Analyst",
  avatar: "/images/cj-avatar.jpg",
  email: "cjjohnazurapaulin2022@gmail.com",
  location: "Asia/Manila",
  languages: ["English", "Filipino"],
};

const newsletter: Newsletter = {
  display: false,
  title: <>Subscribe to {person.firstName}'s Newsletter</>,
  description: <>Monthly data analytics insights and project breakdowns</>,
};

const social: Social = [
  {
    name: "GitHub",
    icon: "github",
    link: "https://github.com/cjjohnazurapaulin2022",
    essential: true,
  },
  {
    name: "LinkedIn",
    icon: "linkedin",
    link: "https://www.linkedin.com/in/cj-john-paulin-6b29aa2ba",
    essential: true,
  },
  {
    name: "Email",
    icon: "email",
    link: "mailto:cjjohnazurapaulin2022@gmail.com",
    essential: true,
  },
];

const home: Home = {
  path: "/",
  image: "/images/og/home.jpg",
  label: "Home",
  title: `${person.name}'s Portfolio`,
  description: `Data analytics portfolio showcasing SQL, Python, and business intelligence projects by ${person.name}`,
  headline: <>Turning Data into Business Decisions</>,
  featured: {
    display: true,
    title: (
      <Row gap="12" vertical="center">
        <strong className="ml-4">Featured Project</strong>{" "}
        <Line background="brand-alpha-strong" vert height="20" />
        <Text marginRight="4" onBackground="brand-medium">
          Digital Marketing Campaign Analysis
        </Text>
      </Row>
    ),
    href: "/work/digital-marketing-campaign-analysis",
  },
  subline: (
    <>
      I'm CJ, a data analyst specializing in{" "}
      <Text as="span" size="xl" weight="strong">
        SQL, Excel, Python, and Business Intelligence
      </Text>
      . I turn complex data into actionable insights that drive business growth
      and data-informed decisions.
    </>
  ),
};

const about: About = {
  path: "/about",
  label: "About",
  title: `About – ${person.name}`,
  description: `Meet ${person.name}, ${person.role} specializing in data analytics and business intelligence`,
  tableOfContent: {
    display: true,
    subItems: false,
  },
  avatar: {
    display: true,
  },
  calendar: {
    display: false,
    link: "https://cal.com",
  },
  intro: {
    display: true,
    title: "Introduction",
    description: (
      <>
        I'm a data analyst passionate about uncovering insights that drive
        business decisions. With expertise in SQL, Python, and data
        visualization tools like Tableau and Power BI, I transform raw data
        into compelling stories and actionable recommendations.
        <br /><br />
        My approach combines technical rigor with business acumen. I focus on
        delivering measurable outcomes — whether that's reducing reporting
        time, identifying revenue opportunities, or optimizing marketing spend.
        <br /><br />
        I'm a fresh graduate actively building my portfolio and seeking my
        first data analyst role. Every project here reflects real analytical
        thinking applied to real-world datasets.
        <br /><br />
        📧 <strong>Get in touch:</strong>{" "}
        
          href="mailto:cjjohnazurapaulin2022@gmail.com"
          style={{ color: "#007bff", textDecoration: "underline" }}
        >
          cjjohnazurapaulin2022@gmail.com
        </a>
      </>
    ),
  },
  work: {
    display: true,
    title: "Experience",
    experiences: [
      {
        company: "Self-Directed Data Analytics Projects",
        timeframe: "2024 – Present",
        role: "Independent Data Analyst",
        achievements: [
          <>
            Completed end-to-end analysis of digital marketing campaign data
            using Python, Pandas, and Seaborn — identifying channel-level ROI
            and spend efficiency patterns.
          </>,
          <>
            Built data visualizations and dashboards to communicate findings
            to a non-technical audience, simulating a real business reporting
            workflow.
          </>,
          <>
            Actively developing skills in SQL, Power BI, and Tableau through
            project-based learning and real-world datasets.
          </>,
        ],
        images: [],
      },
    ],
  },
  studies: {
    display: true,
    title: "Education & Certifications",
    institutions: [
      {
        // Replace with your actual degree and school
        name: "Your University Name",
        description: <>Bachelor's Degree — [Your Field of Study], [Year Graduated]</>,
      },
      {
        // Replace with real cert name and link when ready
        name: "Add Your Certification Here",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert1.png" target="_blank">
              View Certificate →
            </a>
          </>
        ),
      },
    ],
  },
  technical: {
    display: true,
    title: "Technical Skills",
    skills: [
      {
        title: "SQL & Databases",
        description: (
          <>
            Writing complex queries, joins, aggregations, window functions, and
            CTEs for data extraction and reporting across PostgreSQL, MySQL, and
            BigQuery.
          </>
        ),
        tags: [
          { name: "PostgreSQL", icon: "database" },
          { name: "MySQL", icon: "database" },
          { name: "BigQuery", icon: "database" },
        ],
        images: [],
      },
      {
        title: "Python for Data Analysis",
        description: (
          <>
            Data cleaning, exploratory data analysis, and visualization using
            Pandas, NumPy, Matplotlib, and Seaborn inside Jupyter Notebook.
          </>
        ),
        tags: [
          { name: "Python", icon: "python" },
          { name: "Pandas", icon: "code" },
          { name: "NumPy", icon: "code" },
          { name: "Matplotlib", icon: "code" },
          { name: "Seaborn", icon: "code" },
        ],
        images: [],
      },
      {
        title: "Business Intelligence & Visualization",
        description: (
          <>
            Building interactive dashboards and visual stories for business
            stakeholders using Tableau and Power BI.
          </>
        ),
        tags: [
          { name: "Tableau", icon: "chart" },
          { name: "Power BI", icon: "chart" },
        ],
        images: [],
      },
      {
        title: "Excel & Spreadsheet Analysis",
        description: (
          <>
            Advanced formulas, pivot tables, VLOOKUP/XLOOKUP, and data
            modeling for business reporting and ad-hoc analysis.
          </>
        ),
        tags: [
          { name: "Excel", icon: "table" },
          { name: "Pivot Tables", icon: "table" },
        ],
        images: [],
      },
      {
        title: "Statistics & Analytics Methods",
        description: (
          <>
            Descriptive statistics, hypothesis testing, A/B test analysis, and
            regression to support data-driven recommendations.
          </>
        ),
        tags: [
          { name: "Statistics", icon: "chart" },
          { name: "A/B Testing", icon: "chart" },
          { name: "Regression", icon: "chart" },
        ],
        images: [],
      },
    ],
  },
};

const blog: Blog = {
  path: "/blog",
  label: "Insights",
  title: "Data Analytics Insights & Tutorials",
  description: `SQL walkthroughs, Python tips, and lessons from real data projects — by ${person.name}`,
};

const work: Work = {
  path: "/work",
  label: "Projects",
  title: `Data Analytics Projects – ${person.name}`,
  description: `SQL, Python, Tableau, and Power BI projects by ${person.name}`,
};

const gallery: Gallery = {
  path: "/gallery",
  label: "Dashboards",
  title: `Dashboard Gallery – ${person.name}`,
  description: `A collection of data visualizations and dashboards built with Tableau, Power BI, and Python`,
  images: [
    {
      src: "/images/gallery/sales-dashboard.jpg",
      alt: "Sales Performance Dashboard",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/churn-analysis.jpg",
      alt: "Customer Churn Analysis",
      orientation: "horizontal",
    },
  ],
};

export { person, social, newsletter, home, about, blog, work, gallery };
