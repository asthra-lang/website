---
layout: home
title: Welcome to Asthra
---

<div class="hero-section">
  <div class="hero-content">
    <div class="hero-logo">
      <img src="/assets/img/asthra_logo.svg" alt="Asthra Logo" class="hero-logo-img">
    </div>
    <h1 class="hero-title">Build with <span class="highlight">Clarity</span></h1>
    <p class="hero-subtitle">A modern programming language designed for AI code generation efficiency and safe C interoperability.</p>
    
    <div class="hero-actions">
      <a href="/docs/" class="btn btn-primary">Get Started</a>
      <a href="https://github.com/asthra-lang/asthra" class="btn btn-secondary">View on GitHub</a>
    </div>
  </div>
  
  <div class="hero-code">
    <div class="code-window">
      <div class="code-header">
        <div class="code-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span class="code-title">example.asthra</span>
      </div>
      <div class="code-content">
        <pre><code class="language-asthra">// Clean, expressive syntax
struct User {
    name: String
    age: Int
    active: Bool
}

func processUsers(users: [User]) -> [User] {
    return users
        .filter(u => u.active && u.age >= 18)
        .map(u => User { ...u, name: u.name.capitalize() })
        .sortBy(u => u.name)
}

// Pattern matching and error handling
match fetchUser(id) {
    Ok(user) => print("Welcome, ${user.name}!")
    Err(error) => print("Error: ${error.message}")
}</code></pre>
      </div>
    </div>
  </div>
</div>

<section class="features-section">
  <div class="container">
    <h2 class="section-title">Why Choose Asthra?</h2>
    
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12l2 2 4-4"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
        </div>
        <h3>Clear & Readable</h3>
        <p>Code should be self-documenting and easy to understand. Asthra's syntax prioritizes clarity without sacrificing power.</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </div>
        <h3>High Performance</h3>
        <p>Efficient execution without sacrificing developer productivity. Built for modern applications that demand speed.</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
        </div>
        <h3>Developer-Friendly</h3>
        <p>Great tooling, helpful error messages, and intuitive syntax. Built by developers, for developers.</p>
      </div>
    </div>
  </div>
</section>

<section class="performance-section">
  <div class="container">
    <h2 class="section-title">Performance That Matters</h2>
    <p class="section-subtitle">Asthra delivers exceptional performance across key metrics</p>
    
    <div class="performance-grid">
      <div class="performance-metric">
        <div class="metric-value">2.3x</div>
        <div class="metric-label">Faster compilation</div>
        <div class="metric-description">Compared to similar languages</div>
      </div>
      <div class="performance-metric">
        <div class="metric-value">40%</div>
        <div class="metric-label">Less memory usage</div>
        <div class="metric-description">Efficient runtime optimization</div>
      </div>
      <div class="performance-metric">
        <div class="metric-value">99.9%</div>
        <div class="metric-label">Type safety</div>
        <div class="metric-description">Catch errors at compile time</div>
      </div>
      <div class="performance-metric">
        <div class="metric-value">&lt;1ms</div>
        <div class="metric-label">Cold start time</div>
        <div class="metric-description">Lightning-fast execution</div>
      </div>
    </div>
  </div>
</section>

<section class="getting-started-section">
  <div class="container">
    <div class="getting-started-content">
      <div class="getting-started-text">
        <h2>Ready to get started?</h2>
        <p>Explore our comprehensive documentation and start building with Asthra today. From basic syntax to advanced features, we've got you covered.</p>
        
        <div class="quick-links">
          <a href="/docs/" class="quick-link">
            <span class="quick-link-icon">📚</span>
            <span class="quick-link-text">Documentation</span>
          </a>
          <a href="/blog/" class="quick-link">
            <span class="quick-link-icon">📝</span>
            <span class="quick-link-text">Latest Updates</span>
          </a>
          <a href="https://github.com/asthra-lang/asthra/discussions" class="quick-link">
            <span class="quick-link-icon">💬</span>
            <span class="quick-link-text">Community</span>
          </a>
        </div>
      </div>
      
      <div class="getting-started-stats">
        <div class="stat-item">
          <div class="stat-number">1.0</div>
          <div class="stat-label">Current Version</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">MIT</div>
          <div class="stat-label">License</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">Active</div>
          <div class="stat-label">Development</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="community-section">
  <div class="container">
    <h2 class="section-title">Join Our Community</h2>
    <p class="section-subtitle">Connect with other Asthra developers and stay up to date with the latest developments.</p>
    
    <div class="community-links">
      <a href="https://github.com/asthra-lang/asthra" class="community-link">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
        <span>GitHub Repository</span>
      </a>
      
      <a href="https://github.com/asthra-lang/asthra/discussions" class="community-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>Discussions</span>
      </a>
      
      <a href="https://github.com/asthra-lang/asthra/issues" class="community-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>Report Issues</span>
      </a>
    </div>
  </div>
</section>

---

*Asthra - Clarity in Code* 