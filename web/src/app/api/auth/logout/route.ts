import { NextResponse } from "next/server";
import { cookies } from "next/headers";

import { SESSION_COOKIE } from "@/lib/auth";
import { deleteSessionByToken } from "@/lib/user-store";

export async function POST(request: Request) {
  const cookieStore = await cookies();
  const token = cookieStore.get(SESSION_COOKIE)?.value;

  if (token) {
    await deleteSessionByToken(token);
  }

  cookieStore.set(SESSION_COOKIE, "", {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: 0,
  });

  return NextResponse.redirect(new URL("/login", request.url), 303);
}
