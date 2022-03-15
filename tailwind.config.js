// Add opacity terms explicitly, to enable ourselves to use those values
// in theme() as `theme("colors.teal.600/20")`
function injectOpacityNested(theme, color) {
  let opacity = theme("opacity");
  let new_color = {};
  for (let key of Object.keys(color)) {
    new_color[key] = color[key];
    for (let opacity_key of Object.keys(opacity)) {
      new_color[`${key}/${opacity_key}`] = withOpacity(
        color[key],
        opacity[opacity_key]
      );
    }
  }
  return new_color;
}
function injectOpacitySingle(theme, key, color) {
  let opacity = theme("opacity");
  let new_color = {};
  new_color[key] = color;
  for (let opacity_key of Object.keys(opacity)) {
    new_color[`${key}/${opacity_key}`] = withOpacity(
      color,
      opacity[opacity_key]
    );
  }
  return new_color;
}

function withOpacity(color, opacity) {
  const _opacity = Math.round(Math.min(Math.max(opacity || 1, 0), 1) * 255);
  return color + _opacity.toString(16).toUpperCase();
}

module.exports = {
  content: ["src/*/theme/**/*.html"],
  darkMode: "class",
  theme: {
    fontSize: {
      xxxs: "0.625rem",
      xxs: "0.75rem",
      xs: "0.8125rem",
      sm: "0.875rem",
      base: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "3.75rem",
      "7xl": "4.5rem",
      "8xl": "6rem",
      "9xl": "8rem",
    },
    colors: ({ colors, theme }) => {
      return {
        inherit: colors.inherit,
        current: colors.current,
        transparent: colors.transparent,
        slate: injectOpacityNested(theme, colors.slate),
        gray: injectOpacityNested(theme, colors.gray),
        zinc: injectOpacityNested(theme, colors.zinc),
        neutral: injectOpacityNested(theme, colors.neutral),
        stone: injectOpacityNested(theme, colors.stone),
        red: injectOpacityNested(theme, colors.red),
        orange: injectOpacityNested(theme, colors.orange),
        amber: injectOpacityNested(theme, colors.amber),
        yellow: injectOpacityNested(theme, colors.yellow),
        lime: injectOpacityNested(theme, colors.lime),
        green: injectOpacityNested(theme, colors.green),
        emerald: injectOpacityNested(theme, colors.emerald),
        teal: injectOpacityNested(theme, colors.teal),
        cyan: injectOpacityNested(theme, colors.cyan),
        sky: injectOpacityNested(theme, colors.sky),
        blue: injectOpacityNested(theme, colors.blue),
        indigo: injectOpacityNested(theme, colors.indigo),
        violet: injectOpacityNested(theme, colors.violet),
        purple: injectOpacityNested(theme, colors.purple),
        fuchsia: injectOpacityNested(theme, colors.fuchsia),
        pink: injectOpacityNested(theme, colors.pink),
        rose: injectOpacityNested(theme, colors.rose),
        ...injectOpacitySingle(theme, "black", "#000000"),
        ...injectOpacitySingle(theme, "white", "#FFFFFF"),
      };
    },
  },
  extend: {
    maxWidth: {
      "8xl": "90rem",
    },
  },
};
