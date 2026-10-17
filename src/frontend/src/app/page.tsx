'use client';

import React, { useState, useEffect } from 'react';
import { User } from '../types/user';
import { mockUsers } from '../lib/api/mocks/user_mock';
import { UserCard, UIState } from '../components/UserCard';

export default function HomePage() {
  const [users, setUsers] = useState<User[]>([]);
  const [state, setState] = useState<UIState>('loading');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const loadData = async () => {
    setState('loading');
    try {
      // Giả lập nạp dữ liệu (Ưu tiên Mock ở Wave 1, chuyển Live API ở Wave 2)
      setTimeout(() => {
        setUsers(mockUsers);
        setState(mockUsers.length > 0 ? 'success' : 'empty');
      }, 600);
    } catch {
      setErrorMessage('Không thể kết nối tới Backend API.');
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
          <h2 className="text-xl font-bold text-slate-800">Danh Sách Thành Viên (Wave 1 Mock)</h2>
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
