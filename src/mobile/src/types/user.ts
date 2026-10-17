/**
 * TypeScript Interface: User (Mobile React Native)
 * Khớp 100% với Web Interface và Backend Schema (snake_case).
 */
export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreatePayload {
  email: string;
  full_name: string;
  is_active?: boolean;
}
