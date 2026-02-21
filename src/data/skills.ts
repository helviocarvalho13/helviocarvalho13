export interface Skill {
  name: string;
  projects: number;
  maxProjects: number;
  icon: string;
}

export interface Region {
  id: string;
  name: string;
  emoji: string;
  description: string;
  color: string;
  skills: Skill[];
  position: { x: number; y: number };
  nodeType: "normal" | "castle" | "fortress" | "ghost" | "star";
}

export interface Project {
  id: number;
  name: string;
  description: string;
  stars: number; // 1-3
  icon: string;
}

export interface WorkExperience {
  company: string;
  role: string;
  period: string;
  description: string;
  icon: string;
  skills: string[];
}

export interface VolunteerWork {
  organization: string;
  role: string;
  period: string;
  description: string;
  icon: string;
}

/** Paths connecting regions (pairs of region IDs) */
export const paths: [string, string][] = [
  ["frontend", "backend"],
  ["backend", "ai"],
  ["backend", "database"],
  ["frontend", "devops"],
  ["devops", "methodologies"],
  ["methodologies", "database"],
  ["backend", "methodologies"],
];

export const ceoInfo = {
  name: "Helvio Carvalho",
  title: "Tech Lead / CEO",
  company: "Luna Tecnologia",
  companyUrl: "https://lunatecnologia.com.br",
  linkedin: "https://linkedin.com/in/helviocarvalho",
  github: "https://github.com/helviocarvalho",
  bio: "Desenvolvedor Full Stack apaixonado por criar soluções digitais inovadoras.",
  yearsOfExp: 8,
  completedQuests: 45,
  worldsExplored: 6,
};

export const projects: Project[] = [
  { id: 1, name: "ERP Corporativo", description: "Sistema de gestão empresarial completo", stars: 3, icon: "🏢" },
  { id: 2, name: "E-commerce Platform", description: "Plataforma de vendas online", stars: 3, icon: "🛒" },
  { id: 3, name: "App Mobile Banking", description: "Aplicativo bancário em Flutter", stars: 3, icon: "🏦" },
  { id: 4, name: "API Gateway", description: "Microserviços com Spring Boot", stars: 2, icon: "🔗" },
  { id: 5, name: "Dashboard Analytics", description: "Painel de análise de dados", stars: 2, icon: "📊" },
  { id: 6, name: "CRM System", description: "Gestão de relacionamento com clientes", stars: 2, icon: "👥" },
  { id: 7, name: "Chat Real-time", description: "Sistema de chat com WebSocket", stars: 2, icon: "💬" },
  { id: 8, name: "CI/CD Pipeline", description: "Automação de deploy e testes", stars: 1, icon: "🔄" },
  { id: 9, name: "Landing Pages", description: "Páginas institucionais responsivas", stars: 1, icon: "📄" },
];

export const workExperiences: WorkExperience[] = [
  {
    company: "Luna Tecnologia",
    role: "CEO / Tech Lead",
    period: "2020 - Presente",
    description: "Liderança técnica e estratégica, desenvolvimento de soluções Full Stack para clientes corporativos.",
    icon: "🌙",
    skills: ["Java", "Angular", "Spring Boot", "PostgreSQL"],
  },
  {
    company: "Empresa de Tecnologia",
    role: "Desenvolvedor Full Stack Senior",
    period: "2018 - 2020",
    description: "Desenvolvimento de sistemas empresariais de grande porte com Java e Angular.",
    icon: "💼",
    skills: ["Java", "Angular", "Oracle", "REST APIs"],
  },
  {
    company: "Startup Digital",
    role: "Desenvolvedor Backend",
    period: "2016 - 2018",
    description: "Criação de APIs e microsserviços para plataformas digitais escaláveis.",
    icon: "🚀",
    skills: ["Java", "Spring Boot", "MySQL", "Docker"],
  },
];

export const volunteerWork: VolunteerWork[] = [
  {
    organization: "Comunidade Dev Local",
    role: "Mentor de Programação",
    period: "2021 - Presente",
    description: "Mentoria para desenvolvedores iniciantes em Java e tecnologias web.",
    icon: "🎓",
  },
  {
    organization: "ONG Educação Digital",
    role: "Instrutor Voluntário",
    period: "2019 - 2021",
    description: "Aulas de programação para jovens em comunidades carentes.",
    icon: "💡",
  },
  {
    organization: "Hackathon Social",
    role: "Organizador & Jurado",
    period: "2020 - Presente",
    description: "Organização de hackathons focados em impacto social positivo.",
    icon: "🏆",
  },
];

