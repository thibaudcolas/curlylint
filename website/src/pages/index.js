import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import CodeSnippet from "@site/src/theme/CodeSnippet";
import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import useBaseUrl from "@docusaurus/useBaseUrl";
import styles from "./styles.module.css";

const install = `# Assuming you’re using Python 3.6+,
pip install curlylint
# Then run:
curlylint my/templates`;

const snippets = [
  {
    label: "Jinja & Nunjucks",
    language: "twig",
    code: `<form role="filter">
    {%- for field in search_form -%}
        {% include "field.njk" %}
    {%- endfor -%}
</form>`,
    annotations: [
      {
        file_path: "test.html",
        line: 1,
        column: 1,
        message: "The `role` attribute needs to have a valid value",
        code: "aria_role",
      },
    ],
  },
  {
    label: "Django Templates",
    language: "twig",
    code: `<form role="filter">
    {% for field in search_form %}
        {% include "field.html" with field=field %}
    {% endfor %}
</form>`,
    annotations: [
      {
        file_path: "test.html",
        line: 1,
        column: 1,
        message: "The `role` attribute needs to have a valid value",
        code: "aria_role",
      },
    ],
  },
  {
    label: "Twig",
    language: "twig",
    code: `<form role="filter">
    {% for field in search_form %}
        {% include "./field.twig" only %}
    {% endfor %}
</form>`,
    annotations: [
      {
        file_path: "test.html",
        line: 1,
        column: 1,
        message: "The `role` attribute needs to have a valid value",
        code: "aria_role",
      },
    ],
  },
];

const features = [
  {
    title: <>Templates-friendly</>,
    description: (
      <>
        Curlylint is meant to work directly with source templates, so it can be
        used like any other static analysis tool – in your IDE, Continuous
        Integration, or pre-commit hooks.
      </>
    ),
  },
  {
    title: <>Catch errors before your users do</>,
    description: (
      <>
        The sooner errors are caught, the easier to fix. Create valid,
        accessible HTML by default.
      </>
    ),
  },
  {
    title: <>Accessible by default</>,
    description: (
      <>
        Curlylint’s main purpose is to catch accessibility issues – use it as a
        good baseline, and spend valuable testing time on checks that cannot be
        automated.
      </>
    ),
  },
];

const Feature = ({ imageUrl, title, description }) => {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx("col col--4", styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt="" />
        </div>
      )}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
};

function Home() {
  const context = useDocusaurusContext();
  const { siteConfig = {} } = context;
  return (
    <Layout
      title={siteConfig.tagline}
      description="curlylint is an experimental linter for “curly braces” templates, and their HTML"
    >
      <header className={clsx("hero hero--primary", styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className={clsx(
                "button button--primary button--lg",
                styles.getStarted,
              )}
              to={useBaseUrl("docs/")}
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>
      <main>
        <div className="container">
          <div className="row">
            <div className="col col--5">
              <h2>Install and run</h2>
              <p>
                Grab curlylint from PyPI, and start HTML directly in your
                templates.
              </p>
              <CodeSnippet snippet={install} lang="bash"></CodeSnippet>
            </div>
            <div className="col col--7">
              {snippets && snippets.length && (
                <section className={styles.configSnippets}>
                  <Tabs
                    defaultValue={snippets[0].label}
                    values={snippets.map((props, idx) => {
                      return { label: props.label, value: props.label };
                    })}
                  >
                    {snippets.map(
                      ({ label, language, code, annotations }, idx) => (
                        <TabItem value={label}>
                          <CodeSnippet
                            key={idx}
                            className={styles.configSnippet}
                            snippet={code}
                            annotations={annotations}
                            lang={language}
                          ></CodeSnippet>
                        </TabItem>
                      ),
                    )}
                  </Tabs>
                </section>
              )}
            </div>
          </div>
        </div>
        <div className="container">
          <hr />
        </div>
        {features && features.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}

export default Home;
