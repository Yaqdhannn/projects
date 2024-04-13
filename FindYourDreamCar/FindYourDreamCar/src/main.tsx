import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
// import "bootstrap"; // probably need to be fixed

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
