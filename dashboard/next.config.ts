import type { NextConfig } from "next";
import path from "node:path";
const config: NextConfig = {
  output: "export",
  generateBuildId: async () =>
    process.env.FINGROWTH_BUILD_ID ?? "fingrowth-0.1.0",
  trailingSlash: true,
  turbopack: { root: path.resolve(process.cwd(), "..") },
};
export default config;
