type Bucket = {
  count: number;
  resetAt: number;
};

const buckets = new Map<string, Bucket>();

const WINDOW_MS = 60_000;
const MAX_ATTEMPTS = 10;
// Cap the map so a flood of distinct keys cannot grow memory unbounded.
const MAX_BUCKETS = 10_000;

export function isRateLimited(key: string, max = MAX_ATTEMPTS, windowMs = WINDOW_MS) {
  const now = Date.now();
  const bucket = buckets.get(key);

  if (!bucket || bucket.resetAt <= now) {
    if (buckets.size >= MAX_BUCKETS) {
      // Sweep expired buckets before evicting anything.
      for (const [k, b] of buckets) {
        if (b.resetAt <= now) {
          buckets.delete(k);
        }
      }
    }
    buckets.set(key, { count: 1, resetAt: now + windowMs });
    return false;
  }

  bucket.count += 1;
  return bucket.count > max;
}

export function getClientIp(request: Request) {
  const forwarded = request.headers.get("x-forwarded-for");
  if (forwarded) {
    return forwarded.split(",")[0]?.trim() || "unknown";
  }
  return request.headers.get("x-real-ip") ?? "unknown";
}
