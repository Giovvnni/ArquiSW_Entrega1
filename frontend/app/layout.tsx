import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Logística",
  description: "Sistema de gestión logística — Entregable 2",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0, background: "#f0f2f5" }}>
        <nav style={{
          background: "#1a1a2e", padding: "0 24px", color: "white",
          display: "flex", alignItems: "center", gap: 32, height: 52,
        }}>
          <a href="/" style={{ color: "white", textDecoration: "none", fontWeight: 700, fontSize: 16 }}>
            Logística
          </a>
          <a href="/pedidos" style={{ color: "#bbb", textDecoration: "none", fontSize: 14 }}>Pedidos</a>
          <a href="/repartidores" style={{ color: "#bbb", textDecoration: "none", fontSize: 14 }}>Repartidores</a>
          <a href="/rutas" style={{ color: "#bbb", textDecoration: "none", fontSize: 14 }}>Rutas</a>
          <a href="/tracking" style={{ color: "#bbb", textDecoration: "none", fontSize: 14 }}>Tracking</a>
        </nav>
        <main style={{ maxWidth: 900, margin: "0 auto", padding: "32px 16px" }}>
          {children}
        </main>
      </body>
    </html>
  );
}
