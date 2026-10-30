import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Escena} from './tipos';
import {COLORES, ETIQUETA, SANS, SUAVE, TINTA} from './tema';

const LIMITE = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Valor 0→1 con resorte, empezando en `desde`. */
export const useResorte = (desde = 0, amortiguacion = 200) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - desde, fps, config: {damping: amortiguacion}});
};

/** Valor 0→1 lineal con suavizado entre dos cuadros. */
export const useTramo = (inicio: number, fin: number) => {
	const frame = useCurrentFrame();
	return interpolate(frame, [inicio, fin], [0, 1], LIMITE);
};

const normalizar = (s: string) =>
	s
		.toLowerCase()
		.normalize('NFD')
		.replace(/[̀-ͯ]/g, '')
		.replace(/[^\p{L}\p{N}]/gu, '');

/** Tiempo (en cuadros) en que se pronuncia cada palabra, repartido por longitud. */
export const tiemposDePalabras = (palabras: string[], inicio: number, fin: number) => {
	const pesos = palabras.map((p) => p.length + 3);
	const total = pesos.reduce((a, b) => a + b, 0) || 1;
	let acumulado = 0;
	return pesos.map((peso) => {
		const t = inicio + ((fin - inicio) * acumulado) / total;
		acumulado += peso;
		return t;
	});
};

/** Texto que se ilumina palabra por palabra al ritmo de la voz. */
export const Palabras: React.FC<{
	texto: string;
	inicio: number;
	fin: number;
	resaltar?: string[];
	acento: string;
	atenuado?: number;
	style?: React.CSSProperties;
}> = ({texto, inicio, fin, resaltar = [], acento, atenuado = 0.16, style}) => {
	const frame = useCurrentFrame();
	const palabras = useMemo(() => texto.split(/\s+/).filter(Boolean), [texto]);
	const tiempos = useMemo(() => tiemposDePalabras(palabras, inicio, fin), [palabras, inicio, fin]);
	const claves = useMemo(() => new Set(resaltar.flatMap((r) => r.split(/\s+/)).map(normalizar)), [resaltar]);
	return (
		<span style={style}>
			{palabras.map((p, i) => {
				const t = tiempos[i];
				const o = interpolate(frame, [t - 3, t + 5], [atenuado, 1], LIMITE);
				const y = interpolate(frame, [t - 3, t + 7], [10, 0], LIMITE);
				const clave = claves.has(normalizar(p));
				return (
					<span
						key={i}
						style={{
							display: 'inline-block',
							opacity: o,
							transform: `translateY(${y}px)`,
							color: clave ? acento : undefined,
							marginRight: '0.26em',
						}}
					>
						{p}
					</span>
				);
			})}
		</span>
	);
};

/** Fondo continuo: degradado, partículas a la deriva, viñeta y grano. */
export const Fondo: React.FC<{acento: string}> = ({acento}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const particulas = useMemo(
		() =>
			new Array(80).fill(0).map((_, i) => ({
				x: random(`x${i}`) * width,
				y: random(`y${i}`) * height,
				r: 0.8 + random(`r${i}`) * 2.2,
				vx: (random(`vx${i}`) - 0.5) * 0.35,
				vy: -0.08 - random(`vy${i}`) * 0.25,
				o: 0.12 + random(`o${i}`) * 0.4,
				fase: random(`f${i}`) * Math.PI * 2,
				color: random(`c${i}`) > 0.7,
			})),
		[width, height],
	);
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 38%, #1a1c24 0%, #0f1015 55%, #08090c 100%)'}} />
			<svg width={width} height={height} style={{position: 'absolute'}}>
				{particulas.map((p, i) => {
					const x = (((p.x + frame * p.vx) % width) + width) % width;
					const y = (((p.y + frame * p.vy) % height) + height) % height;
					const titileo = 0.65 + 0.35 * Math.sin(frame / 40 + p.fase);
					return <circle key={i} cx={x} cy={y} r={p.r} fill={p.color ? acento : TINTA} opacity={p.o * titileo} />;
				})}
			</svg>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
			<svg width={width} height={height} style={{position: 'absolute', opacity: 0.07, mixBlendMode: 'overlay'}}>
				<filter id="grano">
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 12} />
				</filter>
				<rect width="100%" height="100%" filter="url(#grano)" />
			</svg>
		</AbsoluteFill>
	);
};

