export const metadata = {
  title: "AI Learning Platform",
  description: "Kids, English fluency, and Interview coaching — one platform.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0 }}>{children}</body>
    </html>
  );
}
