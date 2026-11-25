"use client";

import { useState, useEffect, useCallback, createContext, useContext, ReactNode } from "react";

interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  email_verified: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
  updateProfile: (data: { full_name?: string; language?: string }) => Promise<void>;
  getPreferences: () => Promise<{ language: string; theme: string; email_notifications: boolean; study_reminders: boolean } | null>;
  updatePreferences: (data: { language?: string; theme?: string; email_notifications?: boolean; study_reminders?: boolean }) => Promise<void>;
  getOnboarding: () => Promise<{ welcome_seen: boolean; language_selected: boolean; interests_selected: boolean; first_course_created: boolean; first_material_uploaded: boolean; tutor_introduced: boolean; completed: boolean } | null>;
  completeOnboardingStep: (step: string) => Promise<void>;
  apiFetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>;
}

const AuthContext = createContext<AuthContextType | null>(null);

const TOKEN_KEY = "aqvera_access_token";
const REFRESH_TOKEN_KEY = "aqvera_refresh_token";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

function setTokens(accessToken: string, refreshToken: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

function clearTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function initAuth() {
      const currentToken = getToken();
      if (!currentToken) {
        if (!cancelled) setIsLoading(false);
        return;
      }
      if (!cancelled) setToken(currentToken);
      try {
        const res = await fetch("/api/auth/profile", {
          headers: { Authorization: `Bearer ${currentToken}` },
        });
        if (res.ok) {
          const data = await res.json();
          if (!cancelled) setUser(data);
        } else {
          clearTokens();
          if (!cancelled) {
            setToken(null);
            setUser(null);
          }
        }
      } catch {
        if (!cancelled) setUser(null);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    void initAuth();
    return () => {
      cancelled = true;
    };
  }, []);

  const apiFetch = useCallback(
    async (input: RequestInfo | URL, init: RequestInit = {}) => {
      const headers: Record<string, string> = {};
      if (init.headers) {
        if (init.headers instanceof Headers) {
          init.headers.forEach((val, key) => {
            headers[key] = val;
          });
        } else if (Array.isArray(init.headers)) {
          init.headers.forEach(([k, v]) => {
            headers[k] = v;
          });
        } else {
          Object.assign(headers, init.headers);
        }
      }
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
      const res = await fetch(input, { ...init, headers });
      if (res.status === 401) {
        // Try refresh
        const refreshToken = getRefreshToken();
        if (refreshToken) {
          try {
            const refreshRes = await fetch("/api/auth/refresh", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ refresh_token: refreshToken }),
            });
            if (refreshRes.ok) {
              const data = await refreshRes.json();
              setTokens(data.access_token, data.refresh_token);
              setToken(data.access_token);
              headers["Authorization"] = `Bearer ${data.access_token}`;
              return fetch(input, { ...init, headers });
            }
          } catch {
            // refresh failed
          }
        }
        clearTokens();
        setToken(null);
        setUser(null);
      }
      return res;
    },
    [token]
  );

  const fetchUserProfile = useCallback(async () => {
    const currentToken = getToken();
    if (!currentToken) return;
    const res = await fetch("/api/auth/profile", {
      headers: { Authorization: `Bearer ${currentToken}` },
    });
    if (res.ok) {
      const data = await res.json();
      setUser(data);
    } else {
      clearTokens();
      setToken(null);
      setUser(null);
    }
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Login failed" }));
        throw new Error(err.detail || "Login failed");
      }
      const data = await res.json();
      setTokens(data.access_token, data.refresh_token);
      setToken(data.access_token);
      await fetchUserProfile();
    },
    [fetchUserProfile]
  );

  const register = useCallback(
    async (email: string, password: string, fullName?: string) => {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Registration failed" }));
        throw new Error(err.detail || "Registration failed");
      }
      await login(email, password);
    },
    [login]
  );

  const logout = useCallback(async () => {
    const refreshToken = getRefreshToken();
    if (refreshToken && token) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      } catch {
        // ignore logout errors
      }
    }
    clearTokens();
    setToken(null);
    setUser(null);
    setIsLoading(false);
  }, [token]);

  const updateProfile = useCallback(
    async (data: { full_name?: string; language?: string }) => {
      const res = await apiFetch("/api/auth/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Profile update failed" }));
        throw new Error(err.detail || "Profile update failed");
      }
      const updated = await res.json();
      setUser(updated);
    },
    [apiFetch]
  );

  const getPreferences = useCallback(async () => {
    const res = await apiFetch("/api/auth/preferences");
    if (!res.ok) return null;
    return res.json();
  }, [apiFetch]);

  const updatePreferences = useCallback(
    async (data: { language?: string; theme?: string; email_notifications?: boolean; study_reminders?: boolean }) => {
      const res = await apiFetch("/api/auth/preferences", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Preferences update failed" }));
        throw new Error(err.detail || "Preferences update failed");
      }
    },
    [apiFetch]
  );

  const getOnboarding = useCallback(async () => {
    const res = await apiFetch("/api/auth/onboarding");
    if (!res.ok) return null;
    return res.json();
  }, [apiFetch]);

  const completeOnboardingStep = useCallback(async (step: string) => {
    const res = await apiFetch(`/api/auth/onboarding/${step}`, {
      method: "POST",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to complete step" }));
      throw new Error(err.detail || "Failed to complete step");
    }
  }, [apiFetch]);

  const ctx: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated: !!token && !!user,
    login,
    register,
    logout,
    refresh: fetchUserProfile,
    updateProfile,
    getPreferences,
    updatePreferences,
    getOnboarding,
    completeOnboardingStep,
    apiFetch,
  };

  return (
    <AuthContext.Provider value={ctx}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
