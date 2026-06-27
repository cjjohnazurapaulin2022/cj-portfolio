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
        <strong className="ml-4">Featured
