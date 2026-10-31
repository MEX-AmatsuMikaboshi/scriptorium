import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Palabras, tamanoPorLongitud, useResorte, useTramo} from './comun';
import {existePictograma, Pictograma} from './movimiento';
import {COLORES, ETIQUETA, PAREJA, SANS, SERIF, SUAVE, TENUE, TINTA} from './tema';
import type {Escena, TipoEscena} from './tipos';

type Meta = {titulo: string; autor: string; capitulo: string; nivel: string};
type P = {e: Escena; meta: Meta};

const LIMITE = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const MARGEN = 170;

const Etiqueta: React.FC<{texto: string; color: string; opacidad?: number}> = ({texto, color, opacidad = 1}) => (
	<div style={{...ETIQUETA, color, opacity: opacidad}}>{texto}</div>
);

/** Línea que se dibuja de izquierda a derecha. */
const Trazo: React.FC<{ancho: number; progreso: number; color: string; grosor?: number}> = ({ancho, progreso, color, grosor = 2}) => (
	<div style={{width: ancho * progreso, height: grosor, background: color, borderRadius: grosor}} />
);

// ------------------------------------------------------------------ Portada

const Portada: React.FC<P> = ({e, meta}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const acento = COLORES[e.acento];
	const linea = useResorte(18);
	const letras = meta.titulo.split('');
	const tamano = meta.titulo.length > 28 ? 110 : 150;
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: `0 ${MARGEN}px`}}>
			<Etiqueta texto={meta.autor} color={acento} opacidad={interpolate(frame, [0, 22], [0, 1], LIMITE)} />
			<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: tamano, color: TINTA, lineHeight: 1.05, margin: '30px 0 34px'}}>
				{letras.map((l, i) => {
					const s = spring({frame: frame - 6 - i * 1.4, fps, config: {damping: 18, mass: 0.6}});
					return (
						<span key={i} style={{display: 'inline-block', opacity: s, transform: `translateY(${(1 - s) * 40}px)`, whiteSpace: 'pre'}}>
							{l}
						</span>
					);
				})}
			</div>
			<Trazo ancho={560} progreso={linea} color={acento} />
			<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 50, color: SUAVE, marginTop: 34, opacity: useTramo(30, 55)}}>
				{meta.capitulo}
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Cita

