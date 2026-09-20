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
          Customer Churn Prediction System
        </Text>
      </Row>
    ),
    href: "/work/customer-churn-prediction",
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
        cjjohnazurapaulin2022@gmail.com
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
            Built a complete ML-powered churn prediction system on 541,909
            real e-commerce transactions — including a live Streamlit web
            app that scores customers monthly and generates automated
            action plans, deployable as a £800–1,200/year client retainer.
          </>,
          <>
            Conducted a digital marketing campaign performance analysis
            using Python, Pandas, and Seaborn — identifying spend
            inefficiencies and high-ROI channels across multiple ad
            platforms.
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
        name: "Foundations: Data, Data, Everywhere",
        description: <>📄 <a href="/images/certifications/cert1.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert1.png",
          alt: "Foundations: Data, Data, Everywhere certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "Prepare, Clean, Transform and Load Data Using Power BI",
        description: <>📄 <a href="/images/certifications/cert2.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert2.png",
          alt: "Prepare, Clean, Transform and Load Data Using Power BI certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "Analyze Data to Answer Questions",
        description: <>📄 <a href="/images/certifications/cert3.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert3.png",
          alt: "Analyze Data to Answer Questions certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "Data Analysis with R Programming",
        description: <>📄 <a href="/images/certifications/cert4.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert4.png",
          alt: "Data Analysis with R Programming certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "Process Data from Dirty to Clean",
        description: <>📄 <a href="/images/certifications/cert5.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert5.png",
          alt: "Process Data from Dirty to Clean certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "The Power of Statistics",
        description: <>📄 <a href="/images/certifications/cert6.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert6.png",
          alt: "The Power of Statistics certificate",
          width: 180,
          height: 180,
        },
      },
      {
        name: "Simplify Complex Data Relationships",
        description: <>📄 <a href="/images/certifications/cert7.png" target="_blank">View Certificate →</a></>,
        image: {
          src: "/images/certifications/cert7.png",
          alt: "Simplify Complex Data Relationships certificate",
          width: 180,
          height: 180,
        },
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
          <>Advanced SQL queries, database design, query optimization across PostgreSQL, MySQL, and BigQuery</>
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
          <>Pandas, NumPy, Matplotlib for data cleaning, analysis, and visualization</>
        ),
        tags: [
          { name: "Python", icon: "python" },
          { name: "Pandas", icon: "code" },
          { name: "NumPy", icon: "code" },
        ],
        images: [],
      },
      {
        title: "Data Visualization",
        description: (
          <>Creating interactive dashboards in Tableau and Power BI</>
        ),
        tags: [
          { name: "Tableau", icon: "chart" },
          { name: "Power BI", icon: "chart" },
        ],
        images: [],
      },
    ],
  },
  toolsIUse: {
    display: true,
    title: "Tools I Use",
    tools: [
      { name: "Python", icon: "https://cdn.simpleicons.org/python/3776AB" },
      { name: "R", icon: "https://cdn.simpleicons.org/r/276DC3" },
      { name: "VS Code", icon: "https://cdn.simpleicons.org/visualstudiocode/007ACC" },
      { name: "Jupyter Notebook", icon: "https://cdn.simpleicons.org/jupyter/F37626" },
      { name: "PostgreSQL", icon: "https://cdn.simpleicons.org/postgresql/4169E1" },
      { name: "Excel", icon: "https://cdn.simpleicons.org/microsoftexcel/217346" },
      { name: "Word", icon: "https://cdn.simpleicons.org/microsoftword/2B579A" },
      { name: "PowerPoint", icon: "https://cdn.simpleicons.org/microsoftpowerpoint/B7472A" },
      { name: "Power BI", icon: "https://cdn.simpleicons.org/powerbi/F2C811" },
      { name: "Tableau", icon: "https://cdn.simpleicons.org/tableau/E97627" },
      { name: "Gmail", icon: "https://cdn.simpleicons.org/gmail/EA4335" },
      { name: "Google Meet", icon: "https://cdn.simpleicons.org/googlemeet/00897B" },
      { name: "Zoom", icon: "https://cdn.simpleicons.org/zoom/2D8CFF" },
      { name: "Calendly", icon: "https://cdn.simpleicons.org/calendly/006BFF" },
      { name: "Claude", icon: "https://cdn.simpleicons.org/claude/D97757" },
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
  label: "Portfolio",
  title: `Data Analytics Projects – ${person.name}`,
  description: `SQL, Python, Tableau, and Power BI projects by ${person.name}`,
};

const gallery: Gallery = {
  path: "/gallery",
  label: "Gallery",
  title: `Dashboard Gallery – ${person.name}`,
  description: `A collection of data visualizations and dashboards`,
  images: [],
};

export { person, social, newsletter, home, about, blog, work, gallery };
