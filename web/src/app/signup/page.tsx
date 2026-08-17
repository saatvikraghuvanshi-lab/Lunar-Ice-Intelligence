import Link from "next/link";

import { AuthCard } from "@/components/auth/auth-card";

export default function SignupPage() {
  return (
    <main className="grid min-h-screen bg-[#0f0e0e] px-6 py-10 text-white lg:grid-cols-[0.9fr_1.1fr]">
      <section className="hidden content-center border-r border-white/15 pr-12 lg:grid">
        <Link href="/" className="mb-10 text-sm font-medium text-[#ff8a98]">
          Lunar Ice Intelligence
        </Link>
        <h1 className="max-w-xl text-4xl font-semibold tracking-tight">
          Create a mission workspace with scientific guardrails.
        </h1>
        <p className="mt-5 max-w-lg text-white/60">
          The product account layer is intentionally simple for the hackathon:
          authenticated users, explicit terms acceptance, and a schema ready for
          saved AOIs and reports.
        </p>
      </section>
      <section className="grid place-items-center">
        <AuthCard mode="signup" />
      </section>
    </main>
  );
}
