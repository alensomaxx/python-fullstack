import Image from "next/image";
export const metadata = {
  title: "Alenso's Portfolio",
  description: "Welcome to Alenso's portfolio. Explore projects and get in touch!",
};
export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-50 to-zinc-100 dark:from-black dark:to-zinc-900">
      {/* Header/Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur dark:bg-black/80 border-b border-zinc-200 dark:border-zinc-800">
        <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-bold text-black dark:text-white">alenso</h2>
          <div className="flex gap-6 text-sm font-medium">
            <a href="#about" className="hover:text-blue-600 dark:hover:text-blue-400">About</a>
            <a href="#projects" className="hover:text-blue-600 dark:hover:text-blue-400">Projects</a>
            <a href="#contact" className="hover:text-blue-600 dark:hover:text-blue-400">Contact</a>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 py-20">
        {/* Hero Section */}
        <section className="mb-20">
          <div className="flex flex-col sm:flex-row items-center gap-12 mb-12">
            <Image
              src="/alenso.png"
              alt="Alenso"
              width={150}
              height={150}
            />
            <div>
              <h1 className="text-5xl font-bold text-black dark:text-white mb-4">
                Hi, I'm Alenso
              </h1>
              <p className="text-xl text-zinc-600 dark:text-zinc-300 mb-6">
                Full-stack developer building amazing web experiences with Next.js and React
              </p>
              <div className="flex gap-4">
                <a
                  href="#contact"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Get In Touch
                </a>
                <a
                  href="#projects"
                  className="px-6 py-3 border-2 border-blue-600 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-zinc-900 transition"
                >
                  View Work
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section id="about" className="mb-20">
          <h2 className="text-3xl font-bold mb-6 text-black dark:text-white">About Me</h2>
          <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl">
            I'm a passionate developer with expertise in TypeScript, React, and Next.js. I love creating intuitive, performant web applications that solve real-world problems.
          </p>
        </section>

        {/* Projects Section */}
        <section id="projects" className="mb-20">
          <h2 className="text-3xl font-bold mb-8 text-black dark:text-white">Featured Projects</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white dark:bg-zinc-900 p-6 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:shadow-lg transition">
                <h3 className="text-xl font-semibold mb-2 text-black dark:text-white">Project {i}</h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm mb-4">Description of your project goes here.</p>
                <a href="#" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
                  Learn more →
                </a>
              </div>
            ))}
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="mb-20">
          <h2 className="text-3xl font-bold mb-6 text-black dark:text-white">Let's Connect</h2>
          <div className="flex gap-4">
            <a href="https://github.com/alensomaxx" target="_blank" rel="noopener noreferrer" className="text-zinc-600 dark:text-zinc-300 hover:text-black dark:hover:text-white">
              GitHub
            </a>
            <a href="https://www.linkedin.com/in/alensomaxx/" target="_blank" rel="noopener noreferrer" className="text-zinc-600 dark:text-zinc-300 hover:text-black dark:hover:text-white">
              LinkedIn
            </a>
            <a href="mailto:alensocreations@gmail.com" className="text-zinc-600 dark:text-zinc-300 hover:text-black dark:hover:text-white">
              Email
            </a>
          </div>
        </section>
      </main>
    </div>
  );
}
