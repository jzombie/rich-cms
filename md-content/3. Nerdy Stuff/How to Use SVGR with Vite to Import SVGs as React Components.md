# How to Use SVGR with Vite to Import SVGs as React Components

Integrating SVGs into your React project can be seamless and efficient with the help of SVGR and Vite. SVGR transforms SVGs into React components, providing you with more control and flexibility over your SVG assets. In this blog post, we'll walk through the steps to set up and use SVGR with Vite in your React project.

## What is SVGR?

SVGR is a tool that transforms SVG files into React components. This allows you to import SVGs directly into your React components, making it easier to manipulate and style them using props.

## What is Vite?

Vite is a modern frontend build tool that provides a fast development server and optimizes the build process. It supports hot module replacement (HMR) and is designed to work well with modern JavaScript frameworks like React.

## Setting Up SVGR with Vite

1. **Install Vite and Create a React Project**

   First, make sure you have Node.js and npm installed. Then, create a new React project using Vite:

   ```sh
   npm create vite@latest my-react-app --template react
   cd my-react-app
   ```

2. **Install Necessary Dependencies**

   Next, install the necessary dependencies for SVGR and Vite:

   ```sh
   npm install @svgr/webpack vite-plugin-svgr
   ```

3. **Configure Vite**

   To use SVGR with Vite, you need to configure Vite to recognize SVG imports. Open `vite.config.js` and add the SVGR plugin:

   ```javascript
   // vite.config.js
   import { defineConfig } from 'vite';
   import react from '@vitejs/plugin-react';
   import svgr from 'vite-plugin-svgr';

   export default defineConfig({
     plugins: [react(), svgr()],
   });
   ```

4. **Import SVG as React Component**

   Now you can import SVG files as React components in your project. Create an SVG file (e.g., `logo.svg`) in your `src/assets` directory.

   ```jsx
   // src/App.jsx
   /// <reference types="vite-plugin-svgr/client" />
   import React from "react";
   import Logo from "@assets/logo.svg?react";

   function App() {
     return (
       <div className="App">
         <header className="App-header">
           <Logo width={100} height={100} />
           <p>Edit <code>src/App.jsx</code> and save to reload.</p>
         </header>
       </div>
     );
   }

   export default App;
   ```

   In the above code, `@assets/logo.svg?react` is the key part. The `?react` suffix tells Vite to process the SVG file using SVGR and convert it into a React component.

## Benefits of Using SVGR

1. **Reusable Components**: SVGs can be used as reusable React components, allowing you to pass props like `width`, `height`, and `fill` to customize them.
2. **Better Performance**: Importing SVGs as React components can lead to better performance since they are directly embedded into your HTML as inline SVGs.
3. **Easier Styling**: You can style your SVGs using CSS-in-JS libraries or standard CSS since they are part of your React component tree.

## Conclusion

Using SVGR with Vite simplifies the process of integrating and managing SVG assets in your React projects. By following the steps outlined above, you can quickly set up your environment to leverage the power of SVGR, making your development process more efficient and your codebase cleaner.

## References

- [SVGR Documentation](https://react-svgr.com/docs/getting-started/)
- [Vite Documentation](https://vitejs.dev/guide/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
