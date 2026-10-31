import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {noise2D} from '@remotion/noise';
import {springTiming, type TransitionPresentation} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {icons} from 'lucide';
import ICONOS from './iconos.json';

const LIMITE = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// ------------------------------------------------------------------ Transiciones entre escenas

/** Cuadros que dura cada transición (las escenas se solapan ese tiempo). */
export const TRANSICION = 24;
export const tiempoTransicion = springTiming({config: {damping: 200}, durationInFrames: TRANSICION});

// Sin fundidos entre escenas con texto: dos textos encimados a media opacidad se leen sucios.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const PRESENTACIONES: TransitionPresentation<any>[] = [
	slide({direction: 'from-right'}),
	wipe({direction: 'from-left'}),
	slide({direction: 'from-bottom'}),
	wipe({direction: 'from-top-right'}),
];
/** Transición que lleva a la escena `i` (la portada entra con fundido). */
export const presentacion = (i: number) => (i <= 1 ? fade() : PRESENTACIONES[i % PRESENTACIONES.length]);

/** Cuadro global en que empieza cada escena, descontando el solapamiento de las transiciones. */
export const inicios = (escenas: {duracion: number}[]) => {
	let t = 0;
	return escenas.map((e) => {
		const inicio = t;
		t += e.duracion - TRANSICION;
		return inicio;
	});
};

/** Índice de la escena en curso y cuadro local dentro de ella. */
export const escenaEn = (escenas: {duracion: number}[], frame: number) => {
	const s = inicios(escenas);
	let i = 0;
	s.forEach((inicio, k) => {
		if (frame >= inicio) i = k;
	});
	return {i, local: frame - s[i], inicios: s};
};

// ------------------------------------------------------------------ Cámara viva

/** Acercamiento lento y deriva suave con ruido, distinta en cada escena: la imagen nunca está quieta. */
export const Camara: React.FC<{semilla: number; duracion: number; children: React.ReactNode}> = ({semilla, duracion, children}) => {
	const frame = useCurrentFrame();
	const t = frame / 110;
	const x = noise2D(`x${semilla}`, t, 0) * 16;
	const y = noise2D(`y${semilla}`, t, 0) * 11;
	const giro = noise2D(`g${semilla}`, t, 0) * 0.3;
	const zoom = interpolate(frame, [0, duracion], [1, 1.05]);
	return <AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${zoom}) rotate(${giro}deg)`}}>{children}</AbsoluteFill>;
};

// ------------------------------------------------------------------ Pictogramas que se dibujan

type Nodo = [string, Record<string, string | number>];
const DATOS = icons as unknown as Record<string, Nodo[]>;
const CATALOGO = ICONOS as Record<string, string>;

export const existePictograma = (nombre?: string) => Boolean(nombre && DATOS[CATALOGO[nombre] ?? '']);

/** Pictograma (Lucide) que se traza línea por línea, flota y se enciende al terminar. */
export const Pictograma: React.FC<{
	nombre?: string;
	tamano: number;
	color: string;
	desde?: number;
	duracion?: number;
	grosor?: number;
}> = ({nombre, tamano, color, desde = 0, duracion = 50, grosor = 1.3}) => {
	const frame = useCurrentFrame();
	const nodos = DATOS[CATALOGO[nombre ?? ''] ?? ''];
	if (!nodos) return null;
	const flota = Math.sin((frame - desde) / 32) * 7;
	const brillo = interpolate(frame, [desde + duracion * 0.8, desde + duracion + 25], [0, 1], LIMITE);
	const entrada = interpolate(frame, [desde, desde + 12], [0.85, 1], LIMITE);
	return (
		<svg
			width={tamano}
			height={tamano}
			viewBox="0 0 24 24"
			style={{
				overflow: 'visible',
				transform: `translateY(${flota}px) scale(${entrada})`,
				filter: `drop-shadow(0 0 ${4 + 14 * brillo}px ${color}88)`,
			}}
		>
			{nodos.map(([etiqueta, atributos], i) => {
				const ini = desde + (i * duracion * 0.45) / nodos.length;
				const p = interpolate(frame, [ini, ini + duracion * 0.6], [0, 1], {...LIMITE, easing: Easing.inOut(Easing.cubic)});
				return React.createElement(etiqueta, {
					...atributos,
					key: i,
					pathLength: 1,
					fill: 'none',
					stroke: color,
					strokeWidth: grosor,
					strokeLinecap: 'round',
					strokeLinejoin: 'round',
					strokeDasharray: 1,
					strokeDashoffset: 1 - p,
				});
			})}
		</svg>
	);
};
