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
        📧 <strong>Email me at:</strong>{" "}
        
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
    title: "Projects & Self-Directed Work",
    experiences: [
      {
        company: "Independent Data Analysis Projects",
        timeframe: "2024 – Present",
        role: "Data Analyst (Self-Directed)",
        achievements: [
          <>
            Conducted end-to-end marketing campaign analysis using Python,
            Pandas, and Seaborn — identifying spend inefficiencies and
            high-ROI channels across multiple ad platforms.
          </>,
          <>
            Built data cleaning pipelines and exploratory analysis workflows
            in Jupyter Notebook, developing reusable templates for future
            projects.
          </>,
          <>
            Actively expanding skills toward data science through coursework
            in statistics, machine learning fundamentals, and advanced SQL.
          </>,
        ],
        images: [],
      },
    ],
  },
  studies: {
    display: true,
    title: "Certifications",
    institutions: [
      {
        name: "Certification 1",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert1.png" target="_blank">
              View Certificate →
            </a>
          </>
        ),
      },
      {
        name: "Certification 2",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert2.png" target="_blank">
              View Certificate →
            </a>
          </>
        ),
      },
      {
        name: "Certification 3",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert3.png" target="_blank">
              View Certificate →
            </a>
          </>
        ),
      },
      {
        name: "Certification 4",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert4.png" target="_blank">
              View Certificate →
            </a>
          </>
        ),
      },
      {
        name: "Certification 5",
        description: (
          <>
            📄{" "}
            <a href="/images/certifications/cert5.png" target="_blank">
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
            Advanced SQL queries, database design, and query optimization
            across PostgreSQL, MySQL, and BigQuery.
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
            Pandas, NumPy, Matplotlib, and Seaborn for data cleaning,
            exploratory analysis, and visualization.
          </>
        ),
        tags: [
          { name: "Python", icon: "python" },
          { name: "Pandas", icon: "code" },
          { name: "NumPy", icon: "code" },
        ],
        images: [],
      },
      {
        title: "Data Visualization & BI",
        description: (
          <>
            Building interactive dashboards and stakeholder-ready reports
            in Tableau and Power BI.
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
            modeling for business reporting and ad hoc analysis.
          </>
        ),
        tags: [
          { name: "Excel", icon: "spreadsheet" },
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
  description: `SQL walkthroughs, Python tips, and lessons from real data projects by ${person.name}`,
};

const work: Work = {
  path: "/work",
  label: "Work",
  title: `Data Analytics Projects – ${person.name}`,
  description: `SQL, Python, Tableau, and Power BI projects by ${person.name}`,
};

const gallery: Gallery = {
  path: "/gallery",
  label: "Gallery",
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
