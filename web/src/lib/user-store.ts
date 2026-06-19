import crypto from "crypto";
import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";

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

export async function findUserByEmail(email: string) {
  const store = await readStore();
  return store.users.find((user) => user.email === email) ?? null;
}

export async function findUserBySessionToken(token: string) {
  const store = await readStore();
  const session = store.sessions.find((item) => item.token === token);

  if (!session || new Date(session.expiresAt) < new Date()) {
    return null;
  }

  return store.users.find((user) => user.id === session.userId) ?? null;
}

export async function createUser(input: {
  name: string;
  email: string;
  passwordHash: string;
  termsVersion: string;
}) {
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
  const store = await readStore();
  store.sessions.push({
    id: crypto.randomUUID(),
    token: input.token,
    userId: input.userId,
    expiresAt: input.expiresAt.toISOString(),
    createdAt: new Date().toISOString(),
  });
  await writeStore(store);
}
