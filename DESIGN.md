---
name: Vocalicious
description: Voice-Assisted Food Ordering & Intelligent Recommendation System
colors:
  primary: "#f59e0b"
  primary-glow: "rgba(245, 158, 11, 0.4)"
  secondary: "#10b981"
  neutral-bg: "#020617"
  neutral-surface: "#0f172a"
  neutral-card: "#1e293b"
  neutral-border: "#334155"
  text-primary: "#f8fafc"
  text-muted: "#94a3b8"
typography:
  display:
    fontFamily: '"Plus Jakarta Sans", sans-serif'
    fontSize: "1.5rem"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  headline:
    fontFamily: '"Plus Jakarta Sans", sans-serif'
    fontSize: "1.125rem"
    fontWeight: 700
    lineHeight: 1.3
  title:
    fontFamily: '"Plus Jakarta Sans", sans-serif'
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: '"Plus Jakarta Sans", sans-serif'
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.4
  label:
    fontFamily: '"Plus Jakarta Sans", sans-serif'
    fontSize: "0.6875rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.02em"
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  2xl: "24px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#020617"
    rounded: "{rounded.xl}"
    padding: "12px 20px"
  button-primary-hover:
    backgroundColor: "#d97706"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-muted}"
    rounded: "{rounded.lg}"
    padding: "8px 12px"
  chip-category:
    backgroundColor: "{colors.neutral-surface}"
    textColor: "{colors.text-muted}"
    rounded: "{rounded.full}"
    padding: "6px 14px"
  card-dish:
    backgroundColor: "{colors.neutral-surface}"
    rounded: "{rounded.2xl}"
    padding: "12px"
---

# Design System: Vocalicious

## Overview

**Creative North Star: "The Precision Culinary Terminal"**

Vocalicious is crafted as a high-precision, zero-noise culinary terminal tailored for Vietnamese food culture. It abandons visual clutter, noisy promotional banners, and convoluted multi-page navigations in favor of purposeful dark ergonomics, instant auditory feedback, and fluid voice recognition. The interface treats food ordering as an exact, delightful ritual where natural language directly transforms into structured orders in milliseconds.

The aesthetic philosophy bridges the deep obsidian shadows of nighttime Vietnamese street food alleys with the crisp, tactical clarity of a modern avionics instrument panel. Surfaces are built with layered slate tones, accented by Culinary Gold for primary interactions and Fresh Herb Mint for availability and success states.

**Key Characteristics:**
- **Zero Noise & Immediate Clarity:** High signal-to-noise ratio; no pop-ups, no spam banners, and strict content prioritization.
- **Tonal Layering with Ambient Glow:** Elevation achieved through subtle luminance steps (`#020617` $\rightarrow$ `#0f172a` $\rightarrow$ `#1e293b`) paired with 1px border definition and warm ambient halos around the voice triggers.
- **Tactile Ergonomics:** Finger-friendly 48x48dp touch targets, rounded contours (2xl/full), and dynamic waveform responses tuned to voice amplitude.

## Colors

The palette balances intense dark slate neutrals with warm culinary radiance and organic herb accents.

### Primary
- **Culinary Gold** (`#f59e0b` / Amber-500): The core interactive accent. Used for the prominent voice microphone trigger, call-to-action buttons, active navigation states, and pricing highlights. It evokes the appetizing golden warmth of broth and crispy shallots.
- **Amber Glow** (`#fbbf24` / Amber-400): Secondary illumination for badges, hover states, and preparation time highlights.

### Secondary
- **Fresh Herb Mint** (`#10b981` / Emerald-500): Indicates kitchen progress milestones, vegetarian badges, store open status, and order completion confirmations.
- **Mint Tint** (`rgba(16, 185, 129, 0.15)`): Used for soft background containers behind positive tags and badges.

### Neutral
- **Obsidian Deep** (`#020617` / Slate-950): The canvas bedrock. Provides absolute contrast for typography and appetizing food photography.
- **Terminal Slate** (`#0f172a` / Slate-900): Surface level for chassis, modals, and container panels.
- **Card Slate** (`#1e293b` / Slate-800): Surface elevation for food cards, input fields, and inactive chips.
- **Border Slate** (`#334155` / Slate-700): 1px structural separators preventing visual bleed.
- **Text Primary** (`#f8fafc` / Slate-50): Maximum contrast for dish names, numbers, and primary headings.
- **Text Muted** (`#94a3b8` / Slate-400): Subtitles, units, and secondary metadata.

### Named Rules
**The Zero Noise Rule.** Never introduce flashing marketing banners, intrusive discount pop-ups, or unprompted modals. The primary accent is reserved strictly for user intent, voice feedback, and transactional certainty.

## Typography

**Display Font:** Plus Jakarta Sans (with system-ui, -apple-system, sans-serif fallback)  
**Body Font:** Plus Jakarta Sans  
**Character:** A geometric yet warm humanist sans-serif offering razor-sharp legibility at micro sizes on small mobile viewports, paired with bold, authoritative display weights for prices and order progress.

