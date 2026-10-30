import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, continueRender, delayRender, Series, staticFile} from 'remotion';
import {Escenario, Fondo, Insignia, Subtitulos} from './comun';
import {EscenaKit} from './escenas';
import {COLORES, FONDO} from './tema';
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
		<AbsoluteFill style={{backgroundColor: FONDO}}>
			<Fondo acento={COLORES.oro} />
			<Series>
				{escenas.map((e, i) => (
					<Series.Sequence key={i} durationInFrames={e.duracion}>
						<Escenario duracion={e.duracion}>
							<EscenaKit e={e} meta={meta} anclas={todasLasAnclas} />
						</Escenario>
						{e.audio && <Audio src={staticFile(e.audio)} />}
					</Series.Sequence>
				))}
			</Series>
			<Subtitulos escenas={escenas} />
			<Insignia escenas={escenas} nivel={nivel} />
		</AbsoluteFill>
	);
};
