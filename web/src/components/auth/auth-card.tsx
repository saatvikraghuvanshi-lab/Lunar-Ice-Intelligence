"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { AlertCircle, ArrowRight, LockKeyhole, Mail, UserRound } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type Mode = "login" | "signup";

type AuthCardProps = {
  mode: Mode;
};

export function AuthCard({ mode }: AuthCardProps) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isSignup = mode === "signup";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") ?? ""),
      email: String(form.get("email") ?? ""),
      password: String(form.get("password") ?? ""),
      acceptedTerms: form.get("acceptedTerms") === "on",
    };

    const response = await fetch(`/api/auth/${mode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(isSignup ? payload : {
        email: payload.email,
        password: payload.password,
      }),
    });

    const body = (await response.json().catch(() => ({}))) as {
      message?: string;
    };

    setLoading(false);

    if (!response.ok) {
      setError(body.message ?? "Something went wrong. Try again.");
      return;
    }

    router.push("/dashboard/evidence");
  }

  return (
    <Card className="w-full max-w-md border-white/15 bg-[#161316]/94 shadow-2xl shadow-[#fe2e4b]/10">
      <CardHeader>
        <div className="mb-3 flex size-11 items-center justify-center rounded-md border border-[#fe2e4b]/55 bg-[#fe2e4b]/12 text-white shadow-lg shadow-[#fe2e4b]/10">
          <LockKeyhole className="size-5" />
        </div>
        <CardTitle>{isSignup ? "Create your mission account" : "Welcome back"}</CardTitle>
        <CardDescription>
          {isSignup
            ? "Save candidate AOIs, review judge-demo runs, and keep an audit trail for your team."
            : "Sign in to continue your mission workspace."}
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="grid gap-4">
          {isSignup ? (
            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <div className="relative">
                <UserRound className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-white/38" />
                <Input id="name" name="name" autoComplete="name" autoFocus className="pl-9" placeholder="Mission team lead" />
              </div>
            </div>
          ) : null}

          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Mail className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-white/38" />
              <Input
                id="email"
                name={isSignup ? "email" : undefined}
                type="email"
                autoComplete="email"
                autoFocus={!isSignup}
                className="pl-9"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name={isSignup ? "password" : undefined}
              type="password"
              autoComplete={isSignup ? "new-password" : "current-password"}
              minLength={isSignup ? 8 : undefined}
              placeholder={isSignup ? "At least 8 characters" : "Your password"}
            />
          </div>

          {isSignup ? (
            <label className="flex items-start gap-3 rounded-md border border-white/15 bg-white/[0.04] p-3 text-sm text-white/72">
              <Checkbox name="acceptedTerms" />
              <span>
                I accept the{" "}
                <Link href="/terms" className="text-[#ff8a98] underline-offset-4 hover:underline">
                  Terms of Use
                </Link>{" "}
                and understand this is a decision-support prototype, not a source of confirmed lunar ice claims.
              </span>
            </label>
          ) : null}

          {error ? (
            <div
              role="alert"
              className="flex items-start gap-2 rounded-md border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-100"
            >
              <AlertCircle className="mt-0.5 size-4 shrink-0" />
              <span>{error}</span>
            </div>
          ) : null}
        </CardContent>
        <CardFooter className="grid gap-4">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Working..." : isSignup ? "Create account" : "Sign in"}
            <ArrowRight />
          </Button>
          <p className="text-center text-sm text-white/58">
            {isSignup ? "Already have an account?" : "New to the workspace?"}{" "}
            <Link
              href={isSignup ? "/login" : "/signup"}
              className="font-medium text-[#ff8a98] underline-offset-4 hover:underline"
            >
              {isSignup ? "Sign in" : "Create account"}
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
