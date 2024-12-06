# Genopen

<div align="center">

![Genopen Logo](./logo.ico)

</div>

Genopen is a Python application that allows you to create blogs easily and quickly from content written in Markdown. Whether you are a writer, a developer, or just someone who wants to share their thoughts online, Genopen provides an intuitive command-line interface to easily generate blogs ready to be published.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating a Project](#creating-a-project)
  - [Adding Posts](#adding-posts)
  - [Generating the Blog](#generating-the-blog)
- [Project Structure](#project-structure)
- [Themes](#themes)
- [Configuration](#configuration)
- [License](#license)

## Features

- **Project Creation**: Generate a new empty project.
- **Markdown Writing**: Add posts using Markdown syntax, which will be automatically converted to HTML.
- **Customizable Themes**: Use the default theme or create your own to customize the appearance of your blog.
- **Automatic Generation**: Convert all your posts into a complete static website.
- **Sitemap and RSS**: Automatically generate a sitemap and an RSS feed for your blog.

## Installation

Make sure you have Python installed on your machine. Then, clone the repository and install the dependencies:

```sh
# Clone the repository
$ git clone https://github.com/your-username/genopen.git

# Navigate to the project directory
$ cd genopen

# Install the dependencies
$ pip install -r requirements.txt

# Install the application locally
$ pip install .
```

## Usage

Genopen is used via a command-line interface (CLI). Here are the main commands:

### Creating a Project

To create a new blog project:

```sh
$ genopen create <project_name>
```

This command creates a new directory containing the necessary structure to start working on your blog.

### Adding Posts

Once the project is created, you can add new posts:

```sh
$ cd <project_name>
$ genopen add "Title of Your Post"
```

This command creates a pre-filled Markdown file with the title and necessary metadata.

### Generating the Blog

To generate the HTML pages for your blog:

```sh
$ genopen build
```

The generated blog will be placed in a directory named `web/`. This directory will contain all the pages and resources ready to be deployed on a server.

## Project Structure

Here is an overview of the project structure:

```
<project_name>/
  |-- content/
  |    |-- posts/               # Contains the blog posts in Markdown
  |    |-- assets/              # Contains images and other resources for the posts
  |
  |-- themes/                   # Contains themes to customize your blog
  |    |-- default/             # Default theme
  |
  |-- genopen.config            # Project configuration file
  |-- web/                      # Generated folder containing the final blog
```

## Themes

The `themes/` folder contains HTML, CSS, and other resources needed to customize the appearance of your blog. By default, Genopen includes a simple theme, but you can create and use your own themes.

### Creating a New Theme

To create a new theme, add a folder under `themes/` and include the HTML files (e.g., `index.html`, `post.html`) as well as the CSS and other necessary resources. Update the configuration (`genopen.config`) to point to the new theme.

## Configuration

The `genopen.config` file allows you to configure your blog.

- **Mandatory Variables**: The following three variables are required for the `genopen build` command:

  - `theme`: Specifies the theme to be used.
  - `date_format`: Defines the date format.
  - `locale`: Sets the language and local format.

- **Theme-Specific Variables**: Other variables (e.g., `blog_name`, `domain`) are optional and depend on the theme being used. You can define them in the configuration file if your theme requires them.

- **Environment Variables**: Sensitive data (e.g., API keys) can be configured using environment variables with a defined prefix (`environment_prefix`). This allows secrets to be securely managed.

## License

This project is licensed under the [MIT License](./LICENSE). You are free to use, modify, and distribute it as you wish.
