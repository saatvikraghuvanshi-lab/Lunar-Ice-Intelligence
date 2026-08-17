import crypto from "crypto";
import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";
import type { User as PrismaUser } from "@prisma/client";

import { prisma } from "@/lib/db";

export type StoredUser = {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  role: "MEMBER" | "ADMIN";
  createdAt: string;
  updatedAt: string;
};

type StoredSession = {
  id: string;
  token: string;
  userId: string;
  expiresAt: string;
  createdAt: string;
};

type StoredTermsAcceptance = {
  id: string;
  userId: string;
  version: string;
  createdAt: string;
};

type Store = {
  users: StoredUser[];
  sessions: StoredSession[];
  termsAcceptances: StoredTermsAcceptance[];
};

// Local development uses a JSON file so no database is required. In production
// (Vercel) DATABASE_URL points at a hosted PostgreSQL (Supabase/Neon) and the
// Prisma schema in web/prisma/schema.prisma is used instead.
const useDatabase = (process.env.DATABASE_URL ?? "").startsWith("postgres");

function toStoredUser(user: PrismaUser): StoredUser {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    passwordHash: user.passwordHash,
    role: user.role,
    createdAt: user.createdAt.toISOString(),
    updatedAt: user.updatedAt.toISOString(),
  };
}

/* ------------------------------------------------------------------ */
/* JSON file store (local dev)                                         */
/* ------------------------------------------------------------------ */

const storePath = path.join(process.cwd(), ".local", "users.json");

async function readStore(): Promise<Store> {
  try {
    return JSON.parse(await readFile(storePath, "utf8")) as Store;
  } catch {
    return { users: [], sessions: [], termsAcceptances: [] };
  }
}

async function writeStore(store: Store) {
  await mkdir(path.dirname(storePath), { recursive: true });
  await writeFile(storePath, JSON.stringify(store, null, 2));
}

/* ------------------------------------------------------------------ */
/* Shared API                                                          */
/* ------------------------------------------------------------------ */

export async function findUserByEmail(email: string) {
  if (useDatabase) {
    const user = await prisma.user.findUnique({ where: { email } });
    return user ? toStoredUser(user) : null;
  }

  const store = await readStore();
  return store.users.find((user) => user.email === email) ?? null;
}

export async function findUserBySessionToken(token: string) {
  if (useDatabase) {
    const session = await prisma.session.findUnique({
      where: { token },
      include: { user: true },
    });

    if (!session || session.expiresAt < new Date()) {
      return null;
    }

    return toStoredUser(session.user);
  }

  const store = await readStore();
  const session = store.sessions.find((item) => item.token === token);

  if (!session || new Date(session.expiresAt) < new Date()) {
    return null;
  }

  return store.users.find((user) => user.id === session.userId) ?? null;
}

export async function deleteSessionByToken(token: string) {
  if (useDatabase) {
    await prisma.session.deleteMany({ where: { token } });
    return;
  }

  const store = await readStore();
  const remaining = store.sessions.filter((item) => item.token !== token);

  if (remaining.length !== store.sessions.length) {
    store.sessions = remaining;
    await writeStore(store);
  }
}

export async function createUser(input: {
  name: string;
  email: string;
  passwordHash: string;
  termsVersion: string;
}) {
  if (useDatabase) {
    const user = await prisma.user.create({
      data: {
        name: input.name,
        email: input.email,
        passwordHash: input.passwordHash,
        termsAcceptances: {
          create: { version: input.termsVersion },
        },
      },
    });
    return toStoredUser(user);
  }

  const store = await readStore();
  const now = new Date().toISOString();
  const user: StoredUser = {
    id: crypto.randomUUID(),
    name: input.name,
    email: input.email,
    passwordHash: input.passwordHash,
    role: "MEMBER",
    createdAt: now,
    updatedAt: now,
  };

  store.users.push(user);
  store.termsAcceptances.push({
    id: crypto.randomUUID(),
    userId: user.id,
    version: input.termsVersion,
    createdAt: now,
  });

  await writeStore(store);
  return user;
}

export async function createStoredSession(input: {
  token: string;
  userId: string;
  expiresAt: Date;
}) {
  if (useDatabase) {
    // Drop expired sessions while we are here so the table does not grow forever.
    await prisma.session.deleteMany({ where: { expiresAt: { lt: new Date() } } });
    await prisma.session.create({
      data: {
        token: input.token,
        userId: input.userId,
        expiresAt: input.expiresAt,
      },
    });
    return;
  }

  const store = await readStore();
  // Drop expired sessions while we are here so the store does not grow forever.
  store.sessions = store.sessions.filter(
    (session) => new Date(session.expiresAt) > new Date(),
  );
  store.sessions.push({
    id: crypto.randomUUID(),
    token: input.token,
    userId: input.userId,
    expiresAt: input.expiresAt.toISOString(),
    createdAt: new Date().toISOString(),
  });
  await writeStore(store);
}
