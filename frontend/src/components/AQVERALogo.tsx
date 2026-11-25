"use client";

export interface AQVERALogoProps {
  size?: number;
  variant?: "light" | "dark";
  className?: string;
}

/**
 * AQVERA Brand Mark — Original SVG logo.
 *
 * Geometric abstract symbol combining:
 * - The letter A (peak shape)
 * - An open book / upward learning path (two diverging strokes)
 * - Subtle knowledge progression (ascending chevron layers)
 *
 * Brand colors: Deep Ink #101D2B, Soft Sage #C7E8DC, Sage Dark #315C50
 */
export function AQVERALogo({
  size = 32,
  variant = "light",
  className,
}: AQVERALogoProps) {
  const ink = variant === "dark" ? "#FFFFFF" : "#101D2B";
  const sage = variant === "dark" ? "#C7E8DC" : "#315C50";

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="AQVERA"
      role="img"
    >
      <defs>
        <linearGradient
          id="aqvera-gradient"
          x1="0"
          y1="0"
          x2="0"
          y2="1"
          gradientUnits="userSpaceOnUse"
        >
          <stop offset="0" stopColor={sage} />
          <stop offset="1" stopColor={ink} />
        </linearGradient>
      </defs>

      {/* Outer book frame — upward learning path */}
      <path
        d="M16 2 L4 14 L16 26 L28 14 L16 2 Z"
        fill={ink}
        stroke={sage}
        strokeWidth="1.5"
        strokeLinejoin="round"
      />

      {/* Inner ascending chevron — knowledge progression */}
      <path
        d="M8 12 L16 4 L24 12"
        fill="none"
        stroke={sage}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M10 16 L16 10 L22 16"
        fill="none"
        stroke={sage}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity={0.6}
      />

      {/* Center vertical stroke — the letter A spine */}
      <path
        d="M16 2 L16 26"
        fill="none"
        stroke={sage}
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

/**
 * Full horizontal logo with wordmark.
 */
export function AQVERAHorizontalLogo({
  size = 32,
  variant = "light",
  className,
}: AQVERALogoProps) {
  return (
    <div
      className={`flex items-center gap-3 ${className ?? ""}`}
      role="img"
      aria-label="AQVERA"
    >
      <AQVERALogo size={size} variant={variant} />
      <div className="flex flex-col leading-none">
        <span
          className={`text-sm font-bold tracking-tight ${
            variant === "dark" ? "text-white" : "text-[#101D2B]"
          }`}
        >
          AQVERA
        </span>
        <span
          className={`text-[10px] uppercase tracking-wider ${
            variant === "dark" ? "text-[#C7E8DC]" : "text-[#77828A]"
          }`}
        >
          Academic Learning
        </span>
      </div>
    </div>
  );
}
