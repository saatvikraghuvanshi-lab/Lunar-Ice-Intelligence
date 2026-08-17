import { NextResponse } from "next/server";

import { createSession, verifyPassword } from "@/lib/auth";
import { findUserByEmail } from "@/lib/user-store";
import { getClientIp, isRateLimited } from "@/lib/rate-limit";
import { loginSchema } from "@/lib/validation";

export async function POST(request: Request) {
  if (isRateLimited(`login:${getClientIp(request)}`)) {
    return NextResponse.json(
      { message: "Too many attempts. Please try again in a minute." },
      { status: 429 },
    );
  }

  const payload = await request.json().catch(() => null);
  const parsed = loginSchema.safeParse(payload);

  if (!parsed.success) {
    return NextResponse.json(
      { message: parsed.error.issues[0]?.message ?? "Invalid login details" },
      { status: 400 },
    );
  }

  const user = await findUserByEmail(parsed.data.email);

  if (!user || !(await verifyPassword(parsed.data.password, user.passwordHash))) {
    return NextResponse.json(
      { message: "Email or password is incorrect." },
      { status: 401 },
    );
  }

  await createSession(user.id);

  return NextResponse.json({
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
    },
  });
}
