#!/usr/bin/env python3
"""
Convert Jekyll blog to static HTML site
"""
import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class Post:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.frontmatter = {}
        self.content = ""
        self.parse()

    def parse(self):
        """Parse markdown file with YAML frontmatter"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        parts = re.split(r'^---\s*$', content, flags=re.MULTILINE, maxsplit=2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            self.content = parts[2].strip()

            # Parse YAML frontmatter (simple parsing)
            current_list_key = None
            for line in frontmatter_text.split('\n'):
                stripped = line.strip()
                if not stripped:
                    continue

                if line.startswith('  - '):
                    # This is a list item
                    item = line.replace('  - ', '').strip()
                    if current_list_key and current_list_key in self.frontmatter:
                        self.frontmatter[current_list_key].append(item)
                elif ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')

                    # Handle lists (tags, categories)
                    if key in ['tags', 'categories']:
                        self.frontmatter[key] = []
                        current_list_key = key
                    else:
                        self.frontmatter[key] = value
                        current_list_key = None

    def get_url_slug(self) -> str:
        """Extract URL slug from filename (remove date prefix)"""
        filename = os.path.basename(self.filepath)
        # Remove .md extension
        filename = filename[:-3]
        # Remove date prefix (YYYY-MM-DD-)
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
        return slug

    def get_date(self) -> datetime:
        """Extract date from frontmatter or filename"""
        if 'modified' in self.frontmatter:
            date_str = self.frontmatter['modified'].split('T')[0]
            return datetime.strptime(date_str, '%Y-%m-%d')

        # Fallback to filename
        filename = os.path.basename(self.filepath)
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})', filename)
        if match:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return datetime.now()

    def convert_markdown_to_html(self, md_text: str) -> str:
        """Simple markdown to HTML converter"""
        html = md_text

        # Code blocks with language (must be before inline code)
        html = re.sub(
            r'```(\w+)\n(.*?)```',
            lambda m: f'<pre><code class="language-{m.group(1)}">{self.escape_html(m.group(2))}</code></pre>',
            html,
            flags=re.DOTALL
        )

        # Code blocks without language
        html = re.sub(
            r'```\n(.*?)```',
            lambda m: f'<pre><code>{self.escape_html(m.group(1))}</code></pre>',
            html,
            flags=re.DOTALL
        )

        # Inline code (must be after code blocks)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # Images with links
        html = re.sub(
            r'<figure[^>]*>\s*<a href="([^"]+)"><img src="([^"]+)"[^>]*></a>\s*<figcaption>([^<]+)</figcaption>\s*</figure>',
            r'<figure><a href="\1"><img src="\2" alt="\3"></a><figcaption>\3</figcaption></figure>',
            html
        )

        # Images
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', html)

        # Links
        html = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'<a href="\1">\2</a>', html)
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

        # Headers (must be before bold to avoid ** conflicts)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Unordered lists (handle both * and - markers) - before bold/italic
        lines = html.split('\n')
        processed_lines = []
        in_list = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Check if this is a list item (starts with * or - followed by space)
            if re.match(r'^[\*\-] ', stripped):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                # Extract list item content
                content = re.sub(r'^[\*\-] ', '', stripped)
                processed_lines.append(f'<li>{content}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                processed_lines.append(line)

        # Close list if still open
        if in_list:
            processed_lines.append('</ul>')

        html = '\n'.join(processed_lines)

        # Bold (must be before italic)
        html = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html)

        # Italic (single asterisks or underscores, but not at beginning of word)
        html = re.sub(r'(?<!\*)\*([^\*\n]+)\*(?!\*)', r'<em>\1</em>', html)

        # Notice blocks
        html = re.sub(
            r'\{: \.notice--(info|warning|danger)\}',
            r'',
            html
        )

        # Paragraphs (simple approach)
        lines = html.split('\n')
        processed = []
        in_html_block = False

        block_tags = ['<pre>', '<ul>', '<ol>', '<h1>', '<h2>', '<h3>', '<figure>', '<blockquote>', '<p>']
        closing_tags = ['</pre>', '</ul>', '</ol>', '</h1>', '</h2>', '</h3>', '</figure>', '</blockquote>', '</p>']
        self_closing_tags = ['<li>', '<img', '<br']

        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                processed.append('')
                continue

            # Check if we're entering an HTML block
            if any(stripped.startswith(tag) for tag in block_tags):
                in_html_block = True
                processed.append(line)
            # Check if we're leaving an HTML block
            elif any(stripped.endswith(tag) for tag in closing_tags):
                processed.append(line)
                in_html_block = False
            # Check if line is already HTML
            elif stripped.startswith('<') or in_html_block:
                processed.append(line)
            else:
                # Regular text line - wrap in paragraph if not already wrapped
                if not any(line.strip().startswith(f'<{tag}') for tag in ['p', 'li', 'h1', 'h2', 'h3', 'ul', 'ol', 'pre', 'code']):
                    processed.append(f'<p>{line}</p>')
                else:
                    processed.append(line)

        html = '\n'.join(processed)

        # Clean up multiple newlines
        html = re.sub(r'\n{3,}', '\n\n', html)

        return html

    def escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text

    def to_html(self) -> str:
        """Convert post to HTML"""
        title = self.frontmatter.get('title', 'Untitled')
        description = self.frontmatter.get('description', '')
        date = self.get_date()
        tags = self.frontmatter.get('tags', [])

        content_html = self.convert_markdown_to_html(self.content)

        return self.get_post_template(title, description, date, tags, content_html)

    def get_post_template(self, title: str, description: str, date: datetime, tags: List[str], content: str) -> str:
        """Generate HTML template for post"""
        tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in tags]) if isinstance(tags, list) else ''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Egor Gorchakov's Blog</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">Egor Gorchakov</a>
            <a href="/">Home</a>
        </nav>
    </header>

    <main>
        <article class="post">
            <header class="post-header">
                <h1>{title}</h1>
                <div class="post-meta">
                    <time datetime="{date.strftime('%Y-%m-%d')}">{date.strftime('%B %d, %Y')}</time>
                    {f'<div class="tags">{tags_html}</div>' if tags_html else ''}
                </div>
            </header>

            <div class="post-content">
                {content}
            </div>
        </article>
    </main>

    <footer>
        <p>&copy; {datetime.now().year} Egor Gorchakov. All rights reserved.</p>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</body>
</html>'''


def create_index_page(posts: List[Post]) -> str:
    """Create index.html with all posts listed"""
    # Sort posts by date (newest first)
    posts_sorted = sorted(posts, key=lambda p: p.get_date(), reverse=True)

    posts_html = []
    for post in posts_sorted:
        title = post.frontmatter.get('title', 'Untitled')
        description = post.frontmatter.get('description', '')
        date = post.get_date()
        slug = post.get_url_slug()
        tags = post.frontmatter.get('tags', [])
        tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in tags]) if isinstance(tags, list) else ''

        posts_html.append(f'''
        <article class="post-preview">
            <h2><a href="/{slug}/">{title}</a></h2>
            <div class="post-meta">
                <time datetime="{date.strftime('%Y-%m-%d')}">{date.strftime('%B %d, %Y')}</time>
                {f'<div class="tags">{tags_html}</div>' if tags_html else ''}
            </div>
            <p>{description}</p>
        </article>''')

    posts_list = '\n'.join(posts_html)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Egor Gorchakov's Blog</title>
    <meta name="description" content="Software development blog by Egor Gorchakov">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">Egor Gorchakov</a>
            <a href="/">Home</a>
        </nav>
    </header>

    <main>
        <div class="intro">
            <h1>Blog</h1>
            <p>Thoughts on software development, architecture, and technology</p>
        </div>

        <div class="posts-list">
            {posts_list}
        </div>
    </main>

    <footer>
        <p>&copy; {datetime.now().year} Egor Gorchakov. All rights reserved.</p>
    </footer>
</body>
</html>'''


def create_css() -> str:
    """Create CSS stylesheet"""
    return '''/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #fff;
}

/* Header */
header {
    background: #fff;
    border-bottom: 1px solid #e1e4e8;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

nav {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}

nav a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

nav a.logo {
    font-weight: 700;
    font-size: 1.2rem;
}

nav a:hover {
    color: #0366d6;
}

/* Main Content */
main {
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

/* Intro Section */
.intro {
    margin-bottom: 3rem;
}

.intro h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #1a1a1a;
}

.intro p {
    font-size: 1.2rem;
    color: #586069;
}

/* Posts List */
.posts-list {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
}

.post-preview {
    padding-bottom: 2.5rem;
    border-bottom: 1px solid #e1e4e8;
}

.post-preview:last-child {
    border-bottom: none;
}

.post-preview h2 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.post-preview h2 a {
    text-decoration: none;
    color: #1a1a1a;
}

.post-preview h2 a:hover {
    color: #0366d6;
}

.post-preview p {
    color: #586069;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

/* Post Meta */
.post-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin: 0.5rem 0;
}

.post-meta time {
    color: #586069;
    font-size: 0.95rem;
}

.tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.tag {
    background: #f1f8ff;
    color: #0366d6;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    font-size: 0.85rem;
    font-weight: 500;
}

/* Post Page */
.post {
    max-width: 750px;
}

.post-header {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e1e4e8;
}

.post-header h1 {
    font-size: 2.5rem;
    line-height: 1.2;
    margin-bottom: 1rem;
    color: #1a1a1a;
}

/* Post Content */
.post-content {
    font-size: 1.1rem;
    line-height: 1.8;
}

.post-content h1,
.post-content h2,
.post-content h3 {
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #1a1a1a;
    line-height: 1.3;
}

.post-content h1 {
    font-size: 2rem;
}

.post-content h2 {
    font-size: 1.6rem;
}

.post-content h3 {
    font-size: 1.3rem;
}

.post-content p {
    margin-bottom: 1.5rem;
}

.post-content a {
    color: #0366d6;
    text-decoration: none;
}

.post-content a:hover {
    text-decoration: underline;
}

.post-content ul,
.post-content ol {
    margin-bottom: 1.5rem;
    padding-left: 2rem;
}

.post-content li {
    margin-bottom: 0.5rem;
}

.post-content img {
    max-width: 100%;
    height: auto;
    margin: 1.5rem 0;
    border-radius: 5px;
}

.post-content figure {
    margin: 2rem 0;
    text-align: center;
}

.post-content figcaption {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #586069;
    font-style: italic;
}

/* Code Blocks */
.post-content code {
    background: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.9em;
}

.post-content pre {
    background: #1e1e1e;
    padding: 1.5rem;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1.5rem 0;
}

.post-content pre code {
    background: none;
    padding: 0;
    color: #e1e4e8;
    font-size: 0.9rem;
}

/* Footer */
footer {
    border-top: 1px solid #e1e4e8;
    padding: 2rem 0;
    margin-top: 4rem;
    text-align: center;
    color: #586069;
}

/* Responsive */
@media (max-width: 768px) {
    nav {
        padding: 0 1rem;
    }

    main {
        padding: 2rem 1rem;
    }

    .intro h1 {
        font-size: 2rem;
    }

    .post-header h1 {
        font-size: 2rem;
    }

    .post-preview h2 {
        font-size: 1.5rem;
    }

    .post-content {
        font-size: 1rem;
    }
}'''


def main():
    """Main conversion function"""
    base_dir = Path('/Users/egorg/Uber/egorikas.github.io')
    posts_dir = base_dir / '_posts'

    # Read all posts
    posts = []
    for md_file in sorted(posts_dir.glob('*.md')):
        post = Post(str(md_file))
        posts.append(post)

    print(f'Found {len(posts)} posts')

    # Create output directories and files
    for post in posts:
        slug = post.get_url_slug()
        post_dir = base_dir / slug
        post_dir.mkdir(exist_ok=True)

        # Write post HTML
        html = post.to_html()
        with open(post_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'Created /{slug}/')

    # Create index.html
    index_html = create_index_page(posts)
    with open(base_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    print('Created /index.html')

    # Create style.css
    css = create_css()
    with open(base_dir / 'style.css', 'w', encoding='utf-8') as f:
        f.write(css)

    print('Created /style.css')

    print(f'\nConversion complete! Created {len(posts)} post pages + index page')


if __name__ == '__main__':
    main()