### Hierarchy
- **Display** (800 font-extrabold, 1.25rem - 1.5rem, line-height 1.2): Restaurant identity, ETD countdown timer, and modal primary headings.
- **Headline** (700 font-bold, 1rem - 1.125rem, line-height 1.3): Dish card titles, section headers, and cart summary total.
- **Title** (700 font-bold, 0.8125rem - 0.875rem, line-height 1.3): Price figures, button labels, and status badges.
- **Body** (500 font-medium, 0.75rem, line-height 1.4): Flavor descriptions, location details, and order notes.
- **Label** (600 font-semibold, 0.6875rem, letter-spacing 0.02em): Micro-tags (prep time, category chips, timestamps).

### Named Rules
**The Currency Emphasis Rule.** Prices are always set in bold or extrabold with the localized Vietnamese `đ` or `VNĐ` symbol clearly visible, ensuring immediate transactional comprehension.

## Layout

The spatial model uses an ergonomically constrained, mobile-first chassis:
- **Chassis Bounds:** Max-width 420px on desktop screens with 860px height to simulate a premium smartphone shell; 100vw/100vh edge-to-edge on real mobile hardware.
- **Spatial Grid:** 4px baseline rhythm (`4px`, `8px`, `12px`, `16px`, `24px`).
- **Fixed Infrastructure:** Persistent Top Status & Dynamic Island Bar (height ~48px) and Bottom Floating Navigation Dock (height ~68px) with floating central microphone action button.
- **Scroll Behavior:** Smooth internal vertical container scrolling with custom slim 4px amber-accented scrollbars.

## Elevation & Depth

Vocalicious conveys hierarchy through layered tonal contrast rather than arbitrary blurry drop shadows.

### Shadow Vocabulary
- **Voice Halo Glow** (`box-shadow: 0 0 30px rgba(245, 158, 11, 0.5)`): Ambient radiating glow on the voice microphone FAB during idle and active listening.
- **Chassis Elevation** (`box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7)`): Outer shadow anchoring the mobile frame on desktop viewports.
- **Dock Glassmorphism** (`backdrop-filter: blur(12px); background: rgba(2, 6, 23, 0.85)`): Floats over menu content with a 1px border separator (`border-slate-800/80`).

### Named Rules
**The State-Driven Elevation Rule.** Surfaces rest flat with 1px border contrast. Elevation and glowing halos only activate in direct response to user state, particularly active microphone listening and cart badge updates.

## Shapes

- **Contour Strategy:** Soft, friendly industrial radii (`rounded-2xl` 16px for cards, `rounded-3xl` 24px for modals, `rounded-full` for chips and FABs).
- **Border Precision:** 1px hairline borders (`border border-slate-800`) are mandatory on all dark containers to maintain separation against the Obsidian Deep canvas.
- **Touch Bounds:** Touch targets adhere to a strict minimum 48×48dp footprint.

## Components

### Buttons
- **Shape:** `rounded-2xl` (16px) or `rounded-full` (9999px).
- **Primary:** Background `bg-amber-500`, text `text-slate-950`, font-extrabold. On hover: `bg-amber-400`. On active: `scale-95`.
- **Secondary / Action Ghost:** `bg-slate-800/80` with border `border-slate-700/60`, text `text-slate-300`.

### Voice Microphone FAB (Signature Component)
- **Shape:** Perfect circle 56×56px (`w-14 h-14 rounded-full`).
- **Styling:** Floating in the center of the bottom dock with pulsating amber aura (`animate-voice-glow`), gradient background `bg-gradient-to-tr from-amber-600 to-amber-400`, icon `text-slate-950 text-xl`.
- **Waveform Modal:** Fullscreen overlay with 16 dynamic equalizer bars animated by Web Audio / speech amplitude.

### Dish Card
- **Shape:** `rounded-2xl` (16px), background `bg-slate-900`, 1px border `border-slate-800`.
- **Media:** 80×80px rounded square thumbnail on the left with optimized aspect-square crop.
- **Metadata:** Dish name (white font-bold), price (amber-400 font-extrabold), prep time tag (`~8 phút`), vegetarian badge (`Ăn chay`).
- **Quick Action:** Rapid "+" button on bottom right with haptic transition.

### Navigation Dock
- **Shape:** Floating bottom capsule bar (`rounded-3xl` or edge-to-edge), background `bg-slate-950/80` with `backdrop-blur-md`.
- **Items:** 3 primary tabs ("Thực đơn", "Giỏ hàng" with badge counter, "Theo dõi bếp") flanking the central microphone FAB.

## Do's and Don'ts

### Do:
- **Do** maintain a strict 48x48dp minimum touch target for all clickable buttons, chips, and icons.
- **Do** preserve the 1px hairline border (`border-slate-800`) on dark card surfaces to ensure structural legibility.
- **Do** use Culinary Gold (`#f59e0b`) exclusively for user-initiated primary actions and voice cues.
- **Do** show transparent preparation time badges on dishes and precise ETD countdowns during order waiting.

### Don't:
- **Don't** add unrequested commercial pop-ups, flashing discount tickers, or visual noise that interrupts ordering.
- **Don't** use generic non-Vietnamese food photos; all dishes must accurately depict authentic local cuisine.
- **Don't** drop below 4.5:1 text contrast ratio on dark backgrounds.
- **Don't** hijack or alter the physical Back button or system gesture behavior.

