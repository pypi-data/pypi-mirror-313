# {file}`postcss.config.js` in the home folder

A {file}`postcss.config.js` file in the home folder will stop vite-based projects from building successfully.
This results in an error message such as the one shown below:

::::{error}

Failed to load PostCSS config: Failed to load PostCSS config (searchPath: /home/ou/TM352-23J/tmp/ema/ema-app/web): [Error] Loading PostCSS Plugin failed: Cannot find module 'tailwindcss'

::::

::::{admonition} Fix

You can fix this simply by deleting the {file}`postcss.config.js` in the home folder or by running

:::{code-block} console
$ tm352 vce check --fix
:::

::::
