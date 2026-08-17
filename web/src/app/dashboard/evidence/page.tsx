import { redirect } from "next/navigation";
import { ExternalLink, LogOut } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";
import { getCurrentUser } from "@/lib/auth";
import { cn } from "@/lib/utils";

// Same-origin: the demo dashboard ships in web/public/demo, so it works in
// local dev and in a serverless deploy (Vercel) without any extra server.
const evidenceConsoleUrl = "/demo/index.html";
const evidencePages = [
  ["Mission", `${evidenceConsoleUrl}?page=mission`],
  ["Requirements", `${evidenceConsoleUrl}?page=requirements`],
  ["Evidence Ledger", `${evidenceConsoleUrl}?page=details`],
] as const;

export default async function EvidenceConsolePage() {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <main className="grid min-h-screen grid-rows-[auto_1fr_auto] bg-[#0f0e0e] text-white">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-white/15 bg-[#161316]/95 px-4 py-3">
        <div className="flex items-center gap-3">
          <form action="/api/auth/logout" method="post">
            <button
              type="submit"
              className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "text-white/75")}
            >
              <LogOut className="size-4" />
              Logout
            </button>
          </form>
          <div>
            <p className="text-xs uppercase tracking-normal text-[#ff8a98]">
              Integrated demo shell
            </p>
            <h1 className="text-base font-semibold">
              Lunar Ice Evidence Console
            </h1>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {evidencePages.map(([label, href]) => (
            <a
              key={label}
              className={buttonVariants({ variant: "ghost", size: "sm" })}
              href={href}
              target="evidenceFrame"
            >
              {label}
            </a>
          ))}
          <a
            className={buttonVariants({ variant: "outline", size: "sm" })}
            href={evidenceConsoleUrl}
            target="_blank"
            rel="noreferrer"
          >
            Open original
            <ExternalLink className="size-4" />
          </a>
        </div>
      </header>

      <section className="min-h-0 bg-black">
        <iframe
          name="evidenceFrame"
          title="Existing evidence dashboard demo"
          src={`${evidenceConsoleUrl}?page=mission`}
          className="h-full min-h-[calc(100vh-65px)] w-full border-0"
        />
      </section>

      <footer className="flex flex-wrap items-center justify-between gap-2 border-t border-white/10 bg-[#161316]/95 px-4 py-2 text-xs text-white/50">
        <span>
          Evidence console runs same-origin at{" "}
          <code className="text-white/70">/demo/index.html</code> — no extra server needed.
        </span>
        <span>
          Standalone copy:{" "}
          <code className="text-white/70">python -m http.server 8765 -d .</code> →{" "}
          <code className="text-white/70">localhost:8765/demo/index.html</code>
        </span>
      </footer>
    </main>
  );
}