export const regions: Region[] = [
  {
    id: "frontend",
    name: "Ilha Yoshi",
    emoji: "🏝️",
    description: "Tecnologias de interface e experiência do usuário",
    color: "from-cyan-600 to-blue-500",
    position: { x: 12, y: 55 },
    nodeType: "star",
    skills: [
      { name: "Angular", projects: 13, maxProjects: 20, icon: "🅰️" },
      { name: "React", projects: 2, maxProjects: 20, icon: "⚛️" },
      { name: "Flutter", projects: 2, maxProjects: 20, icon: "🦋" },
      { name: "TypeScript", projects: 8, maxProjects: 20, icon: "🔷" },
      { name: "Dart", projects: 2, maxProjects: 20, icon: "🎯" },
      { name: "Tailwind CSS", projects: 3, maxProjects: 20, icon: "🎨" },
      { name: "HTML/CSS", projects: 15, maxProjects: 20, icon: "📄" },
      { name: "JavaScript", projects: 15, maxProjects: 20, icon: "⚡" },
    ],
  },
  {
    id: "backend",
    name: "Vanilla Dome",
    emoji: "⛰️",
    description: "Lógica de servidor e APIs robustas",
    color: "from-amber-700 to-orange-600",
    position: { x: 45, y: 28 },
    nodeType: "fortress",
    skills: [
      { name: "Java", projects: 20, maxProjects: 20, icon: "☕" },
      { name: "Spring Boot", projects: 15, maxProjects: 20, icon: "🍃" },
      { name: "Node.js", projects: 5, maxProjects: 20, icon: "🟢" },
      { name: "Laravel", projects: 3, maxProjects: 20, icon: "🔴" },
      { name: "PHP", projects: 5, maxProjects: 20, icon: "🐘" },
      { name: "REST APIs", projects: 18, maxProjects: 20, icon: "🔗" },
      { name: "Microservices", projects: 8, maxProjects: 20, icon: "🧩" },
    ],
  },
  {
    id: "database",
    name: "Castelo Koopa",
    emoji: "🏰",
    description: "Bancos de dados e persistência",
    color: "from-purple-700 to-violet-500",
    position: { x: 85, y: 55 },
    nodeType: "castle",
    skills: [
      { name: "Oracle", projects: 10, maxProjects: 20, icon: "🔶" },
      { name: "PostgreSQL", projects: 8, maxProjects: 20, icon: "🐘" },
      { name: "MySQL", projects: 5, maxProjects: 20, icon: "🗄️" },
      { name: "Liquibase", projects: 6, maxProjects: 20, icon: "💧" },
    ],
  },
  {
    id: "devops",
    name: "Forest of Illusion",
    emoji: "🌲",
    description: "CI/CD, deploy e infraestrutura",
    color: "from-red-700 to-orange-500",
    position: { x: 18, y: 82 },
    nodeType: "ghost",
    skills: [
      { name: "Git", projects: 20, maxProjects: 20, icon: "📦" },
      { name: "GitHub Actions", projects: 5, maxProjects: 20, icon: "🔄" },
      { name: "GitLab CI/CD", projects: 4, maxProjects: 20, icon: "🦊" },
      { name: "Jenkins", projects: 6, maxProjects: 20, icon: "🤖" },
      { name: "Docker", projects: 5, maxProjects: 20, icon: "🐳" },
      { name: "Heroku", projects: 3, maxProjects: 20, icon: "☁️" },
    ],
  },
  {
    id: "methodologies",
    name: "Star Road",
    emoji: "⭐",
    description: "Metodologias e boas práticas",
    color: "from-emerald-700 to-green-500",
    position: { x: 55, y: 75 },
    nodeType: "star",
    skills: [
      { name: "Scrum", projects: 15, maxProjects: 20, icon: "🏃" },
      { name: "Kanban", projects: 12, maxProjects: 20, icon: "📋" },
      { name: "Design Patterns", projects: 10, maxProjects: 20, icon: "🏗️" },
      { name: "UML", projects: 8, maxProjects: 20, icon: "📐" },
      { name: "Clean Code", projects: 15, maxProjects: 20, icon: "✨" },
    ],
  },
  {
    id: "ai",
    name: "Special Zone",
    emoji: "🤖",
    description: "Ferramentas de inteligência artificial",
    color: "from-pink-600 to-fuchsia-500",
    position: { x: 80, y: 18 },
    nodeType: "fortress",
    skills: [
      { name: "Lovable", projects: 3, maxProjects: 20, icon: "💜" },
      { name: "Replit AI", projects: 2, maxProjects: 20, icon: "🧠" },
      { name: "ChatGPT", projects: 5, maxProjects: 20, icon: "💬" },
      { name: "Copilot", projects: 8, maxProjects: 20, icon: "🤝" },
    ],
  },
];

export const totalXP = regions.reduce(
  (sum, r) => sum + r.skills.reduce((s, sk) => s + sk.projects, 0),
  0
);

export const maxXP = regions.reduce(
  (sum, r) => sum + r.skills.reduce((s, sk) => s + sk.maxProjects, 0),
  0
);
