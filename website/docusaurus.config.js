const path = require("path");

module.exports = {
  title: "curlylint",
  tagline:
    "Experimental linter for Jinja, Nunjucks, Django templates, Twig, Liquid",
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
      theme: require("prism-react-renderer/themes/github"),
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
      links: [
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
              to: "docs/rules/",
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
          homePageId: "getting-started",
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
  plugins: [path.resolve(__dirname, "./node_modules/docusaurus-lunr-search/")],
};
