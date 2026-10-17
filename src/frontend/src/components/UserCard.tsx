import React from 'react';
import { User } from '../types/user';

export type UIState = 'default' | 'loading' | 'empty' | 'error' | 'success';

interface UserCardProps {
  state: UIState;
  user?: User | null;
  errorMessage?: string;
  onRetry?: () => void;
}

export const UserCard: React.FC<UserCardProps> = ({
  state,
  user,
  errorMessage = "Đã xảy ra lỗi khi tải dữ liệu người dùng.",
  onRetry,
}) => {
  // 1. Loading State: Skeleton Shimmer
  if (state === 'loading') {
    return (
      <div className="p-4 border rounded-xl shadow-sm animate-pulse bg-slate-50 space-y-3">
        <div className="h-5 bg-slate-200 rounded w-1/3"></div>
        <div className="h-4 bg-slate-200 rounded w-2/3"></div>
        <div className="h-3 bg-slate-200 rounded w-1/4"></div>
      </div>
    );
  }

  // 2. Empty State
  if (state === 'empty') {
    return (
      <div className="p-8 border border-dashed rounded-xl text-center bg-slate-50">
        <p className="text-slate-500 font-medium">Chưa có thông tin người dùng.</p>
      </div>
    );
  }

  // 3. Error State
  if (state === 'error') {
    return (
      <div className="p-4 border border-red-200 bg-red-50 rounded-xl space-y-3 text-red-700">
        <p className="font-semibold text-sm">❌ Thao tác thất bại</p>
        <p className="text-xs">{errorMessage}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-3 py-1.5 bg-red-600 text-white rounded-lg text-xs font-medium hover:bg-red-700 transition"
          >
            Thử lại
          </button>
        )}
      </div>
    );
  }

  // 4. Default / Success State
  if (!user) {
    return null;
  }

  return (
    <div className="p-5 border border-slate-200 bg-white rounded-xl shadow-sm hover:shadow transition">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-bold text-slate-800 text-base">{user.full_name}</h3>
        <span
          className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
            user.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'
          }`}
        >
          {user.is_active ? 'Đang hoạt động' : 'Tạm khóa'}
        </span>
      </div>
      <p className="text-slate-600 text-sm mb-3">{user.email}</p>
      <div className="text-xs text-slate-400">
        Tham gia: {new Date(user.created_at).toLocaleDateString('vi-VN')}
      </div>
    </div>
  );
};
