export const INITIAL_USERS = [
  {
    id: "user-student",
    email: "student@aether.edu",
    password: "student123",
    name: "Priyanshi Sharma",
    role: "student",
    suspended: false,
    streakCount: 5,
    joinedDate: "2026-01-15"
  },
  {
    id: "user-teacher",
    email: "teacher@aether.edu",
    password: "teacher123",
    name: "Dr. Sarah Jenkins",
    role: "teacher",
    suspended: false,
    joinedDate: "2025-11-10"
  },
  {
    id: "user-admin",
    email: "admin@aether.edu",
    password: "admin123",
    name: "Chief Administrator",
    role: "admin",
    suspended: false,
    joinedDate: "2025-09-01"
  }
];

export const INITIAL_COURSES = [
  {
    id: "course-vue",
    title: "Mastering Vue 3: From Zero to Hero",
    description: "Learn Vue 3, Vue Router, Pinia, Composition API, and modern SPA design using Tailwind CSS. Create beautiful dynamic user interfaces and scale them efficiently.",
    shortDescription: "Master reactive SPA development with Vue 3 and modern design systems.",
    category: "Development",
    difficulty: "Intermediate",
    thumbnail: "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=600&q=80",
    teacherId: "user-teacher",
    teacherName: "Dr. Sarah Jenkins",
    status: "approved", // approved, pending, rejected
    rating: 4.8,
    reviewsCount: 124,
    studentsCount: 1250,
    duration: "4.5 Hours",
    rejectionReason: "",
    modules: [
      {
        id: "mod-vue-1",
        title: "Module 1: Introduction & App Setup",
        lessons: [
          {
            id: "vue-1-1",
            title: "1. Welcome & Scaffold Vite Project",
            type: "video",
            url: "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
            duration: "10:15",
            completed: false
          },
          {
            id: "vue-1-2",
            title: "2. Setting up Tailwind CSS & Google Fonts",
            type: "pdf",
            url: "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            duration: "Reading Guide (5 mins)",
            completed: false
          }
        ]
      },
      {
        id: "mod-vue-2",
        title: "Module 2: Reactivity & Composition API",
        lessons: [
          {
            id: "vue-2-1",
            title: "3. Understanding ref(), reactive(), and computed()",
            type: "video",
            url: "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
            duration: "18:42",
            completed: false
          },
          {
            id: "vue-2-2",
            title: "4. Component Props, Emits & Custom Events",
            type: "video",
            url: "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
            duration: "15:20",
            completed: false
          }
        ]
      }
    ]
  },
  {
    id: "course-fastapi",
    title: "Full-Stack Backend Development with FastAPI",
    description: "Deep dive into synchronous and asynchronous web services using Python, FastAPI, and MongoDB Atlas. Learn modern RESTful designs, token auth, and route protections.",
    shortDescription: "Build ultra-fast, production-ready Python backend APIs.",
    category: "Backend",
    difficulty: "Advanced",
    thumbnail: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
    teacherId: "user-teacher",
    teacherName: "Dr. Sarah Jenkins",
    status: "pending",
    rating: 4.7,
    reviewsCount: 42,
    studentsCount: 380,
    duration: "6 Hours",
    rejectionReason: "",
    modules: [
      {
        id: "mod-api-1",
        title: "Module 1: Scaffolding FastAPI & Async Core",
        lessons: [
          {
            id: "api-1-1",
            title: "1. Python Async/Await Foundations",
            type: "video",
            url: "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
            duration: "12:05",
            completed: false
          },
          {
            id: "api-1-2",
            title: "2. Setting up Uvicorn & MongoDB Atlas Cloud",
            type: "pdf",
            url: "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            duration: "Atlas Setup PDF",
            completed: false
          }
        ]
      }
    ]
  },
  {
    id: "course-design",
    title: "UI/UX Foundations: Designing High-End Dashboards",
    description: "Create breathtaking digital products. Learn how to master glassmorphism, tailwind variables, micro-animations, typography layouts, and HSL custom colors.",
    shortDescription: "Design high-fidelity user experiences that wow clients.",
    category: "Design",
    difficulty: "Beginner",
    thumbnail: "https://images.unsplash.com/photo-1541462608143-67571c6738dd?auto=format&fit=crop&w=600&q=80",
    teacherId: "user-other-teacher",
    teacherName: "Alex Mercer",
    status: "approved",
    rating: 4.9,
    reviewsCount: 88,
    studentsCount: 920,
    duration: "3.5 Hours",
    rejectionReason: "",
    modules: [
      {
        id: "mod-design-1",
        title: "Module 1: Layout, Contrast & Colors",
        lessons: [
          {
            id: "design-1-1",
            title: "1. Selecting Dark Mode Palettes",
            type: "video",
            url: "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
            duration: "15:40",
            completed: false
          }
        ]
      }
    ]
  }
];

export const INITIAL_ENROLLMENTS = [
  {
    id: "enroll-1",
    studentId: "user-student",
    courseId: "course-vue",
    completedLessons: ["vue-1-1"], // 1 out of 4 completed
    progressPercent: 25,
    enrolledDate: "2026-05-10"
  }
];