const Cita: React.FC<P> = ({e, meta}) => {
	const frame = useCurrentFrame();
	const acento = COLORES[e.acento];
	const entrada = useResorte(0);
	const tamano = tamanoPorLongitud(e.cuerpo, 76);
	const [desde, hasta] = e.revelar ?? [0.05, 0.92];
	const deriva = Math.sin(frame / 45) * 10;
	return (
		<AbsoluteFill style={{justifyContent: 'center', padding: `0 ${MARGEN + 60}px`}}>
			<div
				style={{
					position: 'absolute',
					left: 110,
					top: 30,
					fontFamily: SERIF,
					fontSize: 480,
					lineHeight: 1,
					color: acento,
					opacity: 0.13 * entrada,
					transform: `translate(${(1 - entrada) * -60}px, ${deriva}px) rotate(${(1 - entrada) * -14}deg)`,
				}}
			>
				«
			</div>
			<div style={{fontFamily: SERIF, fontSize: tamano, lineHeight: 1.28, color: TINTA}}>
				<Palabras texto={e.cuerpo} inicio={Math.max(6, e.voz * desde)} fin={e.voz * Math.min(0.97, hasta)} reales={e.tiempos_texto} aparece={e.aparece?.texto} resaltar={e.resaltar} acento={acento} atenuado={0.22} />
			</div>
			<div style={{display: 'flex', alignItems: 'center', gap: 22, marginTop: 46, opacity: useTramo(20, 45)}}>
				<Trazo ancho={80} progreso={useResorte(20)} color={acento} />
				<span style={{fontFamily: SANS, fontSize: 26, letterSpacing: '0.08em', color: SUAVE}}>
					{meta.autor} · cita textual · §{e.anclas[0] ?? ''}
				</span>
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Concepto

const Concepto: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const acento = COLORES[e.acento];
	const termino = useResorte(4, 14);
	const anillo = useTramo(4, 50);
	const r = 150;
	const circ = 2 * Math.PI * r;
	return (
		<AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', padding: `0 ${MARGEN}px`, gap: 90}}>
			<div style={{position: 'relative', width: 2 * r + 20, height: 2 * r + 20, flexShrink: 0}}>
				<svg width={2 * r + 20} height={2 * r + 20}>
					<circle cx={r + 10} cy={r + 10} r={r} fill="none" stroke={TENUE} strokeWidth={2} />
					<circle
						cx={r + 10}
						cy={r + 10}
						r={r}
						fill="none"
						stroke={acento}
						strokeWidth={3}
						strokeDasharray={circ}
						strokeDashoffset={circ * (1 - anillo)}
						transform={`rotate(${-90 + frame * 0.3} ${r + 10} ${r + 10})`}
						strokeLinecap="round"
					/>
					{!existePictograma(e.icono) && <circle cx={r + 10} cy={r + 10} r={8 + 4 * Math.sin(frame / 12)} fill={acento} opacity={0.9} />}
				</svg>
				<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
					<Pictograma nombre={e.icono} tamano={170} color={acento} desde={10} />
				</AbsoluteFill>
			</div>
			<div style={{flex: 1}}>
				<Etiqueta texto="Concepto" color={acento} opacidad={termino} />
				<div
					style={{
						fontFamily: SERIF,
						fontWeight: 500,
						fontSize: tamanoPorLongitud(e.titular, 120),
						color: TINTA,
						lineHeight: 1.05,
						margin: '18px 0 26px',
						opacity: termino,
						transform: `translateX(${(1 - termino) * -30}px)`,
					}}
				>
					{e.titular}
				</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: tamanoPorLongitud(e.cuerpo, 50), lineHeight: 1.35, color: TINTA}}>
					<Palabras texto={e.cuerpo} inicio={18} fin={e.voz * 0.9} reales={e.tiempos_texto} aparece={e.aparece?.texto} resaltar={e.resaltar} acento={acento} atenuado={0.12} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Lista

const Lista: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const acento = COLORES[e.acento];
	const n = Math.max(1, e.items.length);
	const paso = (e.voz * 0.82) / n;
	return (
		<AbsoluteFill style={{justifyContent: 'center', padding: `0 ${MARGEN + 40}px 60px`}}>
			{existePictograma(e.icono) && (
				<div style={{position: 'absolute', right: MARGEN, top: '50%', transform: 'translateY(-55%)', opacity: 0.9}}>
					<Pictograma nombre={e.icono} tamano={300} color={acento} desde={6} duracion={70} grosor={0.9} />
				</div>
			)}
			<Etiqueta texto={`${n} ${n === 1 ? 'idea' : 'ideas'}`} color={acento} opacidad={useTramo(0, 15)} />
			<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: tamanoPorLongitud(e.titular, 84), color: TINTA, margin: '14px 0 50px', opacity: useResorte(2)}}>
				{e.titular}
			</div>
			<div style={{display: 'flex', flexDirection: 'column', gap: 30}}>
				{e.items.map((item, i) => {
					const s = spring({frame: frame - (e.aparece?.items?.[i] ?? 12 + i * paso), fps, config: {damping: 16}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 30, opacity: s, transform: `translateX(${(1 - s) * -50}px)`}}>
							<div
								style={{
									width: 64,
									height: 64,
									borderRadius: 32,
									border: `2px solid ${acento}`,
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									fontFamily: SANS,
									fontWeight: 600,
									fontSize: 26,
									color: acento,
									flexShrink: 0,
								}}
							>
								{i + 1}
							</div>
							<div style={{fontFamily: SANS, fontSize: n > 4 ? 40 : 48, lineHeight: 1.25, color: TINTA}}>{item}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Contraste

const Contraste: React.FC<P> = ({e}) => {
	const a = COLORES[e.acento];
	const b = COLORES[PAREJA[e.acento]];
	const izq = useResorte(e.aparece?.izquierda ?? 4, 16);
	const der = useResorte(e.aparece?.derecha ?? Math.round(e.voz * 0.38), 16);
	const linea = useTramo(0, 30);
	const Columna: React.FC<{lado: {titulo: string; texto: string}; color: string; s: number; dir: number}> = ({lado, color, s, dir}) => (
		<div style={{flex: 1, opacity: s, transform: `translateX(${(1 - s) * 60 * dir}px)`, padding: '0 40px'}}>
			<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: tamanoPorLongitud(lado.titulo, 84), color, lineHeight: 1.05, marginBottom: 28}}>{lado.titulo}</div>
			<div style={{fontFamily: SANS, fontSize: tamanoPorLongitud(lado.texto, 40), lineHeight: 1.4, color: TINTA}}>{lado.texto}</div>
		</div>
	);
	return (
		<AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', padding: `0 ${MARGEN - 40}px`}}>
			<Columna lado={e.izquierda} color={a} s={izq} dir={-1} />
			<div style={{position: 'relative', width: 2, height: 560 * linea, background: TENUE}}>
				<div
					style={{
						position: 'absolute',
						top: '50%',
						left: '50%',
						transform: `translate(-50%, -50%) scale(${der})`,
						width: 72,
						height: 72,
						borderRadius: 36,
						background: '#0d0e12',
						border: `2px solid ${TENUE}`,
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						color: SUAVE,
						fontFamily: SANS,
						fontSize: 30,
					}}
				>
					↔
				</div>
			</div>
			<Columna lado={e.derecha} color={b} s={der} dir={1} />
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Argumento

const Argumento: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const {fps, width} = useVideoConfig();
	const acento = COLORES[e.acento];
	const premisas = e.items.slice(0, 4);
	const n = Math.max(1, premisas.length);
	const ancho = width - 2 * MARGEN;
	const hueco = 36;
	const tarjeta = (ancho - hueco * (n - 1)) / n;
	const finPremisas = e.voz * 0.55;
	const llegada = e.aparece?.texto ?? Math.round(finPremisas + 18); // cuando la voz dice la conclusión
	const flechas = useTramo(llegada - 22, llegada + 3);
	const conclusion = useResorte(llegada, 16);
	const yTarjetas = 250;
	const altoTarjeta = 210;
	const yConclusion = 640;
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', left: MARGEN, top: 170}}>
				<Etiqueta texto="Premisas" color={SUAVE} />
			</div>
			{premisas.map((p, i) => {
				const s = spring({frame: frame - (e.aparece?.items?.[i] ?? 6 + (i * finPremisas) / n), fps, config: {damping: 16}});
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: MARGEN + i * (tarjeta + hueco),
							top: yTarjetas,
							width: tarjeta,
							height: altoTarjeta,
							borderRadius: 18,
							border: `1px solid ${TENUE}`,
							background: 'rgba(255,255,255,0.03)',
							padding: '22px 30px',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							textAlign: 'center',
							fontFamily: SANS,
							fontSize: n > 3 ? 30 : 34,
							lineHeight: 1.35,
							color: TINTA,
							opacity: s,
							transform: `perspective(1100px) rotateX(${(1 - s) * -55}deg) translateY(${(1 - s) * -30}px)`,
							transformOrigin: 'top center',
						}}
					>
						{p}
					</div>
				);
			})}
			<svg width={width} height={1080} style={{position: 'absolute', top: 0, left: 0}}>
				{premisas.map((_, i) => {
					const x1 = MARGEN + i * (tarjeta + hueco) + tarjeta / 2;
					const y1 = yTarjetas + altoTarjeta + 12;
					const x2 = width / 2;
					const y2 = yConclusion - 16;
					const largo = Math.hypot(x2 - x1, y2 - y1) + 60;
					const d = `M ${x1} ${y1} C ${x1} ${y1 + 90}, ${x2} ${y2 - 90}, ${x2} ${y2}`;
					return <path key={i} d={d} fill="none" stroke={acento} strokeWidth={2} strokeDasharray={largo} strokeDashoffset={largo * (1 - flechas)} opacity={0.75} />;
				})}
			</svg>
			<div
				style={{
					position: 'absolute',
					left: width / 2 - 560,
					top: yConclusion,
					width: 1120,
					borderRadius: 20,
					border: `2px solid ${acento}`,
					background: 'rgba(10,11,15,0.85)',
					padding: '26px 34px',
					textAlign: 'center',
					opacity: conclusion,
					transform: `scale(${0.92 + 0.08 * conclusion})`,
				}}
			>
				<Etiqueta texto="Conclusión" color={acento} />
				<div style={{fontFamily: SERIF, fontSize: tamanoPorLongitud(e.cuerpo, 46), lineHeight: 1.3, color: TINTA, marginTop: 12}}>{e.cuerpo}</div>
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Palabra clave

