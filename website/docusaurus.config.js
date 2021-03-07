module.exports = {
  title: "curlylint",
  tagline:
    "Experimental HTML templates linting for Jinja, Nunjucks, Django templates, Twig, Liquid",
  url: "https://www.curlylint.org",
  baseUrl: "/",
  favicon: "img/favicon.ico",
  organizationName: "thibaudcolas",
  projectName: "curlylint",
  themeConfig: {
    googleAnalytics: {
      trackingID: "UA-170227698-1",
      anonymizeIP: true,
    },
    prism: {
      theme: {
        plain: {
          color: "#393A34",
          backgroundColor: "#f6f8fa",
        },
        styles: [
          {
            types: ["comment", "prolog", "doctype", "cdata"],
            style: {
              color: "#999988",
              fontStyle: "italic",
            },
          },
          {
            types: ["namespace"],
            style: {
              opacity: 0.7,
            },
          },
          {
            types: ["string", "attr-value"],
            style: {
              color: "#e3116c",
            },
          },
          {
            types: ["punctuation", "operator"],
            style: {
              color: "#393A34",
            },
          },
          {
            types: [
              "entity",
              "url",
              "symbol",
              "number",
              "boolean",
              "variable",
              "constant",
              "property",
              "regex",
              "inserted",
            ],
            style: {
              color: "#36acaa",
            },
          },
          {
            types: ["atrule", "keyword", "attr-name", "selector"],
            style: {
              color: "#00a4db",
            },
          },
          {
            types: ["function", "deleted", "tag"],
            style: {
              color: "#d73a49",
            },
          },
          {
            types: ["function-variable"],
            style: {
              color: "#6f42c1",
            },
          },
          {
            types: ["tag", "selector", "keyword"],
            style: {
              color: "#00009f",
            },
          },
        ],
      },
      darkTheme: require("prism-react-renderer/themes/dracula"),
      additionalLanguages: ["toml"],
    },
    navbar: {
      title: "curlylint",
      // hideOnScroll: true,
      logo: {
        alt: "",
        src: "img/curlylint-logo.svg",
      },
      items: [
        {
          to: "docs/",
          activeBasePath: "docs",
          label: "Docs",
          position: "left",
        },
        { to: "blog", label: "Blog", position: "left" },
        {
          href: "https://github.com/thibaudcolas/curlylint",
          label: "GitHub",
          position: "left",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Getting Started",
              to: "docs/",
            },
            {
              label: "Rules",
              to: "docs/rules/all",
            },
            {
              label: "Ideas",
              to: "docs/reference/ideas",
            },
          ],
        },
        // {
        //   title: "Community",
        //   items: [
        //     { label: "Help", href: "" },
        //     { label: "About", href: "" },
        //     { label: "Code of conduct", href: "" },
        //   ],
        // },
        {
          title: "More",
          items: [
            {
              label: "Blog",
              to: "blog",
            },
            {
              label: "GitHub",
              href: "https://github.com/thibaudcolas/curlylint",
            },
            {
              label: "Twitter",
              href: "https://twitter.com/thibaud_colas",
            },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Thibaud Colas. Emojis by <a href="https://github.com/mozilla/fxemoji">FxEmojis</a>. Powered by <a href="https://www.netlify.com/">Netlify</a>. <a href="https://github.com/thibaudcolas/curlylint/tree/main/website">Edit on GitHub</a>.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          // It is recommended to set document id as docs home page (`docs/` path).
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl:
            "https://github.com/thibaudcolas/curlylint/edit/main/website/",
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            "https://github.com/thibaudcolas/curlylint/edit/main/website/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
  plugins: [require.resolve("docusaurus-lunr-search")],
};
