import Link from "next/link";
import { ArrowLeft, ExternalLink } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const evidenceConsoleUrl = "http://localhost:8765/demo/index.html";

export default function EvidenceConsolePage() {
  return (
    <main className="grid min-h-screen grid-rows-[auto_1fr] bg-slate-950 text-slate-50">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 bg-slate-950/95 px-4 py-3">
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className={cn(buttonVariants({ variant: "ghost", size: "sm" }), "text-slate-300")}
          >
            <ArrowLeft className="size-4" />
            Login
          </Link>
          <div>
            <p className="text-xs uppercase tracking-normal text-cyan-200">
              Integrated demo shell
            </p>
            <h1 className="text-base font-semibold">
              Lunar Ice Evidence Console
            </h1>
          </div>
        </div>
        <a
          className={buttonVariants({ variant: "outline", size: "sm" })}
          href={evidenceConsoleUrl}
          target="_blank"
          rel="noreferrer"
        >
          Open original
          <ExternalLink className="size-4" />
        </a>
      </header>

      <section className="min-h-0 bg-black">
        <iframe
          title="Existing evidence dashboard demo"
          src={evidenceConsoleUrl}
          className="h-full min-h-[calc(100vh-65px)] w-full border-0"
        />
      </section>
    </main>
  );
}
