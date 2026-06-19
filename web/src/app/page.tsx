import Link from "next/link";
import { ArrowRight, Database, FileCheck2, ShieldCheck } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <section className="mx-auto grid min-h-screen w-full max-w-6xl content-center gap-10 px-6 py-12 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="grid content-center gap-8">
          <div className="inline-flex w-max items-center gap-2 rounded-md border border-cyan-300/30 bg-cyan-300/10 px-3 py-2 text-sm text-cyan-100">
            <ShieldCheck className="size-4" />
            Chandrayaan-2 evidence workspace
          </div>
          <div className="grid gap-5">
            <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-white">
              Lunar Ice Intelligence for candidate landing and rover traverse planning.
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-300">
              A Vercel-ready mission workspace for teams to save AOIs, review
              source-to-evidence decisions, and present a scientifically honest
              south-pole ice screening demo.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link className={cn(buttonVariants({ size: "lg" }), "inline-flex items-center gap-2")} href="/signup">
              Create account <ArrowRight className="size-4" />
            </Link>
            <Link className={buttonVariants({ variant: "outline", size: "lg" })} href="/login">
              Sign in
            </Link>
          </div>
        </div>

        <Card className="self-center">
          <CardContent className="grid gap-5 p-6">
            {[
              {
                icon: Database,
                title: "User database",
                copy: "Prisma-backed users, sessions, and terms acceptance records.",
              },
              {
                icon: FileCheck2,
                title: "Terms of Use",
                copy: "Clear prototype limits: candidate evidence, not confirmed ice.",
              },
              {
                icon: ShieldCheck,
                title: "Judge-ready trust layer",
                copy: "Auth gates the workspace and preserves a clean product story for deployment.",
              },
            ].map((item) => (
              <div key={item.title} className="grid grid-cols-[44px_1fr] gap-4 rounded-md border border-slate-800 bg-slate-900/50 p-4">
                <div className="grid size-11 place-items-center rounded-md bg-cyan-300/10 text-cyan-200">
                  <item.icon className="size-5" />
                </div>
                <div>
                  <h2 className="font-semibold text-white">{item.title}</h2>
                  <p className="mt-1 text-sm leading-6 text-slate-400">{item.copy}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>
    </main>
  );
}
