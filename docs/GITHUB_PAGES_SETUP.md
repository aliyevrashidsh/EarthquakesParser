# GitHub Pages Setup Guide

This guide shows how to enable and access the documentation hosted on GitHub Pages.

## Enabling GitHub Pages

### 1. Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "docs: add GitHub Pages documentation"

# Push to main branch
git push origin main
```

### 2. Enable GitHub Pages in Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Source: **GitHub Actions**
5. Click **Save**

### 3. Wait for Deployment

- GitHub Actions will automatically build and deploy your documentation
- Check the **Actions** tab to see the deployment progress
- First deployment takes 2-5 minutes

## Accessing Your Documentation

Once deployed, your documentation will be available at:

```
https://yourusername.github.io/earthquakes-parser/
```

Replace `yourusername` with your GitHub username.

## Documentation Structure

```
docs/
├── index.md                # Homepage (required)
├── _config.yml             # Jekyll configuration
├── QUICK_START.md          # Quick start guide
├── CONTRIBUTING.md         # Contributing guidelines
├── RELEASE_POLICY.md       # Release policy
├── PROJECT_STRUCTURE.md    # Architecture
├── PRE_COMMIT_GUIDE.md     # Pre-commit hooks
└── SETUP_COMPLETE.md       # Setup guide
```

## Customizing the Theme

### Change Theme

Edit `docs/_config.yml`:

```yaml
theme: jekyll-theme-minimal  # Change this line
```

**Available themes:**
- `jekyll-theme-cayman` (default, modern)
- `jekyll-theme-minimal` (clean and simple)
- `jekyll-theme-architect` (bold headers)
- `jekyll-theme-slate` (dark theme)
- `jekyll-theme-modernist` (minimalist)

### Add Logo

1. Add logo image to `docs/assets/logo.png`
2. Update `_config.yml`:

```yaml
logo: /assets/logo.png
```

### Custom Colors

Create `docs/assets/css/style.scss`:

```scss
---
---

@import "{{ site.theme }}";

// Custom colors
.page-header {
  background-color: #155799;
  background-image: linear-gradient(120deg, #155799, #159957);
}
```

## Navigation

### Add Custom Pages

1. Create new markdown file in `docs/`:
   ```bash
   touch docs/API_REFERENCE.md
   ```

2. Add front matter:
   ```markdown
   ---
   title: API Reference
   ---

   # API Reference

   Content here...
   ```

3. Link from other pages:
   ```markdown
   [API Reference](API_REFERENCE.md)
   ```

## Updating Documentation

### Automatic Deployment

Docs are automatically deployed when you push to main:

```bash
# Edit documentation
vim docs/QUICK_START.md

# Commit and push
git add docs/
git commit -m "docs: update quick start guide"
git push origin main

# GitHub Actions will deploy automatically
```

### Manual Deployment

Trigger manual deployment:

1. Go to **Actions** tab
2. Select **Deploy Documentation** workflow
3. Click **Run workflow**
4. Select **main** branch
5. Click **Run workflow**

## Testing Locally

### Install Jekyll

```bash
# macOS
brew install ruby
gem install jekyll bundler

# Ubuntu
sudo apt install ruby-full build-essential
gem install jekyll bundler
```

### Run Local Server

```bash
cd docs

# Create Gemfile
cat > Gemfile << 'EOF'
source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
EOF

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Open http://localhost:4000 in browser
```

## SEO Optimization

### Add Description

In each markdown file, add front matter:

```markdown
---
title: Quick Start Guide
description: Get started with EarthquakesParser in 5 minutes
---
```

### Add Keywords

Edit `_config.yml`:

```yaml
keywords:
  - earthquake
  - parser
  - python
  - nlp
  - web scraping
```

### Add Google Analytics

1. Get Google Analytics tracking ID
2. Add to `_config.yml`:

```yaml
google_analytics: G-XXXXXXXXXX
```

## Custom Domain (Optional)

### Setup Custom Domain

1. Buy domain (e.g., `earthquakes-parser.com`)
2. Add CNAME record pointing to:
   ```
   yourusername.github.io
   ```
3. Create `docs/CNAME` file:
   ```
   earthquakes-parser.com
   ```
4. Push to GitHub
5. In repository settings, add custom domain

## Troubleshooting

### Documentation Not Showing

1. Check **Actions** tab for errors
2. Ensure `index.md` exists in `docs/`
3. Verify GitHub Pages is enabled in Settings
4. Clear browser cache
5. Wait 5 minutes after first push

### Build Failures

Check the Actions log:
1. Go to **Actions** tab
2. Click on failed workflow
3. Check error messages
4. Common issues:
   - Invalid YAML in `_config.yml`
   - Missing front matter in markdown files
   - Invalid theme name

### 404 Errors

- Ensure file names match exactly (case-sensitive)
- Use `.md` extension in links: `[Link](PAGE.md)`
- Check that files are in `docs/` directory

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Themes](https://pages.github.com/themes/)
- [Jekyll Themes](http://jekyllthemes.org/)

## Quick Reference

```bash
# Enable Pages: Settings → Pages → Source: GitHub Actions
# URL: https://yourusername.github.io/earthquakes-parser/

# Update docs
git add docs/
git commit -m "docs: update documentation"
git push origin main

# Custom domain
echo "yourdomain.com" > docs/CNAME
git add docs/CNAME
git commit -m "docs: add custom domain"
git push
```

---

**Your documentation is now live on GitHub Pages! 🎉**
