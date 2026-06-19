import { redirect } from "next/navigation";
import Link from "next/link";

import { getCurrentUser } from "@/lib/auth";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function DashboardPage() {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-50">
      <div className="mx-auto grid max-w-6xl gap-6">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-5">
          <div>
            <p className="text-sm uppercase tracking-normal text-cyan-200">
              Mission workspace
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">
              Welcome, {user.name}
            </h1>
          </div>
          <Link className={buttonVariants({ variant: "outline" })} href="/dashboard/evidence">
            Open evidence console
          </Link>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          {[
            ["Saved AOIs", "Next: persist selected south-pole areas per user."],
            ["Judge Demo Runs", "Next: store walkthrough notes and selected layer sequence."],
            ["Mission Reports", "Next: link generated PDFs to the signed-in account."],
          ].map(([title, copy]) => (
            <Card key={title}>
              <CardHeader>
                <CardTitle>{title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm leading-6 text-slate-400">
                {copy}
              </CardContent>
            </Card>
          ))}
        </section>

        <Card>
          <CardContent className="p-6 text-sm leading-7 text-slate-300">
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