const PalabraClave: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const acento = COLORES[e.acento];
	const s = useResorte(2, 20);
	const espaciado = interpolate(frame, [0, 40], [0.5, 0.03], {...LIMITE, easing: (t) => 1 - Math.pow(1 - t, 3)});
	const puntos = 56;
	const radio = 380 + 20 * Math.sin(frame / 30);
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
			<svg width={1000} height={1000} style={{position: 'absolute', opacity: 0.85}}>
				{new Array(puntos).fill(0).map((_, i) => {
					const ang = (i / puntos) * Math.PI * 2 + frame * 0.004;
					const llegada = spring({frame: frame - i * 0.4, fps, config: {damping: 22}});
					const rr = radio + (1 - llegada) * 400 * (random(`pk${i}`) - 0.3);
					return <circle key={i} cx={500 + Math.cos(ang) * rr} cy={500 + Math.sin(ang) * rr} r={i % 7 === 0 ? 3.2 : 1.6} fill={i % 7 === 0 ? acento : TINTA} opacity={0.55 * llegada} />;
				})}
			</svg>
			{existePictograma(e.icono) && (
				<div style={{marginBottom: 18}}>
					<Pictograma nombre={e.icono} tamano={150} color={acento} desde={2} grosor={1.2} />
				</div>
			)}
			<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: tamanoPorLongitud(e.titular, 190), letterSpacing: `${espaciado}em`, color: acento, opacity: s, transform: `scale(${0.85 + 0.15 * s})`}}>
				{e.titular}
			</div>
			{e.cuerpo && (
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: tamanoPorLongitud(e.cuerpo, 44), color: TINTA, maxWidth: 1250, marginTop: 34, lineHeight: 1.35}}>
					<Palabras texto={e.cuerpo} inicio={24} fin={e.voz * 0.92} reales={e.tiempos_texto} aparece={e.aparece?.texto} acento={acento} resaltar={e.resaltar} />
				</div>
			)}
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Pregunta

