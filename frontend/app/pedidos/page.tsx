"use client";
import { useState } from "react";
import { api, Pedido } from "../../lib/api";

const inp: React.CSSProperties = {
  display: "block", width: "100%", padding: "8px 10px",
  border: "1px solid #ddd", borderRadius: 6, fontSize: 14, boxSizing: "border-box",
};
const lbl: React.CSSProperties = { display: "block", marginBottom: 4, fontWeight: 600, fontSize: 13 };
const btn: React.CSSProperties = {
  padding: "9px 20px", background: "#4f46e5", color: "white",
  border: "none", borderRadius: 6, cursor: "pointer", fontSize: 14, marginTop: 4,
};
const card: React.CSSProperties = {
  background: "white", borderRadius: 10, padding: 24,
  boxShadow: "0 1px 4px rgba(0,0,0,.08)", marginBottom: 24,
};
const grid2: React.CSSProperties = { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px 16px" };

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

export default function PedidosPage() {
  // --- Crear pedido ---
  const [form, setForm] = useState({
    id: "", origenDir: "", origenId: "",
    destinoDir: "", destinoNombre: "", destinoContacto: "",
    tipo_entrega: "normal", canal_origen: "web", tipo_carga: "", peso_volumen: "",
  });
  const [crearRes, setCrearRes] = useState<Pedido | null>(null);
  const [crearErr, setCrearErr] = useState("");

  const handleCrear = async () => {
    setCrearErr(""); setCrearRes(null);
    try {
      const result = await api.crearPedido({
        id: form.id,
        origen: { direccion: form.origenDir, id_punto_origen: form.origenId },
        destino: { direccion: form.destinoDir, nombre_destinatario: form.destinoNombre, medio_contacto: form.destinoContacto },
        tipo_entrega: form.tipo_entrega,
        canal_origen: form.canal_origen,
        tipo_carga: form.tipo_carga,
        peso_volumen: Number(form.peso_volumen),
      });
      setCrearRes(result);
    } catch (e) {
      setCrearErr((e as Error).message);
    }
  };

  // --- Actualizar estado ---
  const [estadoId, setEstadoId] = useState("");
  const [nuevoEstado, setNuevoEstado] = useState("Validado");
  const [estadoRes, setEstadoRes] = useState<Pedido | null>(null);
  const [estadoErr, setEstadoErr] = useState("");

  const handleEstado = async () => {
    setEstadoErr(""); setEstadoRes(null);
    try {
      setEstadoRes(await api.actualizarEstado(estadoId, nuevoEstado));
    } catch (e) {
      setEstadoErr((e as Error).message);
    }
  };

  // --- Asignar pedido ---
  const [asignarPedidoId, setAsignarPedidoId] = useState("");
  const [asignarRepId, setAsignarRepId] = useState("");
  const [asignarRes, setAsignarRes] = useState<Pedido | null>(null);
  const [asignarErr, setAsignarErr] = useState("");

  const handleAsignar = async () => {
    setAsignarErr(""); setAsignarRes(null);
    try {
      setAsignarRes(await api.asignarPedido(asignarPedidoId, asignarRepId));
    } catch (e) {
      setAsignarErr((e as Error).message);
    }
  };

  // --- Consultar pedido ---
  const [consultarId, setConsultarId] = useState("");
  const [consultarRes, setConsultarRes] = useState<Pedido | null>(null);
  const [consultarErr, setConsultarErr] = useState("");

  const handleConsultar = async () => {
    setConsultarErr(""); setConsultarRes(null);
    try {
      setConsultarRes(await api.obtenerPedido(consultarId));
    } catch (e) {
      setConsultarErr((e as Error).message);
    }
  };

  return (
    <div>
      <h1 style={{ margin: "0 0 24px" }}>Pedidos</h1>

      {/* CREAR */}
      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Crear pedido</h2>
        <div style={grid2}>
          <div>
            <label style={lbl}>ID del pedido</label>
            <input style={inp} value={form.id} onChange={e => setForm({ ...form, id: e.target.value })} placeholder="ej: P001" />
          </div>
          <div>
            <label style={lbl}>Canal origen</label>
            <select style={inp} value={form.canal_origen} onChange={e => setForm({ ...form, canal_origen: e.target.value })}>
              <option value="web">web</option>
              <option value="mobile">mobile</option>
              <option value="api">api</option>
              <option value="telefono">telefono</option>
            </select>
          </div>
          <div>
            <label style={lbl}>Origen — dirección</label>
            <input style={inp} value={form.origenDir} onChange={e => setForm({ ...form, origenDir: e.target.value })} placeholder="ej: Av. Principal 100" />
          </div>
          <div>
            <label style={lbl}>Origen — id_punto_origen</label>
            <input style={inp} value={form.origenId} onChange={e => setForm({ ...form, origenId: e.target.value })} placeholder="ej: CD-Norte" />
          </div>
          <div>
            <label style={lbl}>Destino — dirección</label>
            <input style={inp} value={form.destinoDir} onChange={e => setForm({ ...form, destinoDir: e.target.value })} placeholder="ej: Calle Los Pinos 42" />
          </div>
          <div>
            <label style={lbl}>Destino — nombre destinatario</label>
            <input style={inp} value={form.destinoNombre} onChange={e => setForm({ ...form, destinoNombre: e.target.value })} placeholder="ej: Juan Pérez" />
          </div>
          <div>
            <label style={lbl}>Destino — medio de contacto</label>
            <input style={inp} value={form.destinoContacto} onChange={e => setForm({ ...form, destinoContacto: e.target.value })} placeholder="ej: +56912345678" />
          </div>
          <div>
            <label style={lbl}>Tipo de entrega</label>
            <select style={inp} value={form.tipo_entrega} onChange={e => setForm({ ...form, tipo_entrega: e.target.value })}>
              <option value="normal">normal</option>
              <option value="express">express</option>
              <option value="programada">programada</option>
            </select>
          </div>
          <div>
            <label style={lbl}>Tipo de carga</label>
            <input style={inp} value={form.tipo_carga} onChange={e => setForm({ ...form, tipo_carga: e.target.value })} placeholder="ej: paquete" />
          </div>
          <div>
            <label style={lbl}>Peso / volumen (kg)</label>
            <input style={inp} type="number" value={form.peso_volumen} onChange={e => setForm({ ...form, peso_volumen: e.target.value })} placeholder="ej: 5" />
          </div>
        </div>
        <button style={btn} onClick={handleCrear}>Crear pedido</button>
        <Result data={crearRes} error={crearErr} />
      </div>

      {/* ACTUALIZAR ESTADO */}
      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Actualizar estado</h2>
        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID del pedido</label>
            <input style={inp} value={estadoId} onChange={e => setEstadoId(e.target.value)} placeholder="ej: P001" />
          </div>
          <div style={{ flex: 1 }}>
            <label style={lbl}>Nuevo estado</label>
            <select style={inp} value={nuevoEstado} onChange={e => setNuevoEstado(e.target.value)}>
              <option value="Validado">Validado</option>
              <option value="Cancelado">Cancelado</option>
            </select>
          </div>
        </div>
        <button style={btn} onClick={handleEstado}>Actualizar</button>
        <Result data={estadoRes} error={estadoErr} />
      </div>

      {/* ASIGNAR */}
      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Asignar a repartidor</h2>
        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID del pedido</label>
            <input style={inp} value={asignarPedidoId} onChange={e => setAsignarPedidoId(e.target.value)} placeholder="ej: P001" />
          </div>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID del repartidor</label>
            <input style={inp} value={asignarRepId} onChange={e => setAsignarRepId(e.target.value)} placeholder="ej: R1" />
          </div>
        </div>
        <button style={btn} onClick={handleAsignar}>Asignar</button>
        <Result data={asignarRes} error={asignarErr} />
      </div>

      {/* CONSULTAR */}
      <div style={card}>
        <h2 style={{ margin: "0 0 16px", fontSize: 16 }}>Consultar pedido</h2>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end" }}>
          <div style={{ flex: 1 }}>
            <label style={lbl}>ID del pedido</label>
            <input style={inp} value={consultarId} onChange={e => setConsultarId(e.target.value)} placeholder="ej: P001" />
          </div>
          <button style={btn} onClick={handleConsultar}>Consultar</button>
        </div>
        <Result data={consultarRes} error={consultarErr} />
      </div>
    </div>
  );
}
