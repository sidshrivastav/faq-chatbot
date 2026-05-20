import type { ReactNode } from "react";

type StatusBadgeProps = {
  children: ReactNode;
  tone?: "success" | "warning" | "danger" | "neutral";
};

const toneClasses: Record<NonNullable<StatusBadgeProps["tone"]>, string> = {
  success: "bg-emerald-50 text-emerald-800 ring-emerald-200",
  warning: "bg-amber-50 text-amber-800 ring-amber-200",
  danger: "bg-red-50 text-red-800 ring-red-200",
  neutral: "bg-slate-100 text-slate-800 ring-slate-200",
};

export function StatusBadge({ children, tone = "neutral" }: StatusBadgeProps) {
  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ring-1 ${toneClasses[tone]}`}>
      {children}
    </span>
  );
}
