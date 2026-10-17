import React from 'react';

export const metadata = {
  title: 'AI-Vibe-Coding Platform',
  description: 'Enterprise Multi-Agent Software Development Platform on Antigravity 2.0',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="bg-slate-50 text-slate-900 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
