"use client";
import { useState } from "react";
import { api, Ruta } from "../../lib/api";

const inp: React.CSSProperties = {
  display: "block", width: "100%", padding: "8px 10px",
  border: "1px solid #ddd", borderRadius: 6, fontSize: 14, boxSizing: "border-box",
};
const lbl: React.CSSProperties = { display: "block", marginBottom: 4, fontWeight: 600, fontSize: 13 };
const btn: React.CSSProperties = {
  padding: "9px 20px", background: "#d97706", color: "white",
  border: "none", borderRadius: 6, cursor: "pointer", fontSize: 14, marginTop: 4,
};
const card: React.CSSProperties = {
  background: "white", borderRadius: 10, padding: 24,
  boxShadow: "0 1px 4px rgba(0,0,0,.08)", marginBottom: 24,
};

const WAYPOINTS_PLACEHOLDER = JSON.stringify(
  [{ address: "Av. Principal 100" }, { address: "Calle Los Pinos 42" }],
  null,
  2
);

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

export default function RutasPage() {
  // --- Definir ruta ---
  const [defForm, setDefForm] = useState({ id: "", repartidor_id: "", waypoints: WAYPOINTS_PLACEHOLDER });
  const [defRes, setDefRes] = useState<Ruta | null>(null);
  const [defErr, setDefErr] = useState("");

  const handleDefinir = async () => {
    setDefErr(""); setDefRes(null);
    let waypoints: unknown[];
    try {
      waypoints = JSON.parse(defForm.waypoints);
    } catch {
      setDefErr("Waypoints inválidos: debe ser un array JSON válido");
      return;
    }
    try {
      setDefRes(await api.definirRuta({
        id: defForm.id,
        repartidor_id: defForm.repartidor_id || undefined,
        waypoints,
      }));
    } catch (e) {
      setDefErr((e as Error).message);
    }
  };

  // --- Avanzar waypoint ---
  const [avanzarId, setAvanzarId] = useState("");
  const [avanzarRes, setAvanzarRes] = useState<Ruta | null>(null);
  const [avanzarErr, setAvanzarErr] = useState("");

  const handleAvanzar = async () => {
    setAvanzarErr(""); setAvanzarRes(null);
    try {
      setAvanzarRes(await api.avanzarWaypoint(avanzarId));
    } catch (e) {
      setAvanzarErr((e as Error).message);
    }
  };

  // --- Consultar ruta ---
  const [consultarId, setConsultarId] = useState("");
  const [consultarRes, setConsultarRes] = useState<Ruta | null>(null);
  const [consultarErr, setConsultarErr] = useState("");

  const handleConsultar = async () => {
    setConsultarErr(""); setConsultarRes(null);
    try {
      setConsultarRes(await api.obtenerRuta(consultarId));
    } catch (e) {
      setConsultarErr((e as Error).message);
    }
  };

  return (
    <div>
      <h1 style={{ margin: "0 0 24px" }}>Rutas</h1>

      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Definir ruta</h2>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px", marginBottom: 12 }}>
          <div>
            <label style={lbl}>ID de la ruta</label>
            <input style={inp} value={defForm.id} onChange={e => setDefForm({ ...defForm, id: e.target.value })} placeholder="ej: ruta-1" />
          </div>
          <div>
            <label style={lbl}>ID repartidor (opcional, asigna automáticamente)</label>
            <input style={inp} value={defForm.repartidor_id} onChange={e => setDefForm({ ...defForm, repartidor_id: e.target.value })} placeholder="ej: R1" />
          </div>
        </div>
        <label style={lbl}>Waypoints (JSON array)</label>
        <textarea
          style={{ ...inp, height: 100, resize: "vertical", fontFamily: "monospace" }}
          value={defForm.waypoints}
          onChange={e => setDefForm({ ...defForm, waypoints: e.target.value })}
        />
        <p style={{ fontSize: 12, color: "#888", margin: "4px 0 0" }}>
          Cada waypoint puede tener <code>address</code> (texto) o <code>lat</code>/<code>lon</code>.
        </p>
        <button style={btn} onClick={handleDefinir}>Definir ruta</button>
        <Result data={defRes} error={defErr} />
      </div>

      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Avanzar waypoint</h2>
        <p style={{ margin: "0 0 12px", fontSize: 13, color: "#555" }}>
          Si la ruta está <em>Activa</em> (asignada pero no iniciada), se inicia automáticamente antes de avanzar.
        </p>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end" }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID de la ruta</label>
            <input style={inp} value={avanzarId} onChange={e => setAvanzarId(e.target.value)} placeholder="ej: ruta-1" />
          </div>
          <button style={btn} onClick={handleAvanzar}>Avanzar</button>
        </div>
        <Result data={avanzarRes} error={avanzarErr} />
      </div>

      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Consultar ruta</h2>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end" }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID de la ruta</label>
            <input style={inp} value={consultarId} onChange={e => setConsultarId(e.target.value)} placeholder="ej: ruta-1" />
          </div>
          <button style={btn} onClick={handleConsultar}>Consultar</button>
        </div>
        <Result data={consultarRes} error={consultarErr} />
      </div>
    </div>
  );
}
