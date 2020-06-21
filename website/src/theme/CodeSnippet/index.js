import React, { useEffect, useState } from "react";

import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import useThemeContext from "@theme/hooks/useThemeContext";

import Highlight, { defaultProps } from "prism-react-renderer";
import Prism from "prism-react-renderer/prism";

import monokai from "@site/src/plugins/prism_themes/monokai";

import styles from "./CodeSnippet.module.css";

(typeof global !== "undefined" ? global : window).Prism = Prism;

require("prismjs/components/prism-django");
require("prismjs/components/prism-twig");
require("prismjs/components/prism-liquid");

const getAnnotation = (annotations, line) => {
  return annotations
    .filter((a) => a.line === line + 1)
    .map((a) => a.message)
    .join("\n");
};

function CodeSnippet(props) {
  const {
    siteConfig: {
      themeConfig: { prism = {} },
    },
  } = useDocusaurusContext();

  const [mounted, setMounted] = useState(false);
  // The Prism theme on SSR is always the default theme but the site theme
  // can be in a different mode. React hydration doesn't update DOM styles
  // that come from SSR. Hence force a re-render after mounting to apply the
  // current relevant styles. There will be a flash seen of the original
  // styles seen using this current approach but that's probably ok. Fixing
  // the flash will require changing the theming approach and is not worth it
  // at this point.
  useEffect(() => {
    setMounted(true);
  }, []);

  const { isDarkTheme } = useThemeContext();
  const lightModeTheme = prism.theme || monokai;
  const darkModeTheme = prism.darkTheme || lightModeTheme;
  const prismTheme = isDarkTheme ? darkModeTheme : lightModeTheme;

  const { lang = "html", snippet, annotations = [] } = props;

  return (
    <Highlight
      {...defaultProps}
      key={mounted}
      theme={prismTheme}
      code={snippet}
      language={lang}
    >
      {({ className, style, tokens, getLineProps, getTokenProps }) => (
        <pre className={className} style={style}>
          {tokens.map((line, i) => {
            const annotation = getAnnotation(annotations, i);

            if (annotation) {
              return (
                <div {...getLineProps({ line, key: i })}>
                  <span className={styles.annotation} title={annotation}>
                    {line.map((token, key) => {
                      return <span {...getTokenProps({ token, key })} />;
                    })}
                  </span>
                </div>
              );
            }

            return (
              <div {...getLineProps({ line, key: i })}>
                {line.map((token, key) => {
                  return <span {...getTokenProps({ token, key })} />;
                })}
              </div>
            );
          })}
        </pre>
      )}
    </Highlight>
  );
}

export default CodeSnippet;
