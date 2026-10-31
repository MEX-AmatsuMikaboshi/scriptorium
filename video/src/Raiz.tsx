import React from 'react';
import {CalculateMetadataFunction, Composition} from 'remotion';
import {Explicador} from './Explicador';
import {TRANSICION} from './movimiento';
import type {Escena, PropsExplicador} from './tipos';

const ejemplo = (tipo: Escena['tipo'], extra: Partial<Escena> = {}): Escena => ({
	tipo,
	duracion: 240,
	voz: 210,
	audio: null,
	narracion: 'El pensar bien consiste: o en conocer la verdad o en dirigir el entendimiento por el camino que conduce a ella.',
	anclas: ['1.1.1'],
	titular: 'Pensar bien',
	cuerpo: 'El pensar bien consiste: o en conocer la verdad o en dirigir el entendimiento por el camino que conduce a ella.',
	items: ['Conocer la verdad', 'Dirigir el entendimiento', 'Seguir el camino que conduce a ella'],
	izquierda: {titulo: 'Espejo', texto: 'Muestra los objetos como son en sí.'},
	derecha: {titulo: 'Vidrio de ilusión', texto: 'Presenta lo que realmente no existe.'},
	resaltar: ['verdad'],
	acento: 'oro',
	semilla: 1,
	...extra,
});

// Props de ejemplo para el Studio; en producción llegan desde Python con --props.
const porDefecto: PropsExplicador = {
	titulo: 'El criterio',
	autor: 'Jaime Balmes',
	capitulo: 'Capítulo I. Consideraciones preliminares',
	nivel: 'Nivel 2 · Explicativo fiel',
	escenas: [
		ejemplo('Portada'),
		ejemplo('Pregunta', {titular: '¿En qué consiste el pensar bien?', acento: 'azul'}),
		ejemplo('Cita', {resaltar: ['verdad', 'entendimiento']}),
		ejemplo('Concepto', {titular: 'La verdad', cuerpo: 'La verdad es la realidad de las cosas.', acento: 'verde', icono: 'ojo'}),
		ejemplo('Lista', {titular: 'El buen pensador', acento: 'violeta', icono: 'brújula'}),
		ejemplo('Contraste'),
		ejemplo('Argumento', {cuerpo: 'Pensar bien interesa a todos, no solo a los filósofos.', acento: 'azul'}),
		ejemplo('PalabraClave', {titular: 'Criterio', cuerpo: 'Ver en los objetos todo lo que hay, pero no más de lo que hay.', icono: 'balanza'}),
		ejemplo('Respiro', {titular: 'Una antorcha en el sendero', acento: 'violeta', icono: 'llama'}),
		ejemplo('Cierre', {duracion: 240, voz: 0, narracion: ''}),
	],
};

// Las transiciones solapan escenas consecutivas: el total descuenta ese solapamiento.
const calcular: CalculateMetadataFunction<PropsExplicador> = ({props}) => ({
	durationInFrames: Math.max(1, props.escenas.reduce((total, e) => total + e.duracion, 0) - TRANSICION * Math.max(0, props.escenas.length - 1)),
});

export const Raiz: React.FC = () => (
	<>
		<Composition
			id="Explicador"
			component={Explicador}
			width={1920}
			height={1080}
			fps={60}
			durationInFrames={1}
			defaultProps={porDefecto}
			calculateMetadata={calcular}
		/>
	</>
);