const Pregunta: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const acento = COLORES[e.acento];
	const trazo = useTramo(0, 40);
	const relleno = useTramo(30, 60);
	const texto = e.titular || e.cuerpo;
	const vaiven = Math.sin(frame / 38) * 4 * relleno; // el signo «duda» una vez dibujado
	return (
		<AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', padding: `0 ${MARGEN}px`, gap: 70}}>
			<div style={{position: 'relative', fontFamily: SERIF, fontSize: 560, lineHeight: 0.8, opacity: trazo, transform: `rotate(${(1 - trazo) * -12 + vaiven}deg)`}}>
				<div style={{color: 'transparent', WebkitTextStroke: `3px ${acento}`}}>?</div>
				<div style={{position: 'absolute', inset: 0, color: acento, opacity: 0.85 * relleno}}>?</div>
			</div>
			<div style={{flex: 1}}>
				<Etiqueta texto="La pregunta" color={acento} opacidad={trazo} />
				<div style={{fontFamily: SERIF, fontSize: tamanoPorLongitud(texto, 72), lineHeight: 1.22, color: TINTA, marginTop: 22}}>
					<Palabras texto={texto} inicio={10} fin={e.voz * 0.9} reales={e.tiempos_texto} aparece={e.aparece?.texto} resaltar={e.resaltar} acento={acento} />
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Respiro (campo de partículas que se organiza)

const Respiro: React.FC<P> = ({e}) => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const acento = COLORES[e.acento];
	const orden = useResorte(4, 30);
	const puntos = useMemo(
		() => new Array(140).fill(0).map((_, i) => ({x: random(`rx${i}-${e.semilla}`) * width, y: random(`ry${i}-${e.semilla}`) * height})),
		[width, height, e.semilla],
	);
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
			<svg width={width} height={height} style={{position: 'absolute'}}>
				{puntos.map((p, i) => {
					const ang = (i / puntos.length) * Math.PI * 2 + frame * 0.006;
					const r = 300 + 26 * Math.sin(i * 1.7 + frame / 25);
					const x = p.x + (width / 2 + Math.cos(ang) * r - p.x) * orden;
					const y = p.y + (height / 2 + Math.sin(ang) * r - p.y) * orden;
					return <circle key={i} cx={x} cy={y} r={i % 9 === 0 ? 3 : 1.7} fill={i % 9 === 0 ? acento : TINTA} opacity={0.6} />;
				})}
			</svg>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26}}>
				<Pictograma nombre={e.icono} tamano={190} color={acento} desde={14} duracion={70} grosor={1.1} />
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: tamanoPorLongitud(e.titular, 60), color: TINTA, maxWidth: 520, textAlign: 'center', opacity: useTramo(20, 45)}}>
					{e.titular}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ------------------------------------------------------------------ Cierre

