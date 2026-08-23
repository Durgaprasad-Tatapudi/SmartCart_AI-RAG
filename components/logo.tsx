import React from 'react'

interface LogoProps {
  size?: 'sm' | 'md' | 'lg'
  iconOnly?: boolean
  className?: string
}

export function SmartCartIcon({ className = 'w-7 h-7' }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="logoBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0b382f" />
          <stop offset="50%" stopColor="#145d4f" />
          <stop offset="100%" stopColor="#1b7d6a" />
        </linearGradient>
        <linearGradient id="logoSparkleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6ee7b7" />
          <stop offset="50%" stopColor="#34d399" />
          <stop offset="100%" stopColor="#059669" />
        </linearGradient>
        <linearGradient id="logoGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#fef08a" />
          <stop offset="100%" stopColor="#fbbf24" />
        </linearGradient>
      </defs>

      {/* Rounded container */}
      <rect width="48" height="48" rx="12" fill="url(#logoBgGrad)" />
      <rect
        x="1"
        y="1"
        width="46"
        height="46"
        rx="11"
        fill="none"
        stroke="rgba(255,255,255,0.15)"
        strokeWidth="1"
      />

      {/* Cart Outline */}
      <g transform="translate(1, 0.5)">
        <path
          d="M10 14h4.2l3.8 15.5c.3 1.4 1.5 2.5 3 2.5h14c1.4 0 2.6-1 2.9-2.4L40 18.5c.2-.9-.5-1.5-1.4-1.5H16.8"
          stroke="#ffffff"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Wheels */}
        <circle cx="21" cy="37.5" r="2.3" fill="#ffffff" />
        <circle cx="33" cy="37.5" r="2.3" fill="#ffffff" />

        {/* Floating AI Star */}
        <path
          d="M28 10c0 5.5-4.5 8-4.5 8s4.5 2.5 4.5 8c0-5.5 4.5-8 4.5-8s-4.5-2.5-4.5-8z"
          fill="url(#logoSparkleGrad)"
        />

        {/* Sparkle core dot */}
        <circle cx="28" cy="18" r="0.7" fill="#ffffff" />

        {/* Mini Gold accent sparkle */}
        <path
          d="M36 9.5c0 2-1.7 3-1.7 3s1.7 1 1.7 3c0-2 1.7-3 1.7-3s-1.7-1-1.7-3z"
          fill="url(#logoGoldGrad)"
        />
      </g>
    </svg>
  )
}

export function Logo({ size = 'md', iconOnly = false, className = '' }: LogoProps) {
  const iconSizes = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-10 h-10',
  }

  const textSizes = {
    sm: 'text-base',
    md: 'text-lg',
    lg: 'text-2xl',
  }

  return (
    <div className={`inline-flex items-center gap-2.5 font-bold tracking-tight select-none ${className}`}>
      <SmartCartIcon className={iconSizes[size]} />
      {!iconOnly && (
        <span className={`inline-flex items-center gap-1.5 leading-none ${textSizes[size]}`}>
          <span className="text-foreground tracking-[-0.03em]">
            SmartCart
          </span>
          <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-extrabold tracking-wider bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 uppercase">
            AI
          </span>
        </span>
      )}
    </div>
  )
}
