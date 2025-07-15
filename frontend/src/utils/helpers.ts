/**
 * Generate a unique ID (simplified version)
 */
export function nanoid(): string {
  return Math.random().toString(36).substring(2, 15);
}

/**
 * Delay execution for the specified time
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}