import { User } from '../../../types/user';

export const mockUsers: User[] = [
  {
    id: "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    email: "alex.techlead@vibe.dev",
    full_name: "Alex Tech Lead",
    is_active: true,
    created_at: "2026-10-17T08:00:00Z",
    updated_at: "2026-10-17T08:00:00Z",
  },
  {
    id: "f8e7d6c5-b4a3-2109-8765-43210fedcba9",
    email: "sarah.qa@vibe.dev",
    full_name: "Sarah QA Lead",
    is_active: true,
    created_at: "2026-10-17T09:30:00Z",
    updated_at: "2026-10-17T09:30:00Z",
  },
];
