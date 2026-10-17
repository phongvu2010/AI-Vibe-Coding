/**
 * TypeScript Interface: User
 * Tuân thủ 100% chuẩn snake_case đồng bộ với SQLAlchemy Model và Pydantic Schema.
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
