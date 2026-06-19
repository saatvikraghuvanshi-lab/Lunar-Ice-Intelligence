import { z } from "zod";

export const emailSchema = z.string().trim().email().max(254).toLowerCase();

export const signupSchema = z.object({
  name: z.string().trim().min(2, "Enter your name").max(80),
  email: emailSchema,
  password: z.string().min(8, "Use at least 8 characters").max(128),
  acceptedTerms: z.literal(true, {
    error: "You must accept the Terms of Use",
  }),
});

export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, "Password is required").max(128),
});
