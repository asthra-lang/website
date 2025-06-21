# Asthra Programming Language Website

This repository contains the source code for the Asthra programming language website, built with Jekyll and the custom "Saravarsham" theme.

## Features

- **Custom Jekyll Theme**: "Saravarsham" theme designed specifically for Asthra
- **Documentation System**: Organized documentation with collections
- **Blog Platform**: Built-in blog with pagination and RSS feed
- **GitHub Pages Ready**: Automatic deployment via GitHub Actions
- **Responsive Design**: Mobile-friendly layout
- **Syntax Highlighting**: Code highlighting for Asthra and other languages
- **SEO Optimized**: Built-in SEO tags and sitemap generation

## Local Development

### Prerequisites

- Ruby 2.7 or higher
- Bundler gem

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/asthra-lang/asthra-website.git
   cd asthra-lang-website
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Run the development server:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000`

### Development Commands

- `bundle exec jekyll serve` - Start development server
- `bundle exec jekyll serve --drafts` - Include draft posts
- `bundle exec jekyll build` - Build the site for production
- `bundle exec jekyll clean` - Clean generated files

## Content Structure

### Documentation

Documentation files are stored in the `_docs/` directory:
- `_docs/index.md` - Documentation homepage
- `_docs/installation.md` - Installation guide
- Add new documentation files as needed

### Blog Posts

Blog posts are stored in the `_posts/` directory:
- Follow the naming convention: `YYYY-MM-DD-title.md`
- Include proper front matter with layout, title, date, and categories

### Pages

Static pages can be added to the root directory or organized in subdirectories.

## Theme Customization

The "Saravarsham" theme files are located in:
- `_layouts/` - HTML templates
- `_includes/` - Reusable template components
- `_sass/` - SCSS stylesheets
- `assets/` - CSS, JavaScript, and other assets

### Color Scheme

The theme uses Asthra brand colors defined in `_sass/_variables.scss`:
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Accent: `#06b6d4` (Cyan)

### Typography

- Body text: Inter font family
- Headings: Inter font family
- Code: JetBrains Mono font family

## Deployment

### GitHub Pages (Automatic)

The site automatically deploys to GitHub Pages when you push to the `main` branch. The GitHub Actions workflow (`.github/workflows/pages.yml`) handles the build and deployment process.

### Manual Deployment

To deploy manually:

1. Build the site:
   ```bash
   bundle exec jekyll build
   ```

2. The generated site will be in the `_site/` directory

3. Upload the contents to your web server

## Configuration

Site configuration is managed in `_config.yml`. Key settings include:

- `title` - Site title
- `description` - Site description
- `url` - Site URL
- `navigation` - Main navigation menu
- `collections` - Content collections (docs, blog)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

### Adding Documentation

1. Create a new Markdown file in `_docs/`
2. Add appropriate front matter
3. Update `_docs/index.md` to link to the new page

### Adding Blog Posts

1. Create a new file in `_posts/` with the format `YYYY-MM-DD-title.md`
2. Add front matter with layout, title, date, and categories
3. Write your content in Markdown

## License

This website source code is available under the MIT License. See the LICENSE file for details.

## Support

- [GitHub Issues](https://github.com/asthra-lang/asthra/issues)
- [Discussions](https://github.com/orgs/asthra-lang/discussions)
- [Documentation](https://asthra-lang.org/docs/)

---

Built with ❤️ using Jekyll and the Saravarsham theme. 