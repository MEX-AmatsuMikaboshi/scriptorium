import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, continueRender, delayRender, staticFile} from 'remotion';
import {TransitionSeries} from '@remotion/transitions';
import {Escenario, Fondo, Insignia, Subtitulos} from './comun';
import {EscenaKit} from './escenas';
import {Camara, presentacion, tiempoTransicion} from './movimiento';
import {FONDO} from './tema';
import type {PropsExplicador} from './tipos';

/** Espera a que las fuentes estén cargadas antes de dibujar el primer cuadro. */
const useFuentes = () => {
	const [handle] = useState(() => delayRender('Cargando fuentes'));
	useEffect(() => {
		Promise.all([
			document.fonts.load('500 64px "EB Garamond"'),
			document.fonts.load('italic 400 64px "EB Garamond"'),
			document.fonts.load('400 32px Inter'),
			document.fonts.load('600 32px Inter'),
		])
			.then(() => continueRender(handle))
			.catch(() => continueRender(handle));
	}, [handle]);
};

export const Explicador: React.FC<PropsExplicador> = ({titulo, autor, capitulo, nivel, escenas}) => {
	useFuentes();
	const meta = {titulo, autor, capitulo, nivel};
	const todasLasAnclas = Array.from(new Set(escenas.flatMap((e) => e.anclas))).sort((a, b) =>
		a.localeCompare(b, undefined, {numeric: true}),
	);
	return (
		// Renglones equilibrados en todo el kit: sin una palabra suelta al final de un titular.
		<AbsoluteFill style={{backgroundColor: FONDO, textWrap: 'balance'}}>
			<Fondo escenas={escenas} />
			<TransitionSeries>
				{escenas.map((e, i) => (
					<React.Fragment key={i}>
						{i > 0 && <TransitionSeries.Transition presentation={presentacion(i)} timing={tiempoTransicion} />}
						<TransitionSeries.Sequence durationInFrames={e.duracion}>
							<Escenario duracion={e.duracion} ultima={i === escenas.length - 1}>
								<Camara semilla={e.semilla} duracion={e.duracion}>
									<EscenaKit e={e} meta={meta} anclas={todasLasAnclas} />
								</Camara>
							</Escenario>
							{e.audio && <Audio src={staticFile(e.audio)} />}
						</TransitionSeries.Sequence>
					</React.Fragment>
				))}
			</TransitionSeries>
			<Subtitulos escenas={escenas} />
			<Insignia escenas={escenas} nivel={nivel} />
		</AbsoluteFill>
	);
};
