import type { Metadata } from 'next';
import './globals.css';
import './themes.css';
export const metadata: Metadata = {
  title: 'FinGrowth — Growth workspace',
  description: 'A local workspace connecting growth architecture, funnel evidence, economics and experiments.',
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
