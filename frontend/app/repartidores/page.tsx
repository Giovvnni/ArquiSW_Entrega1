"use client";
import { useState } from "react";
import { api, Repartidor } from "../../lib/api";

const inp: React.CSSProperties = {
  display: "block", width: "100%", padding: "8px 10px",
  border: "1px solid #ddd", borderRadius: 6, fontSize: 14, boxSizing: "border-box",
};
const lbl: React.CSSProperties = { display: "block", marginBottom: 4, fontWeight: 600, fontSize: 13 };
const btn: React.CSSProperties = {
  padding: "9px 20px", background: "#059669", color: "white",
  border: "none", borderRadius: 6, cursor: "pointer", fontSize: 14, marginTop: 4,
};
const card: React.CSSProperties = {
  background: "white", borderRadius: 10, padding: 24,
  boxShadow: "0 1px 4px rgba(0,0,0,.08)", marginBottom: 24,
};

function Result({ data, error }: { data: unknown; error: string }) {
  if (error) return <p style={{ color: "#dc2626", marginTop: 8, fontSize: 13 }}>{error}</p>;
  if (!data) return null;
  return (
    <pre style={{
      marginTop: 12, background: "#f8f8f8", padding: 12, borderRadius: 6,
      fontSize: 12, overflow: "auto", border: "1px solid #eee",
    }}>
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}

export default function RepartidoresPage() {
  // --- Registrar ---
  const [regForm, setRegForm] = useState({ id: "", capacidad: "", ubicacion: "" });
  const [regRes, setRegRes] = useState<Repartidor | null>(null);
  const [regErr, setRegErr] = useState("");

  const handleRegistrar = async () => {
    setRegErr(""); setRegRes(null);
    try {
      const ubicacion = regForm.ubicacion ? { direccion: regForm.ubicacion } : undefined;
      setRegRes(await api.registrarRepartidor({
        id: regForm.id,
        capacidad: Number(regForm.capacidad),
        ubicacion,
      }));
    } catch (e) {
      setRegErr((e as Error).message);
    }
  };

  // --- Consultar ---
  const [consultarId, setConsultarId] = useState("");
  const [consultarRes, setConsultarRes] = useState<Repartidor | null>(null);
  const [consultarErr, setConsultarErr] = useState("");

  const handleConsultar = async () => {
    setConsultarErr(""); setConsultarRes(null);
    try {
      setConsultarRes(await api.obtenerRepartidor(consultarId));
    } catch (e) {
      setConsultarErr((e as Error).message);
    }
  };

  return (
    <div>
      <h1 style={{ margin: "0 0 24px" }}>Repartidores</h1>

      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Registrar repartidor</h2>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px 16px" }}>
          <div>
            <label style={lbl}>ID</label>
            <input style={inp} value={regForm.id} onChange={e => setRegForm({ ...regForm, id: e.target.value })} placeholder="ej: R1" />
          </div>
          <div>
            <label style={lbl}>Capacidad (pedidos)</label>
            <input style={inp} type="number" value={regForm.capacidad} onChange={e => setRegForm({ ...regForm, capacidad: e.target.value })} placeholder="ej: 10" />
          </div>
          <div>
            <label style={lbl}>Ubicación inicial (opcional)</label>
            <input style={inp} value={regForm.ubicacion} onChange={e => setRegForm({ ...regForm, ubicacion: e.target.value })} placeholder="ej: Centro de distribución" />
          </div>
        </div>
        <button style={btn} onClick={handleRegistrar}>Registrar</button>
        <Result data={regRes} error={regErr} />
      </div>

      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Consultar repartidor</h2>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end" }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID del repartidor</label>
            <input style={inp} value={consultarId} onChange={e => setConsultarId(e.target.value)} placeholder="ej: R1" />
          </div>
          <button style={btn} onClick={handleConsultar}>Consultar</button>
        </div>
        <Result data={consultarRes} error={consultarErr} />
      </div>
    </div>
  );
}
