/**
 * Nexus AI — Utility Functions
 */

/**
 * Format a relative time string (e.g., "2 hours ago", "just now").
 */
export function timeAgo(dateString: string): string {
  const now = new Date();
  const date = new Date(dateString);
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return "just now";
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
  return date.toLocaleDateString();
}

/**
 * Truncate a string to a max length with ellipsis.
 */
export function truncate(str: string, maxLength: number = 50): string {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength) + "...";
}

/**
 * Capitalize the first letter of a string.
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Generate a random greeting for the empty chat state.
 */
export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  if (hour < 21) return "Good evening";
  return "Hey there";
}

/**
 * Class name helper — join class names, filtering out falsy values.
 */
export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(" ");
}

/**
 * Get the evolution stage color.
 */
export function getStageColor(stage: string): string {
  const colors: Record<string, string> = {
    nascent: "#6c63ff",
    growing: "#a29bfe",
    mature: "#f0b429",
    transcendent: "#ff6b6b",
  };
  return colors[stage] || colors.nascent;
}

/**
 * Get the evolution stage label.
 */
export function getStageLabel(stage: string): string {
  const labels: Record<string, string> = {
    nascent: "🌱 Nascent",
    growing: "🌿 Growing",
    mature: "🌳 Mature",
    transcendent: "✨ Transcendent",
  };
  return labels[stage] || labels.nascent;
}
