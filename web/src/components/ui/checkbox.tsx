import * as React from "react";
import { Check } from "lucide-react";

import { cn } from "@/lib/utils";

export type CheckboxProps = Omit<React.InputHTMLAttributes<HTMLInputElement>, "type">;

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, ...props }, ref) => (
    <span className="relative inline-grid size-4 place-items-center">
      <input
        ref={ref}
        type="checkbox"
        className={cn(
          "peer size-4 appearance-none rounded border border-white/25 bg-[#0f0e0e] checked:border-[#fe2e4b] checked:bg-[#fe2e4b] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#fe2e4b]",
          className,
        )}
        {...props}
      />
      <Check className="pointer-events-none absolute size-3 text-white opacity-0 peer-checked:opacity-100" />
    </span>
  ),
);
Checkbox.displayName = "Checkbox";
