import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex h-10 cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#fe2e4b] active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50 [&_svg]:size-4",
  {
    variants: {
      variant: {
        default: "bg-[#fe2e4b] text-white shadow-lg shadow-[#fe2e4b]/20 hover:bg-[#ff5169]",
        secondary: "bg-[#4b4a4b] text-white hover:bg-[#5a595a]",
        outline:
          "border border-white/20 bg-transparent text-white hover:bg-white/10",
        ghost: "text-white/78 hover:bg-white/10",
        destructive: "bg-[#fe2e4b] text-white hover:bg-[#ff5169]",
      },
      size: {
        default: "px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-6",
        icon: "size-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  ),
);
Button.displayName = "Button";

export { Button, buttonVariants };
