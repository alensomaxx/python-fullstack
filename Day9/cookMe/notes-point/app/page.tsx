export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
        <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-7 h-7 text-blue-600 dark:text-blue-400">📚</span>
            <span className="text-2xl font-bold text-slate-900 dark:text-white">My Notes</span>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-6 py-20">
        <div className="grid md:grid-cols-2 gap-12 items-center mb-20">
          <div className="space-y-6">
            <h1 className="text-5xl font-bold text-slate-900 dark:text-white leading-tight">
              Personal <span className="text-blue-600 dark:text-blue-400">Knowledge Hub</span>
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Organize your notes and track your learning journey. A space designed just for you.
            </p>
            <div className="flex gap-4 pt-4">
              <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors">
                Start Taking Notes
              </button>
            </div>
          </div>

          {/* Feature Preview */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8 space-y-4">
            <div className="flex items-center gap-3 p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
              <span className="w-5 h-5 text-slate-400">🔍</span>
              <input 
                type="text" 
                placeholder="Search your notes..." 
                className="bg-transparent w-full outline-none text-slate-900 dark:text-white placeholder-slate-400"
              />
            </div>
            <div className="space-y-2">
              <div className="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300">
                📌 React Hooks - Completed
              </div>
              <div className="p-3 bg-amber-50 dark:bg-amber-900/30 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300">
                📝 TypeScript Generics - In Progress
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-700 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300">
                ⏳ DSA Algorithms - Not Started
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 py-12">
          {[
            { icon: '⚡', title: "Lightning Fast", desc: "Minimal UI, maximum focus. Access your notes instantly." },
            { icon: '📚', title: "Organized Topics", desc: "Structure knowledge hierarchically for easy navigation." },
            { icon: '🔍', title: "Smart Search", desc: "Find anything in seconds across all your notes." },
          ].map((feature, i) => (
            <div key={i} className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
              <span className="w-8 h-8 text-blue-600 dark:text-blue-400 mb-3">{feature.icon}</span>
              <h3 className="font-semibold text-slate-900 dark:text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">{feature.desc}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-700 dark:to-blue-900 rounded-2xl p-12 text-center text-white mt-16">
          <h2 className="text-3xl font-bold mb-3">Ready to enhance your learning?</h2>
          <p className="text-blue-100 mb-6">Start organizing your knowledge today.</p>
          <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
            Get Started
          </button>
        </div>
      </main>
    </div>
  );
}