const Cierre: React.FC<P & {anclas: string[]}> = ({e, meta, anclas}) => {
	const acento = COLORES[e.acento];
	return (
		<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: `0 ${MARGEN}px`}}>
			<Etiqueta texto="Fuente" color={acento} opacidad={useTramo(0, 20)} />
			<div style={{fontFamily: SERIF, fontWeight: 500, fontSize: 84, color: TINTA, margin: '24px 0 10px', opacity: useResorte(4)}}>{meta.titulo}</div>
			<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 44, color: SUAVE, opacity: useTramo(10, 30)}}>
				{meta.autor} · {meta.capitulo}
			</div>
			<div style={{margin: '44px 0 26px'}}>
				<Trazo ancho={420} progreso={useResorte(16)} color={acento} />
			</div>
			<div style={{fontFamily: SANS, fontSize: 26, color: SUAVE, maxWidth: 1200, lineHeight: 1.5, opacity: useTramo(24, 50)}}>
				{meta.nivel}: cada idea de este video está anclada a su párrafo de origen.
			</div>
			<div style={{display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center', maxWidth: 1300, marginTop: 26, opacity: useTramo(34, 60)}}>
				{anclas.map((a) => (
					<span key={a} style={{fontFamily: SANS, fontSize: 20, color: acento, border: `1px solid ${acento}55`, borderRadius: 999, padding: '3px 12px'}}>
						§{a}
					</span>
				))}
			</div>
		</AbsoluteFill>
	);
};

const ESCENAS: Record<TipoEscena, React.FC<P & {anclas: string[]}>> = {
	Portada,
	Cita,
	Concepto,
	Lista,
	Contraste,
	Argumento,
	PalabraClave,
	Pregunta,
	Respiro,
	Cierre,
};

export const EscenaKit: React.FC<P & {anclas: string[]}> = (props) => {
	const Componente = ESCENAS[props.e.tipo] ?? Concepto;
	return <Componente {...props} />;
};
