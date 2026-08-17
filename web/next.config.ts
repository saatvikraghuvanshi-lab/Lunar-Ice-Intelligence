import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === "production";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  async headers() {
    return [
      {
        // Apply to all routes, including API routes and static assets.
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
          },
          // HSTS only makes sense over TLS; skip it on localhost dev.
          ...(isProd
            ? [
                {
                  key: "Strict-Transport-Security",
                  value: "max-age=63072000; includeSubDomains",
                },
              ]
            : []),
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              // Next.js embeds its RSC bootstrap as inline scripts, and
              // next/font emits inline styles, so 'unsafe-inline' is required.
              `script-src 'self' 'unsafe-inline'${isProd ? "" : " 'unsafe-eval' ws://localhost:* ws://127.0.0.1:*"}`,
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data: blob:",
              "font-src 'self' data:",
              "connect-src 'self'",
              // The evidence console embeds the demo dashboard same-origin.
              "frame-src 'self'",
              "object-src 'none'",
              "base-uri 'self'",
              "form-action 'self'",
              "frame-ancestors 'self'",
            ].join("; "),
          },
        ],
      },
    ];
  },
};

export default nextConfig;
