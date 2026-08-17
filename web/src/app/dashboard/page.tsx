import { redirect } from "next/navigation";
import Link from "next/link";
import { LogOut } from "lucide-react";

import { getCurrentUser } from "@/lib/auth";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default async function DashboardPage() {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <main className="min-h-screen bg-[#0f0e0e] p-6 text-white">
      <div className="mx-auto grid max-w-6xl gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/15 pb-5">
          <div>
            <p className="text-sm uppercase tracking-normal text-[#ff8a98]">
              Mission workspace
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Welcome, {user.name}
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <Link className={buttonVariants({ variant: "outline" })} href="/dashboard/evidence">
              Open evidence console
            </Link>
            <form action="/api/auth/logout" method="post">
              <button
                type="submit"
                className={cn(buttonVariants({ variant: "ghost" }), "text-white/75")}
              >
                <LogOut className="size-4" />
                Logout
              </button>
            </form>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            ["Saved AOIs", "Persist selected south-pole areas per user."],
            ["Judge Demo Runs", "Store walkthrough notes and selected layer sequence."],
            ["Mission Reports", "Link generated PDFs to the signed-in account."],
          ].map(([title, copy]) => (
            <Card
              key={title}
              className="transition hover:border-white/25 hover:bg-white/[0.03]"
            >
              <CardHeader>
                <div className="flex items-center justify-between gap-3">
                  <CardTitle>{title}</CardTitle>
                  <span className="rounded-full border border-[#f2bf5a]/40 bg-[#f2bf5a]/10 px-2.5 py-0.5 text-[11px] uppercase tracking-wide text-[#ffe4a8]">
                    Planned
                  </span>
                </div>
              </CardHeader>
              <CardContent className="text-sm leading-6 text-white/60">
                {copy}
              </CardContent>
            </Card>
          ))}
        </section>

        <Card>
          <CardContent className="p-6 text-sm leading-7 text-white/70">
            Auth, sessions, user database schema, and terms acceptance are now in
            place. The next integration step is to mount the existing evidence
            dashboard inside this authenticated shell and start saving user
            workspace state.
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
