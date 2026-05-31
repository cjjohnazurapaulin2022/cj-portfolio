import { About, Blog, Gallery, Home, Newsletter, Person, Social, Work } from "@/types";
import { Line, Row, Text } from "@once-ui-system/core";

const person: Person = {
  firstName: "CJ",
  lastName: "Paulin",
  name: `CJ Paulin`,
  role: "Data Analyst",
  avatar: "/images/cj-avatar.jpg",
  email: "cj.paulin@dataanalyst.com",
  location: "Asia/Manila", // Changed to Philippines timezone
  languages: ["English", "Filipino"],
};

const newsletter: Newsletter = {
  display: false, // Turned off newsletter
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
    link: "https://www.linkedin.com/in/cj-paulin/",
    essential: true,
  },
  {
    name: "Email",
    icon: "email",
    link: `mailto:${person.email}`,
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
          Sales Performance Dashboard
        </Text>
      </Row>
    ),
    href: "/work/sales-dashboard",
  },
  subline: (
    <>
    I'm CJ, a data analyst specializing in <Text as="span" size="xl" weight="strong">SQL, Python, and Business Intelligence</Text>. I turn complex data into actionable insights that drive business growth and data-informed decisions.
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
    display: false, // Turned off calendar booking
    link: "https://cal.com",
  },
  intro: {
    display: true,
    title: "Introduction",
    description: (
      <>
        I'm a data analyst passionate about uncovering insights that drive business decisions. 
        With expertise in SQL, Python, and data visualization tools like Tableau and Power BI, 
        I transform raw data into compelling stories and actionable recommendations.
        
        My approach combines technical rigor with business acumen. I focus on delivering measurable 
        outcomes - whether that's reducing reporting time, identifying revenue opportunities, 
        or optimizing marketing spend.
      </>
    ),
  },
  work: {
    display: true,
    title: "Data Analytics Experience",
    experiences: [
      {
        company: "Data Insights Co.",
        timeframe: "2023 - Present",
        role: "Data Analyst",
        achievements: [
          <>
            Built interactive dashboards that reduced reporting time by 75%, saving the team 20+ hours weekly
          </>,
          <>
            Analyzed customer behavior data from 500K+ transactions to identify $500K in upsell opportunities
          </>,
          <>
            Optimized complex SQL queries reducing execution time from 45 seconds to 2 seconds
          </>,
          <>
            Developed Python scripts for automated data cleaning, eliminating manual data processing
          </>,
        ],
        images: [],
      },
      {
        company: "Analytics Department",
        timeframe: "2021 - 2023",
        role: "Junior Data Analyst",
        achievements: [
          <>
            Created weekly sales reports using Excel and SQL, presented insights to management team
          </>,
          <>
            Assisted in migration of legacy data systems to cloud-based analytics platform
          </>,
          <>
            Collaborated with marketing team to analyze campaign performance across 12 channels
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
        name: "Data Analytics Certificate",
        description: <>Comprehensive program covering SQL, Python, Statistics, and Data Visualization</>,
      },
      {
        name: "Tableau Desktop Specialist",
        description: <>Certified in data visualization best practices and dashboard creation</>,
      },
      {
        name: "Google Data Analytics Professional Certificate",
        description: <>Foundations of data analysis, data cleaning, and analysis with spreadsheets and SQL</>,
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
          <>Advanced SQL queries, database design, query optimization across multiple database systems. Experience with joins, subqueries, window functions, and CTEs.</>
        ),
        tags: [
          {
            name: "PostgreSQL",
            icon: "database",
          },
          {
            name: "MySQL",
            icon: "database",
          },
          {
            name: "BigQuery",
            icon: "database",
          },
        ],
        images: [],
      },
      {
        title: "Python for Data Analysis",
        description: (
          <>Data cleaning, manipulation, analysis, and visualization using Python ecosystem. Pandas for data wrangling, Matplotlib/Seaborn for visualization.</>
        ),
        tags: [
          {
            name: "Python",
            icon: "python",
          },
          {
            name: "Pandas",
            icon: "code",
          },
          {
            name: "NumPy",
            icon: "code",
          },
        ],
        images: [],
      },
      {
        title: "Data Visualization & BI",
        description: (
          <>Creating interactive dashboards and reports that communicate insights effectively to stakeholders.</>
        ),
        tags: [
          {
            name: "Tableau",
            icon: "chart",
          },
          {
            name: "Power BI",
            icon: "chart",
          },
          {
            name: "Excel",
            icon: "table",
          },
        ],
        images: [],
      },
      {
        title: "Statistical Analysis",
        description: (
          <>Statistical methods for data analysis including regression, hypothesis testing, and A/B testing.</>
        ),
        tags: [
          {
            name: "Statistics",
            icon: "calculator",
          },
          {
            name: "A/B Testing",
            icon: "test-tube",
          },
          {
            name: "Regression",
            icon: "trending-up",
          },
        ],
        images: [],
      },
    ],
  },
};

const blog: Blog = {
  path: "/blog",
  label: "Blog",
  title: "Data Analytics Insights & Tutorials",
  description: `Sharing my learnings in SQL, Python, and data visualization`,
  // Create new blog posts by adding a new .mdx file to app/blog/posts
  // All posts will be listed on the /blog route
};

const work: Work = {
  path: "/work",
  label: "Work",
  title: `Data Analytics Projects – ${person.name}`,
  description: `SQL, Python, Tableau, and Power BI projects by ${person.name}`,
  // Create new project pages by adding a new .mdx file to app/work/
  // All projects will be listed on the /home and /work routes
};

const gallery: Gallery = {
  path: "/gallery",
  label: "Gallery",
  title: `Dashboard Gallery – ${person.name}`,
  description: `A collection of data visualizations and dashboards`,
  // Replace these with your actual dashboard screenshots
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
    {
      src: "/images/gallery/marketing-roi.jpg",
      alt: "Marketing ROI Dashboard",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/sql-optimization.jpg",
      alt: "SQL Query Optimization Results",
      orientation: "horizontal",
    },
  ],
};

export { person, social, newsletter, home, about, blog, work, gallery };
