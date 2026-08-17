import * as React from "react";

import { cn } from "@/lib/utils";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => (
    <input
      type={type}
      className={cn(
        "flex h-10 w-full rounded-md border border-white/15 bg-[#0f0e0e] px-3 py-2 text-sm text-white ring-offset-[#0f0e0e] transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-white/35 hover:border-white/25 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#fe2e4b] disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      ref={ref}
      {...props}
    />
  ),
);
Input.displayName = "Input";

export { Input };
