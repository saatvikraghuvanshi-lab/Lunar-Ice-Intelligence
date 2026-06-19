import { NextResponse } from "next/server";

import { createSession, hashPassword } from "@/lib/auth";
import { createUser, findUserByEmail } from "@/lib/user-store";
import { signupSchema } from "@/lib/validation";

const TERMS_VERSION = "2026-06-19";

export async function POST(request: Request) {
  const payload = await request.json().catch(() => null);
  const parsed = signupSchema.safeParse(payload);

  if (!parsed.success) {
    return NextResponse.json(
      { message: parsed.error.issues[0]?.message ?? "Invalid signup details" },
      { status: 400 },
    );
  }

  const existing = await findUserByEmail(parsed.data.email);

  if (existing) {
    return NextResponse.json(
      { message: "An account with this email already exists." },
      { status: 409 },
    );
  }

  const user = await createUser({
    name: parsed.data.name,
    email: parsed.data.email,
    passwordHash: await hashPassword(parsed.data.password),
    termsVersion: TERMS_VERSION,
  });

  await createSession(user.id);

  return NextResponse.json({
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
    },
  });
}
