import type {Acento} from './tema';

export type TipoEscena =
	| 'Portada'
	| 'Cita'
	| 'Concepto'
	| 'Lista'
	| 'Contraste'
	| 'Argumento'
	| 'PalabraClave'
	| 'Pregunta'
	| 'Respiro'
	| 'Cierre';

export type Escena = {
	tipo: TipoEscena;
	/** Duración total de la escena, en cuadros. */
	duracion: number;
	/** Cuadros que dura la voz dentro de la escena (el resto es respiro). */
	voz: number;
	/** Archivo de audio dentro de la carpeta pública del trabajo. */
	audio: string | null;
	narracion: string;
	anclas: string[];
	titular: string;
	cuerpo: string;
	items: string[];
	izquierda: {titulo: string; texto: string};
	derecha: {titulo: string; texto: string};
	resaltar: string[];
	/** Fracción [inicio, fin] de la voz en la que se ilumina el texto en pantalla (p. ej. la cita). */
	revelar?: [number, number];
	acento: Acento;
	semilla: number;
};

export type PropsExplicador = {
	titulo: string;
	autor: string;
	capitulo: string;
	nivel: string;
	escenas: Escena[];
};
