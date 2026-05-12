import Link from "next/link";

const cards = [
  {
    href: "/pedidos",
    title: "Pedidos",
    desc: "Crear, validar y asignar pedidos de entrega desde distintos canales.",
    color: "#4f46e5",
  },
  {
    href: "/repartidores",
    title: "Repartidores",
    desc: "Registrar repartidores y consultar su disponibilidad.",
    color: "#059669",
  },
  {
    href: "/rutas",
    title: "Rutas",
    desc: "Definir rutas con waypoints, asignar a repartidores y avanzar entregas.",
    color: "#d97706",
  },
  {
    href: "/tracking",
    title: "Tracking",
    desc: "Consultar el estado de un pedido y ver notificaciones en tiempo real.",
    color: "#dc2626",
  },
];

export default function Dashboard() {
  return (
    <div>
      <h1 style={{ margin: "0 0 4px", fontSize: 28 }}>Gestión Logística de Última Milla</h1>
      <p style={{ color: "#666", margin: "0 0 32px", fontSize: 14 }}>
        Entregable 2 — Arquitectura en Capas + Cliente-Servidor
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16 }}>
        {cards.map((c) => (
          <Link key={c.href} href={c.href} style={{ textDecoration: "none" }}>
            <div style={{
              background: "white", borderRadius: 10, padding: "24px 20px",
              boxShadow: "0 1px 4px rgba(0,0,0,.08)",
              borderTop: `4px solid ${c.color}`,
            }}>
              <h2 style={{ margin: "0 0 8px", fontSize: 18, color: c.color }}>{c.title}</h2>
              <p style={{ margin: 0, color: "#555", fontSize: 13, lineHeight: 1.5 }}>{c.desc}</p>
            </div>
          </Link>
        ))}
      </div>
      <div style={{ marginTop: 40, padding: 20, background: "white", borderRadius: 10, boxShadow: "0 1px 4px rgba(0,0,0,.08)" }}>
        <h3 style={{ margin: "0 0 8px" }}>Flujo de demo</h3>
        <ol style={{ margin: 0, paddingLeft: 20, color: "#555", fontSize: 13, lineHeight: 2 }}>
          <li>Registrar un repartidor en <strong>Repartidores</strong></li>
          <li>Crear un pedido en <strong>Pedidos</strong> y validarlo</li>
          <li>Asignar el pedido al repartidor</li>
          <li>Crear una ruta en <strong>Rutas</strong> con el repartidor_id y avanzar waypoints</li>
          <li>Ver el estado y notificaciones en <strong>Tracking</strong></li>
        </ol>
      </div>
    </div>
  );
}