/** Entrada suave y salida con desvanecimiento para cada escena. */
export const Escenario: React.FC<{duracion: number; children: React.ReactNode}> = ({duracion, children}) => {
	const frame = useCurrentFrame();
	const entrada = interpolate(frame, [0, 14], [0, 1], LIMITE);
	const salida = interpolate(frame, [duracion - 14, duracion - 1], [1, 0], LIMITE);
	const escala = interpolate(frame, [0, 20], [1.025, 1], LIMITE);
	return <AbsoluteFill style={{opacity: Math.min(entrada, salida), transform: `scale(${escala})`}}>{children}</AbsoluteFill>;
};

/** Subtítulos: muestra la frase en curso y resalta la palabra que se está diciendo. */
export const Subtitulos: React.FC<{escenas: Escena[]}> = ({escenas}) => {
	const frame = useCurrentFrame();
	let inicio = 0;
	const actual = escenas.find((e) => {
		if (frame < inicio + e.duracion) return true;
		inicio += e.duracion;
		return false;
	});
	if (!actual || !actual.narracion || actual.tipo === 'Portada') return null;
	const local = frame - inicio;
	const palabras = actual.narracion.split(/\s+/).filter(Boolean);
	const tiempos = tiemposDePalabras(palabras, 4, actual.voz - 6);
	const indice = Math.max(0, tiempos.findIndex((t, i) => local >= t && (i === tiempos.length - 1 || local < tiempos[i + 1])));
	const TAM = 12;
	const bloque = Math.floor(indice / TAM);
	const visibles = palabras.slice(bloque * TAM, bloque * TAM + TAM);
	const opacidad = interpolate(local, [0, 8, actual.voz, actual.voz + 10], [0, 1, 1, 0], LIMITE);
	return (
		<AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 56}}>
			<div
				style={{
					opacity: opacidad,
					maxWidth: 1500,
					padding: '12px 26px',
					borderRadius: 14,
					background: 'rgba(5,6,9,0.55)',
					fontFamily: SANS,
					fontSize: 32,
					lineHeight: 1.35,
					color: SUAVE,
					textAlign: 'center',
				}}
			>
				{visibles.map((p, i) => (
					<span key={i} style={{color: bloque * TAM + i === indice ? TINTA : undefined}}>
						{p}{' '}
					</span>
				))}
			</div>
		</AbsoluteFill>
	);
};

/** Marca de fidelidad: nivel de intervención y párrafos de origen de la escena en curso. */
export const Insignia: React.FC<{escenas: Escena[]; nivel: string}> = ({escenas, nivel}) => {
	const frame = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	let inicio = 0;
	const actual = escenas.find((e) => {
		if (frame < inicio + e.duracion) return true;
		inicio += e.duracion;
		return false;
	});
	const anclas = actual?.anclas ?? [];
	const acento = COLORES[actual?.acento ?? 'oro'];
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', top: 44, left: 64, ...ETIQUETA, fontSize: 16, color: SUAVE}}>{nivel}</div>
			{anclas.length > 0 && actual?.tipo !== 'Cierre' && (
				<div style={{position: 'absolute', top: 40, right: 64, fontFamily: SANS, fontSize: 18, color: SUAVE, display: 'flex', gap: 10}}>
					<span style={{opacity: 0.7}}>fuente</span>
					{anclas.slice(0, 3).map((a) => (
						<span key={a} style={{color: acento, border: `1px solid ${acento}55`, borderRadius: 999, padding: '2px 10px'}}>
							§{a}
						</span>
					))}
				</div>
			)}
			<div style={{position: 'absolute', bottom: 0, left: 0, height: 4, width: `${(frame / durationInFrames) * 100}%`, background: acento, opacity: 0.8}} />
		</AbsoluteFill>
	);
};

export const tamanoPorLongitud = (texto: string, base: number) => {
	const n = texto.length;
	if (n <= 70) return base;
	if (n <= 140) return base * 0.84;
	if (n <= 220) return base * 0.72;
	return base * 0.62;
};
