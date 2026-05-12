"use client";
import { useState, useEffect } from "react";
import { api, Pedido, Notificacion } from "../../../lib/api";

const ESTADO_COLOR: Record<string, string> = {
  Creado: "#6b7280",
  Validado: "#2563eb",
  "Pendiente de asignación": "#d97706",
  Asignado: "#7c3aed",
  "En ruta": "#ea580c",
  Entregado: "#16a34a",
  Cancelado: "#dc2626",
  "Intento fallido": "#b91c1c",
  Reprogramado: "#0891b2",
};

export default function TrackingPage({ params }: { params: { id: string } }) {
  const pedidoId = params.id;
  const [pedido, setPedido] = useState<Pedido | null>(null);
  const [notifs, setNotifs] = useState<Notificacion[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const cargar = async () => {
    setError("");
    try {
      const [p, n] = await Promise.all([
        api.obtenerEstado(pedidoId),
        api.obtenerNotificaciones(pedidoId),
      ]);
      setPedido(p);
      setNotifs(n);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { cargar(); }, [pedidoId]);

  const estadoColor = pedido ? (ESTADO_COLOR[pedido.estado] ?? "#374151") : "#374151";

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>Tracking — pedido {pedidoId}</h1>
        <button
          onClick={cargar}
          style={{
            padding: "6px 14px", background: "#f3f4f6", border: "1px solid #ddd",
            borderRadius: 6, cursor: "pointer", fontSize: 13,
          }}
        >
          Actualizar
        </button>
      </div>

      {loading && <p style={{ color: "#888" }}>Cargando…</p>}
      {error && (
        <div style={{
          background: "white", borderRadius: 10, padding: 24,
          boxShadow: "0 1px 4px rgba(0,0,0,.08)", color: "#dc2626",
        }}>
          {error}
          <br />
          <a href="/tracking" style={{ fontSize: 13, color: "#4f46e5" }}>← Volver a buscar</a>
        </div>
      )}

      {pedido && (
        <>
          <div style={{
            background: "white", borderRadius: 10, padding: 24,
            boxShadow: "0 1px 4px rgba(0,0,0,.08)", marginBottom: 20,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
              <span style={{
                display: "inline-block", padding: "4px 14px", borderRadius: 20,
                background: estadoColor, color: "white", fontWeight: 700, fontSize: 14,
              }}>
                {pedido.estado}
              </span>
              <span style={{ color: "#6b7280", fontSize: 13 }}>
                {pedido.tipo_entrega} · {pedido.canal_origen}
              </span>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div>
                <p style={{ margin: "0 0 4px", fontSize: 12, color: "#9ca3af", textTransform: "uppercase" }}>Origen</p>
                <p style={{ margin: 0, fontSize: 14 }}>
                  {(pedido.origen as Record<string, string>).direccion}
                </p>
              </div>
              <div>
                <p style={{ margin: "0 0 4px", fontSize: 12, color: "#9ca3af", textTransform: "uppercase" }}>Destino</p>
                <p style={{ margin: 0, fontSize: 14 }}>
                  {(pedido.destino as Record<string, string>).direccion}
                </p>
                <p style={{ margin: "2px 0 0", fontSize: 13, color: "#6b7280" }}>
                  {(pedido.destino as Record<string, string>).nombre_destinatario}
                </p>
              </div>
              <div>
                <p style={{ margin: "0 0 4px", fontSize: 12, color: "#9ca3af", textTransform: "uppercase" }}>Repartidor asignado</p>
                <p style={{ margin: 0, fontSize: 14 }}>{pedido.repartidor_asignado ?? "—"}</p>
              </div>
            </div>
          </div>

          <div style={{
            background: "white", borderRadius: 10, padding: 24,
            boxShadow: "0 1px 4px rgba(0,0,0,.08)",
          }}>
            <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>
              Notificaciones ({notifs.length})
            </h2>
            {notifs.length === 0 ? (
              <p style={{ color: "#9ca3af", fontSize: 13, margin: 0 }}>Sin notificaciones aún.</p>
            ) : (
              <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
                {notifs.map((n, i) => (
                  <li key={i} style={{
                    padding: "10px 12px", borderLeft: "3px solid #4f46e5",
                    background: "#f8f8ff", marginBottom: 8, borderRadius: "0 6px 6px 0",
                    fontSize: 13,
                  }}>
                    {n.message}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </>
      )}
    </div>
  );
}
