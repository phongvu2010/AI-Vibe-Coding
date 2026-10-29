/**
 * Typed HTTP Client for communicating with the FastAPI Backend from Vite SPA (`src/lib/api/client.ts`).
 */

function getEnvVar(key: "API_URL" | "USE_MOCKS"): string | undefined {
  try {
    // @ts-expect-error import.meta.env in Vite
    if (typeof import.meta !== "undefined" && import.meta.env) {
      // @ts-expect-error Vite env lookup
      const val = import.meta.env[`VITE_${key}`];
      if (typeof val === "string") return val;
    }
  } catch {
    // import.meta not available
  }
  return undefined;
}

export function getApiBaseUrl(): string {
  const resolved = getEnvVar("API_URL");
  if (resolved) return resolved;
  return "http://localhost:8000";
}

export function isMockMode(): boolean {
  return getEnvVar("USE_MOCKS") === "true";
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
  ) {
    super(detail);
    this.name = "ApiError";
  }
}

/**
 * Standard HTTP Data Envelope Wrapper for Single / Array payloads.
 */
export interface ApiResponseWrapper<T> {
  data: T;
  message?: string;
  status?: string | number;
  success?: boolean;
}

/**
 * Standard HTTP Paginated Collection Wrapper.
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip?: number;
  limit?: number;
}

/**
 * Normalizes response payloads that may be wrapped in an envelope.
 */
export function normalizeApiResponse<T>(payload: unknown): T {
  if (payload && typeof payload === "object") {
    const obj = payload as Record<string, unknown>;
    if ("data" in obj && obj.data !== undefined) {
      return obj.data as T;
    }
    if ("items" in obj && Array.isArray(obj.items)) {
      return obj.items as T;
    }
  }
  return payload as T;
}

export interface ApiRequestOptions extends RequestInit {
  mockData?: unknown;
  /** Automatically unwrap { data: ... } or { items: ... } response envelope if present */
  unwrap?: boolean;
  invalidateCache?: boolean;
}

export async function clearClientApiCache(): Promise<void> {
  if (typeof window !== "undefined") {
    try {
      const clearStorage = (storage?: Storage) => {
        if (!storage) return;
        const keysToRemove: string[] = [];
        for (let i = 0; i < storage.length; i++) {
          const key = storage.key(i);
          if (key && (key.startsWith("api_") || key.startsWith("cache_") || key.startsWith("mock_"))) {
            keysToRemove.push(key);
          }
        }
        keysToRemove.forEach((k) => storage.removeItem(k));
      };

      if (typeof sessionStorage !== "undefined") clearStorage(sessionStorage);
      if (typeof localStorage !== "undefined") clearStorage(localStorage);
    } catch {
      // Ignore storage errors in restricted contexts
    }
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options?: ApiRequestOptions,
): Promise<T> {
  if (isMockMode() && options?.mockData !== undefined) {
    const rawMock = options.mockData;
    return options?.unwrap ? normalizeApiResponse<T>(rawMock) : (rawMock as T);
  }

  const { mockData: _, unwrap, invalidateCache, ...fetchOptions } = options ?? {};

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((fetchOptions.headers as Record<string, string>) ?? {}),
  };

  if (invalidateCache || !isMockMode()) {
    headers["Cache-Control"] = "no-cache, no-store, must-revalidate";
  }

  let targetUrl = `${getApiBaseUrl()}${endpoint}`;
  if (invalidateCache) {
    const separator = targetUrl.includes("?") ? "&" : "?";
    targetUrl = `${targetUrl}${separator}_t=${Date.now()}`;
  }

  const response = await fetch(targetUrl, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    let detail = `HTTP Error ${response.status}`;
    try {
      const errBody = (await response.json()) as { detail?: string | Array<{ loc?: string[]; msg?: string }> };
      if (typeof errBody.detail === "string") {
        detail = errBody.detail;
      } else if (Array.isArray(errBody.detail)) {
        detail = errBody.detail.map((err) => err.msg || JSON.stringify(err)).join(", ");
      }
    } catch {
      // Non-JSON response
    }
    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const jsonResult = (await response.json()) as unknown;
  return unwrap ? normalizeApiResponse<T>(jsonResult) : (jsonResult as T);
}
