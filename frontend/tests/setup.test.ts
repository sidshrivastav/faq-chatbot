import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(__dirname, "..");

describe("frontend setup contract", () => {
  it("defines the expected build and test scripts", () => {
    const packageJson = JSON.parse(readFileSync(resolve(root, "package.json"), "utf8"));

    expect(packageJson.scripts.build).toBe("vite build");
    expect(packageJson.scripts.test).toBe("vitest run");
    expect(packageJson.dependencies.react).toBeDefined();
    expect(packageJson.devDependencies.tailwindcss).toBeDefined();
  });

  it("includes Tailwind entrypoint directives", () => {
    const css = readFileSync(resolve(root, "src/styles/index.css"), "utf8");

    expect(css).toContain("@tailwind base");
    expect(css).toContain("@tailwind components");
    expect(css).toContain("@tailwind utilities");
  });
});
