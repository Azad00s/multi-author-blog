# Multi-Author Blogging Platform (Django)

A complete multi-author blogging platform built with Django where users can register, authors can create/edit/delete posts, readers can comment and like posts, and admins manage everything through the Django admin panel.

## Features

- ✅ User authentication (register, login, logout)
- ✅ Reader and Author roles (promoted by admin)
- ✅ Blog posts with title, slug, content, featured image, category, tags, author, status (Draft/Published), view_count
- ✅ Categories and Tags management (via admin panel)
- ✅ Authors can create, edit, delete only their own posts
- ✅ Author Dashboard showing only their posts
- ✅ Draft posts hidden from public
- ✅ Paginated homepage (5 posts per page)
- ✅ Filter posts by category and tag
- ✅ Search posts by title or content (case-insensitive)
- ✅ Comment system (logged-in users only)
- ✅ Like system (toggle, one like per user per post)
- ✅ View count tracking (increments on each visit)
- ✅ Django admin panel for full site management

## Technology Stack

- **Python** 3.8+
- **Django** 6.0.7
- **SQLite** (development database)
- **Pillow** (image handling)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Azad00s/multi-author-blog.git
cd multi-author-blog
