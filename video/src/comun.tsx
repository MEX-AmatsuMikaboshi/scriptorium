import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';
import {escenaEn} from './movimiento';
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

/**
 * Texto que se ilumina palabra por palabra justo cuando la voz lo dice. Con `reales` (cuadros de la
 * alineación forzada) cada palabra se enciende al pronunciarse; con `reales === null` el texto no se
 * dice tal cual y aparece completo en `aparece`, sin iluminarse; sin `reales` (videos antiguos) se
 * estima repartiendo [inicio, fin].
 */
export const Palabras: React.FC<{
	texto: string;
	inicio: number;
	fin: number;
	reales?: number[] | null;
	aparece?: number;
	resaltar?: string[];
	acento: string;
	atenuado?: number;
	style?: React.CSSProperties;
}> = ({texto, inicio, fin, reales, aparece = 12, resaltar = [], acento, atenuado = 0.16, style}) => {
	const frame = useCurrentFrame();
	const palabras = useMemo(() => texto.split(/\s+/).filter(Boolean), [texto]);
	const tiempos = useMemo(() => {
		if (reales === undefined) return tiemposDePalabras(palabras, inicio, fin);
		return reales && reales.length === palabras.length ? reales : null;
	}, [palabras, inicio, fin, reales]);
	const claves = useMemo(() => new Set(resaltar.flatMap((r) => r.split(/\s+/)).map(normalizar)), [resaltar]);
	const completo = interpolate(frame, [aparece, aparece + 14], [0, 1], LIMITE);
	return (
		<span style={style}>
			{palabras.map((p, i) => {
				const t = tiempos ? tiempos[i] : aparece;
				const o = tiempos ? interpolate(frame, [t - 3, t + 5], [atenuado, 1], LIMITE) : completo;
				const y = tiempos ? interpolate(frame, [t - 3, t + 7], [10, 0], LIMITE) : (1 - completo) * 14;
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

/** Fondo continuo: degradado, luces de color que derivan con la escena, partículas, viñeta y grano. */
export const Fondo: React.FC<{escenas: Escena[]}> = ({escenas}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const {i: actual, inicios: comienzos} = escenaEn(escenas, frame);
	const acento = COLORES[escenas[actual]?.acento ?? 'oro'];
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
			{escenas.map((e, k) => {
				// Luz del color de cada escena: entra y sale con ella y deriva lentamente.
				const fin = comienzos[k] + e.duracion;
				const o = interpolate(frame, [comienzos[k] - 40, comienzos[k] + 20, fin - 20, fin + 40], [0, 1, 1, 0], LIMITE);
				if (o <= 0) return null;
				const t = frame / 240;
				const cx = width * (0.5 + 0.32 * noise2D(`lx${k}`, t, 0));
				const cy = height * (0.45 + 0.28 * noise2D(`ly${k}`, t, 0));
				return (
					<AbsoluteFill
						key={k}
						style={{opacity: 0.16 * o, background: `radial-gradient(circle at ${cx}px ${cy}px, ${COLORES[e.acento]} 0%, transparent 42%)`}}
					/>
				);
			})}
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

/** Entrada suave de cada escena (las transiciones hacen el resto); la última se desvanece al final. */
export const Escenario: React.FC<{duracion: number; ultima?: boolean; children: React.ReactNode}> = ({duracion, ultima, children}) => {
	const frame = useCurrentFrame();
	const salida = ultima ? interpolate(frame, [duracion - 20, duracion - 1], [1, 0], LIMITE) : 1;
	const escala = interpolate(frame, [0, 24], [1.03, 1], {...LIMITE, easing: (t) => 1 - Math.pow(1 - t, 3)});
	return <AbsoluteFill style={{opacity: salida, transform: `scale(${escala})`}}>{children}</AbsoluteFill>;
};

/** Subtítulos: muestra la frase en curso y resalta la palabra que se está diciendo. */
export const Subtitulos: React.FC<{escenas: Escena[]}> = ({escenas}) => {
	const frame = useCurrentFrame();
	const {i, local} = escenaEn(escenas, frame);
	const actual = escenas[i];
	if (!actual || !actual.narracion || actual.tipo === 'Portada') return null;
	// Con alineación: tiempos reales y frases cortadas en la puntuación; sin ella, bloques de 12 estimados.
	const palabras = actual.palabras ? actual.palabras.map((p) => p[0]) : actual.narracion.split(/\s+/).filter(Boolean);
	const tiempos = actual.palabras ? actual.palabras.map((p) => p[1]) : tiemposDePalabras(palabras, 4, actual.voz - 6);
	const bloques: [number, number][] =
		actual.subtitulos ?? Array.from({length: Math.ceil(palabras.length / 12)}, (_, b) => [b * 12, Math.min(palabras.length, b * 12 + 12)]);
	let indice = 0;
	tiempos.forEach((t, i) => {
		if (local >= t) indice = i;
	});
	const dicha = local >= tiempos[0];
	const [desde, hasta] = bloques.find(([a, b]) => indice >= a && indice < b) ?? bloques[0] ?? [0, 0];
	// Mientras el texto principal se ilumina palabra por palabra en pantalla, el subtítulo lo repetiría.
	const karaoke = actual.tiempos_texto;
	const enPantalla = karaoke?.length
		? interpolate(local, [karaoke[0] - 8, karaoke[0], karaoke[karaoke.length - 1] + 12, karaoke[karaoke.length - 1] + 22], [0, 1, 1, 0], LIMITE)
		: 0;
	const opacidad = interpolate(local, [0, 8, actual.voz, actual.voz + 10], [0, 1, 1, 0], LIMITE) * (1 - enPantalla);
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
				{palabras.slice(desde, hasta).map((p, i) => (
					<span key={i} style={{color: dicha && desde + i === indice ? TINTA : undefined}}>
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
	const actual = escenas[escenaEn(escenas, frame).i];
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
