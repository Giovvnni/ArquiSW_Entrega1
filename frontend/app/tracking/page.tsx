"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function TrackingSearch() {
  const [pedidoId, setPedidoId] = useState("");
  const router = useRouter();

  const handleBuscar = () => {
    if (pedidoId.trim()) router.push(`/tracking/${pedidoId.trim()}`);
  };

  return (
    <div>
      <h1 style={{ margin: "0 0 24px" }}>Tracking de pedidos</h1>
      <div style={{
        background: "white", borderRadius: 10, padding: 32,
        boxShadow: "0 1px 4px rgba(0,0,0,.08)", maxWidth: 420,
      }}>
        <label style={{ display: "block", marginBottom: 6, fontWeight: 600, fontSize: 14 }}>
          ID del pedido
        </label>
        <input
          style={{
            display: "block", width: "100%", padding: "10px 12px",
            border: "1px solid #ddd", borderRadius: 6, fontSize: 15,
            boxSizing: "border-box", marginBottom: 12,
          }}
          value={pedidoId}
          onChange={e => setPedidoId(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleBuscar()}
          placeholder="ej: P001"
          autoFocus
        />
        <button
          onClick={handleBuscar}
          style={{
            width: "100%", padding: "10px 0", background: "#dc2626", color: "white",
            border: "none", borderRadius: 6, fontSize: 15, cursor: "pointer",
          }}
        >
          Ver estado
        </button>
      </div>
    </div>
  );
}
