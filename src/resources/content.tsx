import { About, Home, Newsletter, Person, Social, Work } from "@/types";
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
          E-Commerce Customer Intelligence Report
        </Text>
      </Row>
    ),
    href: "/work/ecommerce-customer-intelligence",
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
            Built an end-to-end customer intelligence analysis on 524,878
            real e-commerce transactions — combining RFM segmentation,
            cohort retention, and CLV modeling into a revenue-impact action
            plan.
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
      },
      {
        name: "Prepare, Clean, Transform and Load Data Using Power BI",
        description: <>📄 <a href="/images/certifications/cert2.png" target="_blank">View Certificate →</a></>,
      },
      {
        {
        name: "Analyze Data to Answer Questions",
        description: <>📄 <a href="/images/certifications/cert3.png" target="_blank">View Certificate →</a></>,
      },
