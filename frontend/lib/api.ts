const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3000/api/v1";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error((data as { error?: string }).error ?? "Error desconocido");
  return data as T;
}

export interface Pedido {
  id: string;
  estado: string;
  origen: Record<string, unknown>;
  destino: Record<string, unknown>;
  tipo_entrega: string;
  canal_origen: string;
  tipo_carga: string;
  peso_volumen: number;
  repartidor_asignado: string | null;
}

export interface Repartidor {
  id: string;
  capacidad: number;
  disponible: boolean;
  asignados: string[];
  ubicacion: Record<string, unknown> | null;
  current_route: string | null;
}

export interface Ruta {
  id: string;
  estado: string;
  waypoints: unknown[];
  current_index: number;
  assigned_repartidor: string | null;
  last_reached: unknown;
  metadata: Record<string, unknown>;
}

export interface Notificacion {
  pedido_id: string;
  message: string;
}

export const api = {
  // Pedidos
  crearPedido: (data: unknown) =>
    apiFetch<Pedido>("/pedidos", { method: "POST", body: JSON.stringify(data) }),
  obtenerPedido: (id: string) => apiFetch<Pedido>(`/pedidos/${id}`),
  actualizarEstado: (id: string, estado: string) =>
    apiFetch<Pedido>(`/pedidos/${id}/estado`, {
      method: "PUT",
      body: JSON.stringify({ estado }),
    }),
  asignarPedido: (pedidoId: string, repartidorId: string) =>
    apiFetch<Pedido>(`/pedidos/${pedidoId}/asignar`, {
      method: "POST",
      body: JSON.stringify({ repartidor_id: repartidorId }),
    }),

  // Repartidores
  registrarRepartidor: (data: unknown) =>
    apiFetch<Repartidor>("/repartidores", { method: "POST", body: JSON.stringify(data) }),
  obtenerRepartidor: (id: string) => apiFetch<Repartidor>(`/repartidores/${id}`),

  // Rutas
  definirRuta: (data: unknown) =>
    apiFetch<Ruta>("/rutas", { method: "POST", body: JSON.stringify(data) }),
  obtenerRuta: (id: string) => apiFetch<Ruta>(`/rutas/${id}`),
  avanzarWaypoint: (id: string) =>
    apiFetch<Ruta>(`/rutas/${id}/avanzar`, { method: "PUT" }),

  // Tracking
  obtenerEstado: (pedidoId: string) => apiFetch<Pedido>(`/tracking/${pedidoId}`),
  obtenerNotificaciones: (pedidoId: string) =>
    apiFetch<Notificacion[]>(`/tracking/${pedidoId}/notificaciones`),
};
