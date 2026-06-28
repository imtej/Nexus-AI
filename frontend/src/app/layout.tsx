import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nexus AI — The Evolving Intelligence",
  description:
    "Nexus AI is an evolving AI companion powered by the Collective Knowledge Protocol. It learns, grows, and becomes wiser with every conversation.",
  keywords: ["AI", "companion", "collective knowledge", "evolving AI", "Nexus AI"],
  openGraph: {
    title: "Nexus AI — The Evolving Intelligence",
    description: "Meet Nexus AI — an AI that evolves through conversation.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
