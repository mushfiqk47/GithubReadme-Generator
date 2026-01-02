"""
UI constants for consistent styling and WCAG compliance.
"""

# WCAG AA Compliant Color Palette
# Contrast ratios: 4.5:1 for normal text, 3:1 for large text
COLORS = {
    # Background colors (dark theme)
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#21262d",
    "bg_sidebar": "#010409",
    
    # Text colors
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "text_muted": "#6e7681",
    
    # Accent colors (verified for contrast)
    "accent_blue": "#58a6ff",
    "accent_purple": "#a371f7",
    "accent_green": "#238636",
    "accent_green_hover": "#2ea043",
    "accent_red": "#da3633",
    "accent_yellow": "#d29922",
    
    # Border colors
    "border_default": "#30363d",
    "border_focus": "#58a6ff",
    
    # Status colors
    "success": "#238636",
    "warning": "#d29922",
    "error": "#da3633",
    "info": "#58a6ff",
}

# Spacing scale (8px base unit)
SPACING = {
    "xs": "0.25rem",  # 4px
    "sm": "0.5rem",   # 8px
    "md": "1rem",     # 16px
    "lg": "1.5rem",   # 24px
    "xl": "2rem",     # 32px
    "2xl": "3rem",    # 48px
}

# Border radius
BORDER_RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px",
}

# Typography scale
FONT_SIZES = {
    "xs": "0.75rem",   # 12px
    "sm": "0.875rem",  # 14px
    "base": "1rem",    # 16px
    "lg": "1.125rem",  # 18px
    "xl": "1.25rem",   # 20px
    "2xl": "1.5rem",   # 24px
    "3xl": "2.25rem",  # 36px
    "4xl": "3rem",     # 48px
}

# Z-index scale
Z_INDEX = {
    "dropdown": 1000,
    "sticky": 1020,
    "fixed": 1030,
    "modal_backdrop": 1040,
    "modal": 1050,
    "popover": 1060,
    "tooltip": 1070,
}

# Breakpoints (responsive design)
BREAKPOINTS = {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
}

# Animation durations
ANIMATION = {
    "fast": "150ms",
    "base": "200ms",
    "slow": "300ms",
}

# Focus states for accessibility
FOCUS_STYLES = {
    "outline": "2px solid #58a6ff",
    "outline_offset": "2px",
    "box_shadow": "0 0 0 3px rgba(88, 166, 255, 0.3)",
}
