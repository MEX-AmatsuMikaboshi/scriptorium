import '@fontsource/eb-garamond/400.css';
import '@fontsource/eb-garamond/500.css';
import '@fontsource/eb-garamond/400-italic.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';

export const COLORES = {
	oro: '#E3B261',
	azul: '#7DB4FF',
	rojo: '#FF8A72',
	verde: '#7FD6A8',
	violeta: '#B9A2FF',
} as const;

export type Acento = keyof typeof COLORES;

// Color que acompaña a cada acento cuando una escena necesita dos (p. ej. Contraste).
export const PAREJA: Record<Acento, Acento> = {
	oro: 'azul',
	azul: 'oro',
	rojo: 'azul',
	verde: 'violeta',
	violeta: 'verde',
};

export const TINTA = '#F2EEE6';
export const SUAVE = 'rgba(242, 238, 230, 0.6)';
export const TENUE = 'rgba(242, 238, 230, 0.14)';
export const FONDO = '#0B0C10';
export const SERIF = '"EB Garamond", Georgia, serif';
export const SANS = 'Inter, system-ui, sans-serif';

export const ETIQUETA: React.CSSProperties = {
	fontFamily: SANS,
	fontWeight: 600,
	fontSize: 22,
	letterSpacing: '0.32em',
	textTransform: 'uppercase',
};
