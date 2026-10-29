'use client';

import React, { useState, useEffect } from 'react';
import { User } from '../types/user';
import { mockUsers, mockWrappedUsers } from '../lib/api/mocks/user_mock';
import { UserCard, UIState } from '../components/UserCard';
import { apiRequest, ApiError, isMockMode } from '../lib/api/client';

export default function HomePage() {
  const [users, setUsers] = useState<User[]>([]);
  const [state, setState] = useState<UIState>('loading');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [mockActive, setMockActive] = useState<boolean>(false);

  const loadData = async () => {
    setState('loading');
    setErrorMessage('');
    try {
      // Wave 1 Mock Interception: apiRequest tự động trả về mockData khi USE_MOCKS=true,
      // hoặc kết nối Live Backend API (/api/v1/users) khi ở Wave 2 live mode.
      const data = await apiRequest<User[]>('/api/v1/users', {
        mockData: mockWrappedUsers,
        unwrap: true,
      });

      // Chuẩn hóa dữ liệu linh hoạt (Direct Array hoặc Wrapped Response Envelope)
      let list: User[] = [];
      if (Array.isArray(data)) {
        list = data;
      } else if (data && typeof data === 'object') {
        const anyObj = data as Record<string, unknown>;
        if (Array.isArray(anyObj.items)) {
          list = anyObj.items as User[];
        } else if (Array.isArray(anyObj.data)) {
          list = anyObj.data as User[];
        }
      }

      setUsers(list);
      setMockActive(isMockMode());
      setState(list.length > 0 ? 'success' : 'empty');
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(`Lỗi Backend API (${err.status}): ${err.detail}`);
      } else {
        setErrorMessage(err instanceof Error ? err.message : 'Không thể kết nối tới Backend API.');
      }
      setState('error');
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <main className="max-w-4xl mx-auto py-12 px-4 sm:px-6">
      <header className="mb-10 text-center">
        <div className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold mb-3">
          Antigravity 2.0 Native Platform
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
          AI-Vibe-Coding Portal
        </h1>
        <p className="mt-2 text-base text-slate-600">
          Giao diện chuẩn hóa 5 trạng thái (Default, Loading, Empty, Error, Success) đồng bộ 100% hợp đồng dữ liệu.
        </p>
      </header>

      <section className="space-y-4">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-slate-800">Danh Sách Thành Viên</h2>
            <span
              className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                mockActive ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
              }`}
            >
              {mockActive ? 'Wave 1 Mock Mode' : 'Wave 2 Live Mode'}
            </span>
          </div>
          <button
            onClick={loadData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition"
          >
            Làm mới
          </button>
        </div>

        {state === 'loading' && <UserCard state="loading" />}
        {state === 'empty' && <UserCard state="empty" />}
        {state === 'error' && (
          <UserCard state="error" errorMessage={errorMessage} onRetry={loadData} />
        )}
        {state === 'success' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {users.map((u) => (
              <UserCard key={u.id} state="success" user={u} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
