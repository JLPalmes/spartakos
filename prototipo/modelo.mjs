// SPDX-License-Identifier: AGPL-3.0-or-later
// Modelo descartable de experiencia. No implementa identidad, seguridad ni una red.
export const initialState = () => ({
  page: 'inicio', saved: [], followed: [], posts: [], imported: false,
  community: { visibility: 'private', members: ['alicia', 'bruno', 'carla'],
    protected: [], consents: {}, proposal: false, version: 0 },
  message: '',
});

export function transition(previous, event) {
  const state = structuredClone(previous);
  state.message = '';
  const c = state.community;
  switch (event.type) {
    case 'navigate':
      if (!['inicio', 'explorar', 'guardado', 'comunidad', 'archivo', 'continuidad'].includes(event.page)) throw Error('Destino desconocido');
      state.page = event.page;
      break;
    case 'save':
      state.saved = state.saved.includes(event.id) ? state.saved.filter(id => id !== event.id) : [...state.saved, event.id];
      state.message = 'Selección privada actualizada. No expresa acuerdo ni se publica.';
      break;
    case 'follow':
      state.followed = state.followed.includes(event.id) ? state.followed.filter(id => id !== event.id) : [...state.followed, event.id];
      state.message = 'Seguimiento actualizado. No modifica los permisos de acceso.';
      break;
    case 'publish': {
      if (!['public', 'community'].includes(event.audience)) throw Error('Audiencia desconocida');
      const text = String(event.text ?? '').trim();
      if (!text) throw Error('Escribe algo antes de publicar.');
      if (text.length > 3000) throw Error('El prototipo admite hasta 3000 caracteres.');
      state.posts.push({id: `local-${state.posts.length + 1}`, text, audience: event.audience});
      state.message = event.audience === 'community' ? 'Simulación: publicación solo para integrantes. El operador podría leerla.' : 'Simulación: publicación pública.';
      break;
    }
    case 'import-demo':
      state.imported = true;
      state.message = 'Archivo ficticio incorporado. Sus contactos no son cuentas activas de Spartakos.';
      break;
    case 'propose-open':
      if (c.visibility !== 'private') throw Error('Esta comunidad ya es pública.');
      c.proposal = true;
      c.version += 1;
      c.consents = {};
      state.message = 'Nueva propuesta: apertura futura con historial anterior protegido. Requiere todos los consentimientos.';
      break;
    case 'consent':
      if (!c.proposal) throw Error('No hay propuesta de apertura vigente.');
      if (event.version !== c.version) throw Error('La propuesta cambió. El consentimiento anterior no es válido.');
      if (![...c.members, ...c.protected].includes(event.member)) throw Error('La persona no pertenece al censo protegido.');
      if (event.value !== true) {
        c.proposal = false;
        c.consents = {};
        state.message = 'Propuesta cerrada por una negativa. La comunidad continúa privada.';
      } else {
        c.consents[event.member] = true;
        state.message = 'Consentimiento registrado para esta propuesta. La apertura aún requiere comprobar el censo completo.';
      }
      break;
    case 'remove-member':
      if (!c.members.includes(event.member)) throw Error('La persona no es integrante actual.');
      // Modelo conservador: evita también cerrar una propuesta, expulsar y reiniciarla.
      if (!c.protected.includes(event.member)) c.protected.push(event.member);
      c.members = c.members.filter(member => member !== event.member);
      c.proposal = false;
      c.consents = {};
      c.version += 1;
      state.message = 'La baja cancela la propuesta. No elimina la protección frente a una apertura elusiva.';
      break;
    case 'open': {
      const census = [...new Set([...c.members, ...c.protected])];
      if (!c.proposal || !census.length || !census.every(id => c.consents[id] === true)) throw Error('Falta consentimiento expreso de todo el censo protegido.');
      c.visibility = 'public';
      c.proposal = false;
      state.message = 'Apertura simulada para publicaciones futuras. El historial anterior sigue restringido.';
      break;
    }
    default: throw Error('Acción desconocida');
  }
  return state;
}
